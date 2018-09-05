import requests
import sys
import os
import gzip
import tarfile
import shutil
import click

from pathlib import Path
from bs4 import BeautifulSoup

click.echo('Yona와 찰떡궁합 데이터베이스 MariaDB v10.3.9 x86_64 버전을 설치합니다.')

install_yn = input('설치하시겠습니까? [Y/n] ')
install_yn = install_yn or 'Y'

if install_yn.upper() == 'N':
    click.echo('\nYona를 안정적으로 사용하시려면 MariaDB를 꼭 설치하세요')
elif install_yn.upper() == 'Y':
    click.echo('\n설치를 시작합니다')
else:
    click.echo('\n잘못된 값을 입력하셨습니다')
    sys.exit()

yona_src_path = Path.home() / '.yona_install'
yona_src_path.mkdir(exist_ok=True)

maria_download_full_link = 'http://ftp.kaist.ac.kr/mariadb/mariadb-10.3.9/bintar-linux-x86_64/mariadb-10.3.9-linux-x86_64.tar.gz'

mariadb_download_req = requests.get(maria_download_full_link)
with (yona_src_path / os.path.basename(maria_download_full_link)).open('wb') as maria_file:
    maria_file.write(mariadb_download_req.content)

click.echo('MariaDB 다운로드가 되었습니다')

'''install_path = input('어디에 설치하시겠습니까? [{0}/yona-latest] '.format(Path.home()))
install_path = Path(install_path or '{0}/yona-latest'.format(Path.home()))

try:
    install_path.mkdir(exist_ok=True)
except Exception as e:
    click.echo('설치 디렉터리 생성에 실패했습니다. 파일 시스템 권한을 확인하세요')

yona_tar_file = tarfile.open((yona_src_path / os.path.basename(yona_tar_gz)).resolve(), 'r:gz')
yona_files = yona_tar_file.getmembers()

yona_root_dir = yona_files[0].name
yona_setup_files = yona_files[1:]

for entry in yona_setup_files:
    extract_path = install_path / entry.name[len(yona_root_dir) + 1:]

    if entry.isdir():
        extract_path.mkdir(exist_ok=True)
    else:
        extract_file = yona_tar_file.extractfile(entry)

        if not extract_file:
            continue

        shutil.copyfileobj(extract_file, extract_path.open('wb'))
        extract_path.chmod(entry.mode - 16) 

click.echo("Yona 설치가 완료되었습니다.\nYona와 함께 즐거운 코딩 되세요")
'''
