import click
import shutil
from os import path, getcwd
from shutil import copyfile
from upm.cdn import upload_cdn
from upm import config as config_obj, npm


@click.group(chain=True)
def cli():
    """
    命令行工具
    :return:
    """
    config_obj.init()


@cli.command()
@click.argument('name')
def install(name):
    """
    下载包
    :param name:
    :return:
    """
    click.secho('🥰 正在查询' + name + '...', fg='blue')
    files = npm.fetch_package_files(name)

    if len(files) <= 0:
        click.secho('❎ 未找到{}'.format(name), fg='red')
        exit(1)

    click.secho('\n'.join(files), fg='green')
    filepath = click.prompt('输入需要下载的文件')
    filename = path.basename(filepath)

    try:
        copyfile(
            filepath,
            path.join(getcwd(), filename)
        )
        click.confirm('是否上传cdn?', default=False, abort=True)
        upload_cdn(filepath)
        click.secho('✅ 上传文件成功', fg='blue')
    except IOError:
        click.secho('❎ 文件不存在', fg='red')
        exit(1)
    finally:
        shutil.rmtree('package')


@cli.command('config')
def config():
    pass


@cli.command('set')
@click.argument('key', type=click.Choice(['access_key', 'secret_key', 'bucket_name']))
@click.argument('value')
def config_set(key, value):
    config_obj.set_config(key, value)


@cli.command('delete')
@click.argument('key', type=click.Choice(['access_key', 'secret_key', 'bucket_name']))
def config_delete(key):
    config_obj.delete_config(key)


@cli.command('list')
def config_list():
    config_obj.show_config()


if __name__ == '__main__':
    cli()
