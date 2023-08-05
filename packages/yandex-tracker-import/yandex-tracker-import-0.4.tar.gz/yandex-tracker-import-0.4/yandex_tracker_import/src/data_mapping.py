def get_field(entity, field_path, default=None):
    fields = field_path.split('.')
    cur_value = entity
    for cur_field in fields:
        if not hasattr(cur_value, cur_field):
            return default

        cur_value = getattr(cur_value, cur_field)

    return cur_value


def get_type_config(queue, workflow_mapping):
    return [
        {
            'issueType': issue_type_config['issueType'].key,
            'workflow': workflow_mapping.get(issue_type_config['workflow'].id),
            'resolutions': [
                resolution.key
                for resolution in issue_type_config['resolutions']
            ],
        }
        for issue_type_config in queue['issueTypesConfig']
    ]


def get_data_from_queue(queue, workflow_mapping, importer):
    return {
        'key': queue['key'],
        'name': queue['name'],
        'lead': importer.get_dest_user_id(queue['lead'].id),
        'defaultType': queue['defaultType'].key,
        'defaultPriority': queue['defaultPriority'].key,
        'issueTypesConfig': [
            {
                'issueType': issue_type_config['issueType'].key,
                'workflow': workflow_mapping.get(issue_type_config['workflow'].id),
                'resolutions': [
                    resolution.key
                    for resolution in issue_type_config['resolutions']
                ],
            }
            for issue_type_config in queue['issueTypesConfig']
        ]
    }


def get_data_from_issue(
    source_issue, dest_status, dest_type,
    dest_priority, dest_components_by_name,
    sprints_mapping, importer,
):
    data = {
        'queue': get_field(source_issue, 'queue.key'),
        'summary': get_field(source_issue, 'summary'),
        'key': get_field(source_issue, 'key'),
        'createdAt': get_field(source_issue, 'createdAt'),
        'createdBy': importer.get_dest_user_id(get_field(source_issue, 'createdBy.id')),
        'updatedAt': get_field(source_issue, 'updatedAt'),
        'updatedBy': importer.get_dest_user_id(get_field(source_issue, 'updatedBy.id')),
        'resolvedAt': get_field(source_issue, 'resolvedAt'),
        'resolvedBy': importer.get_dest_user_id(get_field(source_issue, 'resolvedBy.id')),
        'status': dest_status.id,
        'aliases': get_field(source_issue, 'aliases'),
        'deadline': get_field(source_issue, 'deadline'),
        'resolution': get_field(source_issue, 'resolution'),
        'type': dest_type.id,
        'description': get_field(source_issue, 'description'),
        'start': get_field(source_issue, 'start'),
        'end': get_field(source_issue, 'end'),
        'assignee': importer.get_dest_user_id(get_field(source_issue, 'assignee.id')),
        'priority': dest_priority.id,
        'components': [
            dest_components_by_name[cur_source_component.name].id
            for cur_source_component in get_field(source_issue, 'components', [])
        ],
        'tags': get_field(source_issue, 'tags'),
        'sprint': [
            sprints_mapping.get(sprint.id)
            for sprint in get_field(source_issue, 'sprint', [])
        ],
        'followers': [
            importer.get_dest_user_id(follower.id)
            for follower in get_field(source_issue, 'followers', [])
        ],
        'unique': get_field(source_issue, 'unique'),
        'followingMaillists': get_field(source_issue, 'followingMaillists'),
        'originalEstimation': get_field(source_issue, 'originalEstimation'),
        'estimation': get_field(source_issue, 'estimation'),
        'spent': get_field(source_issue, 'spent'),
        'storyPoints': get_field(source_issue, 'storyPoints'),
        'votedBy': [importer.get_dest_user_id(user.id) for user in get_field(source_issue, 'votedBy', [])],
        'favoritedBy': [importer.get_dest_user_id(user.id) for user in get_field(source_issue, 'favoritedBy', [])],
        'descriptionRenderType': 'wf',
    }

    if data['resolvedAt'] and data['resolvedAt'] > data['updatedAt']:
        data['resolvedAt'] = data['updatedAt']

    return data


def get_data_from_board(board, board_type, importer):
    filter_fields_with_user_mapping = {
        'followers',
        'pendingReplyFrom',
        'resolver',
        'access',
        'author',
        'qaEngineer',
        'votedBy',
        'assignee',
    }
    board_data = {
        'name': board.name,
        'boardType': board_type,
        'filter': get_field(board, 'filter'),
        'query': get_field(board, 'query'),
        'useRanking': board.useRanking,
        'country': {'id': board.country.id},
        'defaultQueue': board.defaultQueue.key,
    }
    if board_data['filter']:
        board_data['orderBy'] = 'updated'
        board_data['orderAsc'] = False
        for filter_field in board_data['filter']:
            if filter_field not in filter_fields_with_user_mapping:
                continue
            uids = board_data['filter'][filter_field]
            board_data['filter'][filter_field] = [importer.get_dest_user_id(uid) for uid in uids]

    return board_data


def get_component_data(source_component, importer):
    data = {
        'name': source_component.name,
        'description': source_component.description,
        'queue': source_component.queue.key,
        'assignAuto': source_component.assignAuto,
    }
    lead = importer.get_dest_user_id(get_field(source_component, 'lead.id'))
    if lead:
        data['lead'] = lead

    return data


def get_data_from_checklist(check_list):
    data = {
        'text': check_list['text'],
        'checked': check_list['checked'],
    }
    for key in {'checklistItemType', 'deadline', 'url'}:
        if key in check_list:
            data[key] = check_list[key]
    return data
