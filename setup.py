from setuptools import setup, find_packages

setup_requires = []

install_requires = [
    'requests',
    'lxml',
    'beautifulsoup4',
    'click',
    'future',
    'pyyaml',
    'pexpect'
]

dependency_links = []

setup(
    name='yona',
    url='https://github.com/yona-projects/yona-install',
    version='1.0',
    description='요나 설치 프로그램',
    author='Ji-ho Persy Lee',
    author_email='jhlee@flask.moe',
    packages=find_packages(),
    install_requires=install_requires,
    setup_requires=setup_requires,
    dependency_links=dependency_links,
    scripts=['install.py', 'properties.py'],
    entry_points={
        'console_scripts': [
            'yona_install = install:main'
        ],
    }
)
