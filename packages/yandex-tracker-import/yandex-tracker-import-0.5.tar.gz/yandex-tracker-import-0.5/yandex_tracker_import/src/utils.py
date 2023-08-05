import os

from yandex_tracker_client.collections import (
    ImportCollectionMixin,
    Attachments,
    Workflows,
    Collection,
)
from yandex_tracker_client.exceptions import (
    NotFound,
    BadRequest,
    UnprocessableEntity,
)

from .data_mapping import (
    get_component_data,
    get_data_from_board,
    get_data_from_issue,
    get_data_from_queue,
    get_type_config,
    get_data_from_checklist,
)

from .hashing import (
    get_attachment_hash,
    get_comment_hash,
    get_link_hash,
    get_sprint_hash,
    get_board_hash,
)


class CommentAttachments(ImportCollectionMixin, Attachments):
    path = '/{api_version}/issues/{issue}/comments/{comment}/attachments/{id}'
    import_path = '/{api_version}/issues/{issue}/comments/{comment}/attachments/_import'
    fields = Attachments.fields


class CheckLists(Collection):
    path = '/{api_version}/issues/{issue}/checklistItems'
    fields = {
        'id': None,
        'text': None,
        'checked': None,
        'checklistItemType': None,
    }

    def create(self, items, params=None,):
        return self._execute_request(
            self._connection.post,
            path=self.path,
            params=params,
            data=items,
        )


def import_workflow(source_client, dest_client, source_workflow_id, importer):
    source_workflow = Workflows(source_client._connection).get(source_workflow_id)
    dest_workflow_data = {
        'name': source_workflow['name'],
        'steps': [
            {
                'status': importer.get_or_create_status(step['status'].key, step['status'].name),
                'actions': [
                    {
                        'target': importer.get_or_create_status(action['target'].key, action['target'].name),
                        'name': {
                            'ru': action['name'],
                            'en': action['id'],
                        },
                    }
                    for action in step['actions']
                ]
            }
            for step in list(source_workflow['steps'])
        ],
        'initialAction': {
            'target': importer.get_or_create_status(
                source_workflow['initialAction']['target'].key,
                source_workflow['initialAction']['target'].name,
            ),
            'name': {
                'ru': source_workflow['initialAction']['name'],
                'en': source_workflow['initialAction']['id'],
            }
        }
    }
    return Workflows(dest_client._connection).create(_create_path='/{api_version}/workflows/', **dest_workflow_data)


def import_types_config(source_queue, dest_queue, workflow_mapping):
    type_config = get_type_config(source_queue, workflow_mapping)
    dest_queue.update(issueTypesConfig=type_config)


def import_queues(source_client, dest_client, workflow_mapping, dest_workflows_ids, source_queues, importer):
    dest_queue_by_key = {}
    for source_queue in source_queues:
        print('import queue: ' + source_queue.key)

        for issue_type_config in source_queue['issueTypesConfig']:
            workflow_id = issue_type_config['workflow'].id
            if workflow_id in workflow_mapping:
                continue
            if workflow_id in dest_workflows_ids:
                workflow_mapping[workflow_id] = workflow_id
                continue
            dest_workflow = import_workflow(
                source_workflow_id=workflow_id,
                source_client=source_client,
                dest_client=dest_client,
                importer=importer,
            )
            workflow_mapping[workflow_id] = dest_workflow.id

        try:
            dest_queue = dest_client.queues.get(source_queue['key'])
            import_types_config(
                source_queue=source_queue,
                dest_queue=dest_queue,
                workflow_mapping=workflow_mapping
            )
        except NotFound:
            data = get_data_from_queue(source_queue, workflow_mapping, importer)
            dest_queue = dest_client.queues.create(**data)
        dest_queue_by_key[dest_queue.key] = dest_queue

    return dest_queue_by_key


def import_boards(source_client, dest_client, source_boards, importer):
    dest_boards = dest_client.boards.get_all()
    dest_boards_by_hash = {
        get_board_hash(dest_board): dest_board
        for dest_board in dest_boards
    }
    for source_board in source_boards:
        print('import board: ' + source_board.name)
        if get_board_hash(source_board) in dest_boards_by_hash:
            continue

        try:
            source_client.boards.sprints(source_board).get_all()
            board_type = 'scrum'
        except BadRequest:
            board_type = 'default'

        data = get_data_from_board(board=source_board, board_type=board_type, importer=importer)
        dest_board = dest_client.boards.create(**data)
        dest_boards_by_hash[get_board_hash(dest_board)] = dest_board

    return dest_boards_by_hash


