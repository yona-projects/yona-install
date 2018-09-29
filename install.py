import requests
import sys
import os
import zipfile
import pexpect
import click
import stat
import subprocess
import shlex
import yaml
import properties
import time

from pathlib import Path
from bs4 import BeautifulSoup
from subprocess import PIPE

release_url = 'https://github.com/yona-projects/yona/releases'
release_url_page = requests.get(release_url).content

doc = BeautifulSoup(release_url_page, 'lxml')
release_entry = doc.select('div.release-entry')

last_release = release_entry[0]
last_version = last_release.find(class_='release-header').find('a').string

click.echo('최고의 소스코드 관리 프로그램 Yona의 최근 발표 버전은 {0}입니다'.format(last_version))

install_yn = input('설치하시겠습니까? [Y/n] ')
install_yn = install_yn or 'Y'

if install_yn.upper() == 'N':
    click.echo('\nYona는 언제든지 당신을 기다립니다')
elif install_yn.upper() == 'Y':
    click.echo('\n설치를 시작합니다')
else:
    click.echo('\n잘못된 값을 입력하셨습니다')
    sys.exit()

yona_src_path = Path.home() / '.yona_install'
yona_src_path.mkdir(exist_ok=True)

yona_download_assets = last_release.find('details').find_all('a')
yona_tar_gz = None
for link in yona_download_assets:
    if 'mariadb' in link['href']:
        yona_tar_gz = link['href']

yona_download_full_link = 'https://github.com{0}'

yona_download_req = requests.get(yona_download_full_link.format(yona_tar_gz), stream=True)
yona_setup_file = yona_src_path / os.path.basename(yona_tar_gz)

if not yona_setup_file.exists() or (
        yona_setup_file.stat()[stat.ST_SIZE] != int(yona_download_req.headers['Content-Length'])):
    with yona_setup_file.open('wb') as yona_file:
            download_size = 0
            for chunk in yona_download_req.iter_content(chunk_size=1024 * 1024 * 1):
                yona_file.write(chunk)
                download_size += (1024 * 1024 * 1)
                print("{0:#,}/{1:#,}".format(download_size, int(yona_download_req.headers['Content-Length'])))

click.echo('Yona 다운로드가 되었습니다')

install_path = input('어디에 설치하시겠습니까? [{0}/yona-latest] '.format(Path.home()))
install_path = Path(install_path or '{0}/yona-latest'.format(Path.home()))

try:
    install_path.mkdir(exist_ok=True)
except Exception as e:
    click.echo('설치 디렉터리 생성에 실패했습니다. 파일 시스템 권한을 확인하세요')

yona_zip_file = zipfile.ZipFile(str(yona_setup_file.resolve()), 'r')

yona_files = yona_zip_file.infolist()


def permission(external_attr):
    stat_ix = (4, 2, 1)

    user_perm = 0
    for mode_num, mode in zip(stat_ix, (stat.S_IRUSR, stat.S_IWUSR, stat.S_IXUSR)):
        if (external_attr & mode) > 0:
            user_perm += mode_num

    grp_perm = 0
    for mode_num, mode in zip(stat_ix, (stat.S_IRGRP, stat.S_IWGRP, stat.S_IXGRP)):
        if (external_attr & mode) > 0:
            grp_perm += mode_num

    oth_perm = 0
    for mode_num, mode in zip(stat_ix, (stat.S_IROTH, stat.S_IWOTH, stat.S_IXOTH)):
        if (external_attr & mode) > 0:
            oth_perm += mode_num

    return int('0o{0}{1}{2}'.format(user_perm, grp_perm, oth_perm), 8)


for entry in yona_files[1:]:
    entry.filename = entry.filename[entry.filename.find("/") + 1:]
    yona_zip_file.extract(entry, path=str(install_path))
    st_mode = (entry.external_attr >> 16) & 0xFFFF
    perm = permission(st_mode)
    (install_path / str(entry.filename)).chmod(perm)

# https://ftp.harukasan.org/mariadb//mariadb-10.3.9/repo/
# MariaDB 설치

# 운영체제 확인
lsb_release = subprocess.run(shlex.split("lsb_release -a"), stdout=subprocess.PIPE)
lsb_release_result = lsb_release.stdout.splitlines()

distribute_os = lsb_release_result[0].split(b"\t")[1]
if distribute_os not in (b"Ubuntu", b"Debian"):
    click.echo("우분투 또는 데비안 리눅스가 아닙니다. 설치를 중단합니다")
    # TODO: 다운로드 받은 요나를 지운다.
    # TODO: H2 버전을 안내할지 생각해본다.

