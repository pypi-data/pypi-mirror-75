from .data_mapping import get_field


def get_attachment_hash(attachment):
    return hash(attachment.name + attachment.mimetype + str(attachment.size))


def get_comment_hash(comment):
    attachment_hashes = tuple([get_attachment_hash(attachment) for attachment in comment.attachments])
    return hash(comment.text + str(hash(attachment_hashes)))


def get_link_hash(link):
    return hash(link.type.id + link.object.key + link.direction)


def get_board_hash(board):
    return hash(board.name + str(get_field(board, 'filter')) + str(get_field(board, 'query')))


def get_sprint_hash(sprint):
    return hash(sprint.name + sprint.startDate + sprint.endDate)
