import click
import logging

from ..src.importer import TrackerImporter


logging.getLogger("yandex_tracker_client").setLevel(logging.CRITICAL)
logging.getLogger("yandex_tracker_client").propagate = False


@click.command()
@click.option('--src_org_id', help='Source organization', required=True, prompt='src_org_id')
@click.option('--src_token', help='User token from source organization', required=True, prompt='src_token')
@click.option('--dst_org_id', help='Destination organization', required=True, prompt='dst_org_id')
@click.option('--dst_token', help='User token from destination organization', required=True, prompt='dst_token')
@click.option('--user_mapping', help='User mapping file path', required=True, prompt='user_mapping')
@click.option('--default_uid', help='Default user uid', prompt='default_uid')
def cli(src_org_id, src_token, dst_org_id, dst_token, user_mapping, default_uid):
    importer = TrackerImporter(
        src_org_id=src_org_id,
        src_token=src_token,
        dst_org_id=dst_org_id,
        dst_token=dst_token,
        user_mapping=user_mapping,
        default_uid=default_uid,
    )
    importer.run()


if __name__ == '__main__':
    cli()
