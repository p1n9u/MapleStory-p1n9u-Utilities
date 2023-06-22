# 메이플스토리 재획 타이머

## MapleStory Wealth Acquisition Timer

New Version Release : 2023-06-22

Download EXE file link : https://www.dropbox.com/scl/fi/m5a2o96nzlxa6zjddodgy/_230622.zip?dl=0&rlkey=dm4tbqlbrz6t8qp0nhdwmdeso  
[ 다운받고 압축풀고 사용. 글자 밀림 현상 수정을 원하면 폰트 설치. ]  
[ 테스트 인원 : 3명 (굉구, 냉동참미, 사시) 정상 작동 ]  
[ 1분-설치형 루시드 소울도 있긴함.. 추가하기 귀찮 ]

### Initial Interface

![img](interface_img/i_interface.png)

### Running Interface

![img](interface_img/r_interface.png)

### Usage

1. Download EXE file from Link
2. Extract Zip file
    - exe file
    - google fonts
3. install google fonts ( Recommanded )
    - Roboto : https://fonts.google.com/specimen/Roboto
    - Noto Sans Korean : https://fonts.google.com/noto/specimen/Noto+Sans+KR

### Dev

1. PyCharm Community Edition 2022.3.2
2. Python 3.11.0 (main, Oct 24 2022, 18:26:48) [MSC v.1933 64 bit (AMD64)] on win32
3. pyinstaller 5.8.0
4. PyQt5 5.15.9 ( include designer for UI )

### Build

1. Build : pyinstaller --clean --onefile --noconsole --icon="resources/icon/potion.ico" --add-data="resources/\*;." -n RiceHarvester main.py

    - Use Window PowerShell ( Vanilla is better than Anaconda for file size )

2. modify RiceHarvester.spec file

    datas=[('resources/wav/*', './resources/wav'),
    ('resources/ui/*', './resources/ui'),
    ('resources/icon/*', './resources/icon'),
    ('resources/img/*', './resources/img')
    ],

3. pyinstall .\RiceHarvester.spec

### Music Reference

1. [ Angelic Buster Lyric : Star Bubble https://www.youtube.com/watch?v=ixww1OHztbs / SpotLight ]
2. [ Town BGM : https://maplestory.nexon.com/Media/Music ]
3. [ https://downloads.khinsider.com/game-soundtracks/album/maplestory-music ]
