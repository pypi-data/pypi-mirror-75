import os

from datetime import datetime
from pathlib import Path

from yandex_tracker_client import TrackerClient
from yandex_tracker_client.collections import ImportCollectionMixin, Attachments, Workflows
from yandex_tracker_client.exceptions import NotFound, BadRequest, UnprocessableEntity

from .utils import (
    import_boards,
    import_columns,
    import_components,
    import_links,
    import_issues,
    import_queues,
    import_sprints,
)


class TrackerImporter:
    RELATION_MAP = {
        'relates': {'inward': 'relates', 'outward': 'relates'},
        'depends': {'inward': 'is dependent by', 'outward': 'depends on'},
        'subtask': {'inward': 'is subtask for', 'outward': 'is parent task for'},
        'duplicates': {'inward': 'duplicates', 'outward': 'is duplicated by'},
        'epic': {'inward': 'is epic of', 'outward': 'has epic'},
    }

    def __init__(
        self, src_org_id,
        src_token, dst_org_id,
        dst_token, user_mapping,
        default_uid=None,
    ):
        self.source_client = TrackerClient(token=src_token, org_id=src_org_id)
        self.dest_client = TrackerClient(token=dst_token, org_id=dst_org_id)
        self.user_map = self.make_user_map(user_mapping=user_mapping)
        self.default_uid = default_uid

        self._status_cache = {}
        self._type_cache = {}
        self._priority_cache = {}
        self._workflow_cache = {}

        self.errors = []

    def get_dest_user_id(self, source_user_id):
        if source_user_id is None:
            return None
        return self.user_map.get(str(source_user_id), self.default_uid or str(source_user_id))

    def make_user_map(self, user_mapping):
        user_map = {}
        if os.path.isfile(user_mapping):
            with open(user_mapping) as f:
                for line in f:
                    source_user_id, dest_user_id = line.split()
                    user_map[source_user_id] = dest_user_id
        else:
            print(f'Path {user_mapping} not found, will use only default_uid')
        return user_map

    def get_or_create_status(self, status_key, status_name):
        if status_key not in self._status_cache:
            try:
                status = self.dest_client.statuses.get(status_key)
            except NotFound:
                status = self.dest_client.statuses.create(key=status_key, name=status_name)
            self._status_cache[status_key] = status

        return self._status_cache[status_key]

    def get_or_create_type(self, source_type):
        if source_type.key not in self._type_cache:
            try:
                type = self.dest_client.issue_types.get(source_type.key)
            except NotFound:
                type = self.dest_client.issue_types.create(key=source_type.key, name=source_type.name)
            self._type_cache[source_type.key] = type

        return self._type_cache[source_type.key]

    def get_or_create_priority(self, source_priority):
        if source_priority.key not in self._priority_cache:
            try:
                priority = self.dest_client.priorities.get(source_priority.key)
            except NotFound:
                priority = self.dest_client.issue_types.create(key=source_priority.key, name=source_priority.name)
            self._priority_cache[source_priority.key] = priority

        return self._priority_cache[source_priority.key]

    def get_relation_name_by_link(self, link):
        return self.RELATION_MAP[link.type.id][link.direction]

    def _make_tmp_dir(self):
        tmp_dir = os.path.dirname(os.path.realpath(__file__)) + '/tmp_import'
        Path(tmp_dir).mkdir(exist_ok=True)
        return tmp_dir

    def run(self):
        self.tmp_dir = self._make_tmp_dir()

        dest_workflows_ids = {
            workflow.id
            for workflow in Workflows(self.dest_client._connection).get_all()
        }

        source_queues = self.source_client.queues.get_all(expand='all')

        dest_queue_by_key = import_queues(
            source_client=self.source_client,
            dest_client=self.dest_client,
            dest_workflows_ids=dest_workflows_ids,
            workflow_mapping=self._workflow_cache,
            source_queues=source_queues,
            importer=self,
        )
        source_boards = self.source_client.boards.get_all()
        dest_boards_by_hash = import_boards(
            source_client=self.source_client,
            dest_client=self.dest_client,
            source_boards=source_boards,
            importer=self,
        )
        import_columns(
            source_client=self.source_client,
            dest_client=self.dest_client,
            source_boards=source_boards,
            dest_boards_by_hash=dest_boards_by_hash,
            importer=self,
        )
        sprints_mapping = import_sprints(
            source_client=self.source_client,
            dest_client=self.dest_client,
            source_boards=source_boards,
            dest_boards_by_hash=dest_boards_by_hash,
        )
        for queue in source_queues:
            dest_components_by_name = import_components(
                source_client=self.source_client,
                dest_client=self.dest_client,
                source_queue=queue,
                dest_queue_by_key=dest_queue_by_key,
                importer=self,
            )
            source_issues = self.source_client.issues.find(
                queue=queue.key,
            )
            dest_issue_by_key = import_issues(
                source_client=self.source_client,
                dest_client=self.dest_client,
                source_issues=source_issues,
                importer=self,
                dest_components_by_name=dest_components_by_name,
                sprints_mapping=sprints_mapping,
            )
            import_links(
                source_client=self.source_client,
                dest_client=self.dest_client,
                dest_issue_by_key=dest_issue_by_key,
                source_issues=source_issues,
                importer=self,
            )
        print(f'Process finished, got total {len(self.errors)} errors: {self.errors}')




