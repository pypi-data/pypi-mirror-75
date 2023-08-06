# coding: utf-8
CONF_FILE = '~/.local/etc/fdfs/client.conf'


def test_use_storage_id():
    from fdfs_client import client
    client.get_tracker_conf(CONF_FILE)


def test_upload():
    from fdfs_client import client
    cli = client.Fdfs_client(client.get_tracker_conf(CONF_FILE))
    ret = cli.upload_appender_by_buffer(b'a', 'test')
    remote_file_id = ret['Remote file_id']
    cli.delete_file(remote_file_id)


def test_create_appender_by_zefo_buffer():
    from fdfs_client import client
    cli = client.Fdfs_client(client.get_tracker_conf(CONF_FILE))
    ret = cli.upload_appender_by_buffer(b'', 'test')
    remote_file_id = ret['Remote file_id']
    cli.delete_file(remote_file_id)
