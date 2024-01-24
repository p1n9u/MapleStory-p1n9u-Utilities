# 메이플스토리 재획 타이머 (굉구 유틸리티)

## MapleStory Wealth Acquisition Timer (p1n9u utilities)

New Version Release : 2024-01-24

### Download

- 링크 (최신 버전이 아님)
- [Blog](https://p1n9u.com/projects/2022-06-10-mapleStory-wealth-acquisition-timer/)
- [Dropbox](https://www.dropbox.com/scl/fi/o3dsqfcbhxc4zwenzq32v/_230622-2.zip?dl=0&rlkey=b10lnhk4julwkf63ju8o58w88)  
    - exe file  
    - 다운받고 압축풀고 사용. 글자 밀림 현상 수정을 원하면 폰트 설치.  

### Version

- v3.0.0-240124 : Latest, Need Test
- v2.0.2-230622 : ZIP FILE(재획타이머_230622-2)
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
3. PyQt5 designer 5.14.1 (install by pip, command: $designer)


### Build

1. Build : installer --clean --onefile --noconsole --icon="resources/icon/favicon.ico" --add-data="resources/*;." -n MSp1n9utils App.py

    - **Use Windows PowerShell**
    - [Reference](https://flytrap.tistory.com/entry/pyinstaller-%EC%9A%A9%EB%9F%89-%EC%A4%84%EC%9D%B4%EB%8A%94-%EB%B0%A9%EB%B2%95-230MB-36MB)

2. modify RiceHarvester.spec file

    datas=[('resources/snd/', './resources/snd'), ('resources/ui/', './resources/ui'), ('resources/icon/', './resources/icon'), ('resources/img/', './resources/img')],

3. pyinstaller .\MSp1n9utils.spec
