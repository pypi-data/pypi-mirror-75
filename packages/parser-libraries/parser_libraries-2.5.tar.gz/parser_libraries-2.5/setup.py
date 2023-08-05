from setuptools import setup

setup(
    name='parser_libraries',
    version='2.5',
    packages=['parser_libraries'],
    author_email='ivan.frinom@gmail.com',
    install_requires=[
        'pymysql',
        'openpy',
        'requests',
	'bs4',
	'selenium',
	'pytelegrambotapi'
    ]
)
