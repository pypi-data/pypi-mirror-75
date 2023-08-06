# coding: utf-8

storage_server = 'ip'


def test_file_info_raw():
    import socket, struct

    fmt_head = '!QBB'

    group_name = b'group1'
    file_id = b'M00/00/1D/oYYBAF78D_uAQPHKACQBXRgNsdk46.json1'

    body = struct.pack('!16s %ds' % len(file_id), group_name, file_id)
    head = struct.pack('!QBB', len(body), 22, 0)

    sock = socket.create_connection((storage_server, 11049))
    sock.send(head)
    sock.send(body)

    ret = sock.recv(1024)
    print()
    print('ret', ret)
    ret_len, ret_cmd, ret_status = struct.unpack(fmt_head, ret[:10])
    if ret_status != 0:
        print('error', ret_status)
    else:
        ret_body = struct.unpack('!QQQ16s', ret[10:])
        print('header', ret_len, ret_cmd, ret_status)
        print('ret_body', ret_body)


def test_file_info():
    from fdfs_client import client
    cli = client.Fdfs_client(client.get_tracker_conf('~/.local/etc/fdfs/client.conf'))
    ret = cli.query_file_info('group1/M00/00/1D/oYYBAF78D_uAQPHKACQBXRgNsdk46.json')
    print(ret)
