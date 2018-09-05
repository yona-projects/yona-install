import requests
import sys
import os
import gzip
import tarfile
import shutil
import click

from pathlib import Path
from bs4 import BeautifulSoup

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
    if link['href'].endswith('tar.gz'):
        yona_tar_gz = link['href']

yona_download_full_link = 'https://github.com{0}'

yona_download_req = requests.get(yona_download_full_link.format(yona_tar_gz))
with (yona_src_path / os.path.basename(yona_tar_gz)).open('wb') as yona_file:
    yona_file.write(yona_download_req.content)

click.echo('Yona 다운로드가 되었습니다')

install_path = input('어디에 설치하시겠습니까? [{0}/yona-latest] '.format(Path.home()))
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
