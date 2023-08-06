# coding: utf-8

import json
import os

import click

from fdfs_client import client
from fdfs_client import jsonencoder


def print_result(ret):
    click.echo(json.dumps(ret, indent=2, ensure_ascii=False, cls=jsonencoder.MyJsonEncoder))


def get_fdfs_cli(conf=os.path.expanduser('~/.local/etc/fdfs/client.conf')):
    return client.Fdfs_client(client.get_tracker_conf(conf))


@click.group()
def main():
    """
    Usage

    * Upload once:

        fdfs upload <filepath>

    * Upload by chunks:

        fdfs create <file_ext_no_dot>

        fdfs append <remote_file_id> <filepath>

    * Download

        fdfs download <remote_file_id>

    * Delete:

        fdfs delete <remote_file_id>
    """
    pass


@main.command()
@click.option('--conf', default='~/.local/etc/fdfs/client.conf', help='the client.conf path')
@click.argument('filepath', type=click.Path(exists=True))
def upload(filepath, conf):
    """Direct upload."""
    cache_last_folder_path(filepath)
    click.echo(f'Uploading: {filepath}, using: {conf}')
    cli = get_fdfs_cli(conf)
    ret = cli.upload_by_filename(filepath)
    print(ret)


@main.command()
@click.option('--conf', default='~/.local/etc/fdfs/client.conf')
@click.argument('remote_file_id')
def delete(remote_file_id, conf):
    cache_last_folder_path(remote_file_id)
    if '/' not in remote_file_id:
        folder = get_last_folder_path()
        remote_file_id = f'{folder}/{remote_file_id}'
    click.echo(f'Deleting: {remote_file_id}, using: {conf}')
    cli = get_fdfs_cli(conf)
    ret = cli.delete_file(remote_file_id.encode())
    print_result(ret)


@main.command()
@click.option('--conf', default='~/.local/etc/fdfs/client.conf', help='the client.conf path')
@click.argument('ext_name')
def create(conf, ext_name):
    """Using this cmd to create a upload task for big files"""
    click.echo(f'Creating appender for big files uploading... ({conf})')
    cli = get_fdfs_cli(conf)
    ret = cli.upload_appender_by_buffer(b'', ext_name.encode())
    print_result(ret)


@main.command()
@click.option('--conf', default='~/.local/etc/fdfs/client.conf', help='the client.conf path')
@click.argument('remote_file_id')
@click.argument('filepath', type=click.Path(exists=True))
def append(conf, remote_file_id, filepath):
    cache_last_folder_path(remote_file_id)
    """Append content to the appender remote file id"""
    click.echo(f'Append data to remote file id: {remote_file_id}, file: {filepath}, conf: {conf}')
    cli = get_fdfs_cli(conf)
    ret = cli.append_by_filename(filepath, remote_file_id.encode())
    print_result(ret)


@main.command()
@click.option('--conf', default='~/.local/etc/fdfs/client.conf', help='the client.conf path')
@click.argument('remote_file_id')
@click.argument('download_to', type=click.Path(exists=False))
def download(conf, remote_file_id, download_to):
    cache_last_folder_path(remote_file_id)
    click.echo(f'Downloading file id: {remote_file_id}, to: {download_to}, using conf: {conf}')
    cli = get_fdfs_cli(conf)
    ret = cli.download_to_file(download_to, remote_file_id.encode())
    print_result(ret)


@main.command()
@click.option('--conf', default='~/.local/etc/fdfs/client.conf', help='the client.conf path')
@click.option('--file_id', '-f', default=None, help='Force use this file id')
@click.argument('filepath', type=click.Path(exists=True))
def upload2(filepath, conf, file_id):
    """Chunk upload"""
    import os, pathlib
    click.echo(f'Uploading: {filepath}, using: {conf}')
    cli = get_fdfs_cli(conf)

    meta_dict = {}
    meta_file = pathlib.Path(filepath + '.upload')

    if meta_file.exists():
        meta_file_handler = meta_file.open('r')
        meta_dict = json.load(meta_file_handler)
        meta_file_handler.close()

    file_id = file_id or meta_dict.get('file_id')

    if not file_id:
        ret = cli.upload_appender_by_buffer(b'', os.path.splitext(filepath)[-1].replace('.', ''))
        file_id = ret['Remote file_id']
        meta_dict['file_id'] = file_id.decode()
        click.echo(f'file_id: {file_id}')
        meta_file_handler = meta_file.open('w')
        json.dump(meta_dict, meta_file_handler, ensure_ascii=False, indent=2)
        meta_file_handler.close()
    if isinstance(file_id, str):
        file_id = file_id.encode()
    offset, create_timestamp, crc32, source_ip_addr = cli.query_file_info(file_id)
    if offset == pathlib.Path(filepath).stat().st_size:
        click.echo(f'File upload complete: {offset}')
        # meta_file.unlink()
        return
    else:
        click.echo(f'Uploading from offset: {offset}')

    with open(filepath, 'rb') as fin:
        fin.seek(offset)
        buffer_size = 1024 * 1024 * 5
        while True:
            buffer = fin.read(buffer_size)
            if not buffer:
                click.echo('Upload complete!')
                meta_file.unlink()
                ret = cli.regenerate_appender_filename(file_id)
                click.echo(ret)
                break
            # todo 应该校验crc32，但是 Fdfs 是自定义的 hash 规则。还没实现。有空再说
            ret = cli.append_by_buffer(buffer, file_id)
            print(ret)


@main.command()
@click.option('--conf', default='~/.local/etc/fdfs/client.conf', help='the client.conf path')
@click.argument('remote_file_id')
def info(conf, remote_file_id):
    cli = get_fdfs_cli(conf)
    ret = cli.query_file_info(remote_file_id.encode())
    print_result(ret)


@main.command()
def version():
    import fdfs_client
    print(fdfs_client.__version__)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Cache(metaclass=Singleton):
    def __init__(self):
        self.file_name = '/tmp/fdfs.cache'

        init_data = None
        if os.path.exists(self.file_name):
            with open(self.file_name) as fin:
                init_data = fin.read()
        self.cache = json.loads(init_data) if init_data else {}

    def get(self, key):
        return self.cache.get(key)

    def set(self, key, value):
        self.cache[key] = value
        with open(self.file_name, 'w') as cache_file:
            json.dump(self.cache, cache_file)


def get_folder_path(file_id: str):
    if '/' in file_id:
        folder, file_name = file_id.rsplit('/', 1)
        return folder
    else:
        return ''


def cache_last_folder_path(file_id):
    if '/' in file_id:
        folder_path = get_folder_path(file_id)
        Cache().set('last_folder', folder_path)


def get_last_folder_path():
    return Cache().get('last_folder')


if __name__ == '__main__':
    main()
