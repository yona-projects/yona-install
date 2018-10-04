# Yonafi

## Yona Installer

### Prequires
* OS: Ubuntu, Debian 8 or 9
* Python:3.5 or higher

### 설치 방법

1. 리눅스에 root 사용자로 로그인 합니다.
1. git 명령어를 사용해 yonafi를 다운로드 받습니다.

   ```shell
   # git clone https://github.com/yona/yona-install
   ```

1. 파이썬 가상환경을 만들고 진입합니다.

    ```shell
    # pip3 install pipenv
    # cd yona-install
    # pipenv install
    # pipenv shell
    ``` 

1. 요나를 설치합니다.

    ```shell
    # python install.py
    최고의 소스코드 관리 프로그램 Yona의 최근 발표 버전은 Yona v1.10.1 Beta build입니다
    설치하시겠습니까? [Y/n] 
    
    설치를 시작합니다
    ... 다운로드 상태 출력
    Yona 다운로드가 되었습니다
    어디에 설치하시겠습니까? [/root/yona-latest] 
    dirmngr 패키지가 설치되어 있지 않습니다. dirmngr 패키지를 설치합니다
    OpenJDK를 설치합니다
    
    WARNING: apt does not have a stable CLI interface. Use with caution in scripts.
    
    패키지에서 템플릿을 추출하는 중: 100%
    MariaDB를 설치합니다
    
    WARNING: apt does not have a stable CLI interface. Use with caution in scripts.
    
    패키지에서 템플릿을 추출하는 중: 100%
    MariaDB 설정을 진행합니다.
    Yona 설치가 완료되었습니다.
    Yona와 함께 즐거운 코딩 되세요
    ``` 

### 주요 기능

* Yona 최신 안정화 버전 다운로드
* OpenJRE 자동 설치
* MariaDB 자동 설치

### Future

* 데비안과 우분투 하위 버전 테스트
* CentOS 지원
* YONA_DATA 환경 변수 지정 기능
* yonafi 스크립트 지원
* 시스템 데몬 등록 기능(systemd 우선 지원)
* DB 설정 기능
* 그 외, 생각나는건 있지만 새벽이라 이제 그만

### Troubleshooting

1. pip3 명령이 없습니다.
   * python3-pip 패키지를 설치하세요
1. CentOS나 윈도우에서 설치가 안됩니다.
   * 아직 지원 계획이 없습니다
1. 어디에 설치되나요?
   * root 사용자로 설치할 경우 기본 경로는 /root/yona-latest 입니다. 이 경로는 설치할 때 자유롭게 바꿀 수 있습니다.
1. 시스템 데몬 등록 기능은 없나요?
   * 1.0 만드느라 지쳐서 향후 개발 예정입니다.
1. 이거 만든 인간 얼굴이 보고 싶습니다.
   * 대학원에서 데이터베이스 공부하느라 바쁩니다. 찾지 마세요.
1. 업데이트 계획이 있긴 한가요?
   * 업데이트 계획 없는 프로그램은 안 만듭니다.