def import_columns(source_client, dest_client, source_boards, dest_boards_by_hash, importer):
    for source_board in source_boards:
        print('import columns for board: ' + source_board.name)
        dest_board = dest_boards_by_hash[get_board_hash(source_board)]
        dest_board_version = dest_board.version

        # удаляем старые
        for dest_column in dest_client.boards.columns(dest_board).get_all():
            dest_columns = dest_client.boards.columns(dest_board)
            dest_columns._execute_request(
                dest_columns._connection.delete,
                dest_column._path, params={
                    'version': dest_board_version
                }
            )
            dest_board_version += 1

        # добавляем новые
        for source_column in source_client.boards.columns(source_board).get_all():
            dest_client.boards.columns(dest_board).create(
                name=source_column.name,
                statuses=[
                    importer.get_or_create_status(status.key, status.name).key
                    for status in source_column.statuses
                ],
                params={
                    'version': dest_board_version
                }
            )
            dest_board_version += 1


def import_sprints(source_client, dest_client, source_boards, dest_boards_by_hash):
    sprint_mapping = {}
    for source_board in source_boards:
        print('import sprints for board: ' + source_board.name)
        dest_board = dest_boards_by_hash[get_board_hash(source_board)]
        source_sprints = source_client.boards.sprints(source_board)

        try:
            dest_sprints = dest_client.boards.sprints(dest_board).get_all()
        except BadRequest:
            continue

        dest_sprints_by_hash = {
            get_sprint_hash(dest_sprint): dest_sprint
            for dest_sprint in dest_sprints
        }
        for source_sprint in source_sprints:
            source_sprint_hash = get_sprint_hash(source_sprint)
            if source_sprint_hash in dest_sprints_by_hash:
                sprint_mapping[str(source_sprint.id)] = str(dest_sprints_by_hash[source_sprint_hash].id)
                continue
            dest_sprint = dest_client.sprints.create(
                name=source_sprint.name,
                board={'id': dest_board.id},
                startDate=source_sprint.startDate,
                endDate=source_sprint.endDate,
            )
            sprint_mapping[str(source_sprint.id)] = str(dest_sprint.id)
    return sprint_mapping


def import_components(source_client, dest_client, source_queue, dest_queue_by_key, importer):
    source_components = source_client.queues.components(source_queue)
    dest_components = dest_client.queues.components(dest_queue_by_key[source_queue.key])
    dest_components_by_name = {dest_component.name: dest_component for dest_component in dest_components}
    for source_component in source_components:
        if source_component.name in dest_components_by_name:
            continue
        data = get_component_data(source_component=source_component, importer=importer)
        dest_component = dest_client.components.create(**data)
        dest_components_by_name[dest_component.name] = dest_component
    return dest_components_by_name


def import_issues(
    source_client, dest_client, source_issues,
    importer, dest_components_by_name,
    sprints_mapping,
):
    dest_issue_by_key = {}

    for source_issue in source_issues:
        print('import issue: ' + source_issue.key)
        try:
            dest_issue = dest_client.issues.get(source_issue['key'])
            dest_issue_by_key[dest_issue.key] = dest_issue
        except NotFound:
            dest_status = importer.get_or_create_status(source_issue.status.key, source_issue.status.name)
            dest_type = importer.get_or_create_type(source_issue.type)
            dest_priority = importer.get_or_create_priority(source_issue.priority)

            data = get_data_from_issue(
                source_issue=source_issue,
                dest_status=dest_status,
                dest_type=dest_type,
                dest_priority=dest_priority,
                dest_components_by_name=dest_components_by_name,
                sprints_mapping=sprints_mapping,
                importer=importer,
            )
            try:
                dest_issue = dest_client.issues.import_object(**data)
                dest_issue_by_key[dest_issue.key] = dest_issue
                import_comments(
                    source_client=source_client,
                    dest_client=dest_client,
                    source_issue=source_issue,
                    dest_issue=dest_issue,
                    importer=importer,
                )
                import_issue_files(
                    source_client=source_client,
                    dest_client=dest_client,
                    source_issue=source_issue,
                    dest_issue=dest_issue,
                    importer=importer,
                )
                import_checklists(
                    dest_client=dest_client,
                    source_issue=source_issue,
                    dest_issue=dest_issue,
                )
            except UnprocessableEntity as e:
                importer.errors.append(f'error importing issue {source_issue.key} | error: {str(e)}')
    return dest_issue_by_key