distribute_code = lsb_release_result[-1].split(b"\t")[1]
if (distribute_os == b"Ubuntu") and (distribute_code not in (b"artful", b"bionic", b"trusty",
                                                             b"xenial", b"yakkety", b"zesty")):
    click.echo("MariaDB 설치가 지원되지 않는 우분투 배포본입니다.")
    sys.exit(0)

if (distribute_os == b"Debian") and (distribute_code not in (b"jessie", b"sid", b"stretch", b"wheezy")):
    click.echo("MariaDB 설치가 지원되지 않는 데비안 배포본입니다.")
    sys.exit(0)

# dirmngr 설치 확인
dirmngr_installed = subprocess.run(shlex.split("dpkg -l dirmngr"), stdout=subprocess.PIPE)
if not dirmngr_installed.stdout.splitlines()[-1].startswith(b"ii"):
    click.echo("dirmngr 패키지가 설치되어 있지 않습니다. dirmngr 패키지를 설치합니다")
    subprocess.run(shlex.split("sudo apt-get install dirmngr"), stdout=PIPE)

# MariaDB GPG 키를 받아온다.
subprocess.run(
    shlex.split("sudo apt-key adv --recv-keys --keyserver hkp://keyserver.ubuntu.com:80 0xcbcb082a1bb943db"),
    stdout=PIPE)
subprocess.run(
    shlex.split("sudo apt-key adv --recv-keys --keyserver hkp://keyserver.ubuntu.com:80 0xF1656F24C74CD1D8"),
    stdout=PIPE)

with Path("/etc/apt/sources.list.d/mariadb.list").open("w") as apt_file:
    apt_file.write("deb http://ftp.harukasan.org/mariadb//mariadb-10.3.9/repo/{0} {1} main".format(
        distribute_os.decode("utf-8").lower(),
        distribute_code.decode("utf-8")
    ))

# 소스 저장소 갱신
subprocess.run(shlex.split("apt update"))

# MariaDB 설치
sysenv = os.environ.copy()
sysenv['DEBIAN_FRONTEND'] = 'noninteractive'

openjdk_install = subprocess.Popen("apt install openjdk-9-jre", stdout=PIPE, stdin=PIPE, shell=True, env=sysenv)
openjdk_install.communicate(b"y\n")

mariadb_install = subprocess.Popen("apt install mariadb-server", stdout=PIPE, stdin=PIPE, shell=True, env=sysenv)
stdout, stderr = mariadb_install.communicate(b"y\n")

click.echo("MariaDB 설치가 완료되었습니다.")

click.echo("MariaDB 설정을 진행합니다.")

install_settings = yaml.load(open("settings.yml"))

c = pexpect.spawn('mysql -u root')

c.expect('MariaDB [(none)]>')

# 유저 생성
c.sendline("create user '{user}'@'{host}' IDENTIFIED BY '{passwd}';".format_map(install_settings['db']))

# DB 생성
c.sendline("set global innodb_file_format = BARRACUDA;")
c.sendline("set global innodb_file_format_max = BARRACUDA;")
c.sendline("set global innodb_large_prefix = ON;")

c.sendline("create database {0}".format(install_settings['db']['name']))
c.sendline("DEFAULT CHARACTER SET utf8mb4")
c.sendline("DEFAULT COLLATE utf8mb4_bin;")

# 권한 부여
c.sendline("GRANT ALL ON {name}.* to '{user}'@'{host}';".format_map(install_settings['db']))

c.close()

# MariaDB 설정 파일 생성
with open("/etc/my.cnf", "w") as my_cnf:
    my_cnf.write("[client]\n")
    my_cnf.write("default-character-set=utf8mb4\n")
    my_cnf.write("\n")
    my_cnf.write("[mysql]\n")
    my_cnf.write("default-character-set=utf8mb4\n")
    my_cnf.write("\n")
    my_cnf.write("[mysqld]\n")
    my_cnf.write("collation-server=utf8mb4_unicode_ci\n")
    my_cnf.write("init-connect='SET NAMES utf8mb4'\n")
    my_cnf.write("character-set-server=utf8mb4\n")
    my_cnf.write("lower_case_table_names=1\n")
    my_cnf.write("innodb_file_format=barracuda\n")
    my_cnf.write("innodb_large_prefix=on\n")

# DB 데몬 재시작
subprocess.run("systemctl restart mariadb.service", shell=True)

# Yona 첫 실행
subprocess.run(install_path / 'bin' / 'yona')

time.sleep(3)

# application.conf 설정
conf = properties.db_settings(install_path / 'conf' / 'application.conf', install_settings['db'])
print(conf)

click.echo("Yona 설치가 완료되었습니다.\nYona와 함께 즐거운 코딩 되세요")
