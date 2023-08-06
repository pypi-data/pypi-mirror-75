from os import path

UPM_CONFIG_NAME = '.upmrc'

config_path = path.join(
    path.expanduser('~'),
    UPM_CONFIG_NAME
)

config = {
    'access_key': '',
    'secret_key': '',
    'bucket_name': ''
}


def update_config_file():
    """
    更新配置文件
    :return:
    """
    config_list = []
    for key, value in config.items():
        config_list.append('{}={}'.format(key, value))
    with open(config_path, 'w') as file:
        file.write('\n'.join(config_list))


def set_config(key, value):
    config[key] = value
    update_config_file()


def delete_config(key):
    del config[key]
    update_config_file()


def show_config():
    with open(config_path, 'r+') as file:
        print(file.read())


def init():
    """
    初始化配置文件
    :return:
    """
    if not path.exists(config_path):
        update_config_file()
    else:
        file = open(config_path)
        lines = file.read().splitlines()
        for line in lines:
            key, value = line.split('=')
            config[key] = value


if __name__ == '__main__':
    init()