def import_comments(source_client, dest_client, source_issue, dest_issue, importer):
    print('import comments for issue: ' + source_issue.key)
    source_comments = source_client.issues.comments(source_issue).get_all(expand='attachments')

    dest_comments = dest_client.issues.comments(dest_issue).get_all(expand='attachments')
    dest_comments_by_hash = {
        get_comment_hash(dest_comment): dest_comment
        for dest_comment in dest_comments
    }

    for source_comment in source_comments:
        if get_comment_hash(source_comment) in dest_comments_by_hash:
            continue

        dest_comment_updated_at = source_comment.updatedAt
        if dest_issue.updatedAt < dest_comment_updated_at:
            dest_comment_updated_at = dest_issue.updatedAt

        dest_comment = dest_client.issues.comments(dest_issue).import_object(
            text=source_comment.text,
            createdAt=dest_comment_updated_at,
            createdBy=importer.get_dest_user_id(source_comment.createdBy.uid),
            updatedAt=dest_comment_updated_at,
            updatedBy=importer.get_dest_user_id(source_comment.updatedBy.uid),
            textRenderType='wf',
        )
        import_comment_files(
            source_client=source_client,
            dest_client=dest_client,
            dest_issue=dest_issue,
            dest_comment=dest_comment,
            source_comment=source_comment,
            importer=importer,
        )


def import_checklists(dest_client, source_issue, dest_issue):
    print('import checklists for issue: ' + source_issue.key)
    check_lists = []
    for check_list in source_issue['checklistItems']:
        check_lists.append(get_data_from_checklist(check_list))

    if check_lists:
        CheckLists(dest_client._connection).create(
            items=check_lists,
            params={'issue': dest_issue.key},
        )


def import_comment_files(source_client, dest_client, source_comment, dest_comment, dest_issue, importer):
    for source_attachment in source_comment.attachments:
        source_client.attachments.download_to(source_attachment, importer.tmp_dir)
        filepath = importer.tmp_dir + '/' + source_attachment.name
        CommentAttachments(dest_client._connection).import_object(
            filepath,
            params={
                'issue': dest_issue.key, 'comment': dest_comment.id,
                'createdAt': dest_comment.createdAt,
                'createdBy': dest_comment.createdBy
            },
        )
        os.remove(filepath)


def import_links(source_client, dest_client, source_issues, dest_issue_by_key, importer):
    for source_issue in source_issues:
        print('import links for issue: ' + source_issue.key)
        dest_issue = dest_issue_by_key.get(source_issue.key)
        if not dest_issue:
            importer.errors.append(f'skip importing links for issue {source_issue.key}')
            continue

        source_links = source_client.issues.links(source_issue)
        dest_links = dest_client.issues.links(dest_issue)
        dest_links_by_hash = {
            get_link_hash(dest_link): dest_link
            for dest_link in dest_links
        }

        for source_link in source_links:
            if source_link.direction == 'outward' or get_link_hash(source_link) in dest_links_by_hash:
                continue

            source_link_updated_at = source_link.updatedAt
            if source_link_updated_at > dest_issue.updatedAt:
                source_link_updated_at = dest_issue.updatedAt
            if source_link_updated_at < dest_issue.createdAt:
                source_link_updated_at = dest_issue.updatedAt

            linked_dest_issue = dest_issue_by_key.get(source_link.object.key)
            if not linked_dest_issue:
                importer.errors.append(
                    f'skip linking issues {source_issue.key} and'
                    f' {source_link.object.key} because {source_link.object.key} not imported'
                )
                continue

            if source_link_updated_at > linked_dest_issue.updatedAt:
                source_link_updated_at = linked_dest_issue.updatedAt
            if source_link_updated_at < linked_dest_issue.createdAt:
                source_link_updated_at = linked_dest_issue.updatedAt

            dest_client.issues.links(dest_issue).import_object(
                relationship=importer.get_relation_name_by_link(source_link),
                issue=source_link.object.key,
                createdAt=source_link_updated_at,
                createdBy=importer.get_dest_user_id(source_link.createdBy.id),
                updatedAt=source_link_updated_at,
                updatedBy=importer.get_dest_user_id(source_link.updatedBy.id),
            )


def import_issue_files(source_client, dest_client, source_issue, dest_issue, importer):
    print('import files for issue: ' + source_issue.key)

    source_attachments = source_client.issues.attachments(source_issue)
    dest_attachments = dest_client.issues.attachments(dest_issue)
    dest_attachments_by_hash = {
        get_attachment_hash(dest_attachment): dest_attachment
        for dest_attachment in dest_attachments
    }

    for source_attachment in source_attachments:
        if get_attachment_hash(source_attachment) in dest_attachments_by_hash:
            continue

        source_client.attachments.download_to(source_attachment, importer.tmp_dir)
        filepath = importer.tmp_dir + '/' + source_attachment.name
        attachment_created_at = source_attachment.createdAt
        if attachment_created_at > dest_issue.updatedAt:
            attachment_created_at = dest_issue.updatedAt
        elif attachment_created_at < dest_issue.createdAt:
            attachment_created_at = dest_issue.createdAt

        dest_client.issues.attachments(dest_issue).import_object(
            filepath,
            params={
                'createdAt': attachment_created_at,
                'createdBy': importer.get_dest_user_id(source_attachment.createdBy.id),
            },
        )
        os.remove(filepath)
