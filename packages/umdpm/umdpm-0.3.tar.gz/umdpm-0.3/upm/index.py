import click
import shutil
import inquirer
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

    questions = [
        inquirer.Checkbox(
            'filename',
            message='选择需要下载的文件',
            choices=files
        ),
        inquirer.List(
            'cdn',
            message='是否上传cdn?[y/n]',
            choices=['yes', 'no']
        )
    ]
    answers = inquirer.prompt(questions)

    filenames = answers['filename']
    for filename in filenames:
        filepath = path.join('./package', filename)
        name = path.basename(filename)
        copyfile(
            filepath,
            path.join(getcwd(), name)
        )
        if answers['cdn'] == 'yes':
            upload_cdn(filepath)
            click.secho(f'✅ {name}上传成功', fg='blue')

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
