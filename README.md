# 메이플스토리 재획 타이머 (굉구 유틸리티)

## MapleStory Wealth Acquisition Timer (p1n9u utilites)

New Version Release : 2024-01-24

### Download

- v3.0.1
- [Blog](https://p1n9u.com) Not LTS Version in Blog
- [Dropbox](https://www.dropbox.com/scl/fi/o3dsqfcbhxc4zwenzq32v/_230622-2.zip?dl=0&rlkey=b10lnhk4julwkf63ju8o58w88) : LTS Version
    - MSp1n9utils.exe: 실행 파일
    - MaplestoryFont_TTF: 메이플스토리 폰트, 설치 권장
    - log: 프로그램 에러로그 기록
    - nexon_api_key: 자신의 넥슨 오픈 API키 저장
    - 매뉴얼

### Version

- v3.0.1-240125 : LTS, Testing.. Distribution not supported
    - 에러 로깅 기능 추가
    - 화면 상단 고정 기능 추가
- v3.0.0-240124
    - update feature
        1. v2: 재획타이머 개선
        2. 보스타이머 추가: 칼로스 + 웹/미디어
        3. 캐릭터검색 추가: 넥슨 OPEN API
        4. 웹사이트 와드 추가: 웹/미디어
        5. 카피라이트 추가: Licenses
- v2.0.2-230622
    - 농기구 멘트 가독성 패치
- v2.0.1-230622
    - 시간밀림현상 수정
- v2.0.0-230622
    - update feature
        1. 메인 스킬 UI 분리
        2. 경뿌 타이머 추가
        3. 폴프 타이머 추가
        4. 준비물 체크박스 추가
- v1.0.0-beta : 2023-02-24
- v0.0.0-alpha : 2022-06-10


### Interface


### Dev

1. Python 3.12.0
2. pyinstaller 6.3.0
3. PyQt5 designer 5.14.1 (install by pip, exec command: $ designer)


### Build

1. Build : pyinstaller --clean --onefile --noconsole --icon="resources/icon/favicon.ico" --add-data="resources/*;." -n MSp1n9utils App.py

    - **Use Windows PowerShell**
        - [reference](https://flytrap.tistory.com/entry/pyinstaller-%EC%9A%A9%EB%9F%89-%EC%A4%84%EC%9D%B4%EB%8A%94-%EB%B0%A9%EB%B2%95-230MB-36MB)

2. modify RiceHarvester.spec file

    datas=[('resources/snd/', './resources/snd'), ('resources/ui/', './resources/ui'), ('resources/icon/', './resources/icon'), ('resources/img/', './resources/img')],

3. pyinstaller .\MSp1n9utils.spec
