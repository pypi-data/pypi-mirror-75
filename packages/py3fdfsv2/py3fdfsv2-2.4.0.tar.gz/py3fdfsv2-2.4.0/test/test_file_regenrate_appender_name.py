# coding: utf-8

storage_server = 'fdfs_server'


def test_regenerate_appender_file_name():
    from fdfs_client import client
    cli = client.Fdfs_client(client.get_tracker_conf('~/.local/etc/fdfs/client.conf'))
    ret = cli.upload_appender_by_buffer(b'just a test', 'test')
    file_id = ret.get('Remote file_id')
    try:
        print(file_id)
        ret2 = cli.regenerate_appender_filename(file_id)
        print('regenerate appender filename: ', ret)
        ret3 = cli.delete_file(ret2.get('Remote file_id'))
        print('delete result', ret3)
    except:
        ret4 = cli.delete_file(ret.get('Remote file_id'))
        print('delete result', ret4)
        raise
