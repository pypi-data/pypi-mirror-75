from setuptools import setup, find_packages

VERSION = '0.3'
setup(
    name='umdpm',
    version=VERSION,
    description='umd 包管理',
    keywords='swagdog',
    author='wayne',
    author_email='hi.wayne@qq.com',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=[
        'qiniu',
        'click',
        'inquirer'
    ],
    entry_points={
        'console_scripts': [
            'upm = upm.index:cli'
        ]
    }
)

