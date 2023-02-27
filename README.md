# 메이플스토리 재획 타이머

## MapleStory Wealth Acquisition Timer

New Version Release : 2023-02-24

Download EXE file link : https://www.dropbox.com/s/7xij2sq9wdvnvpf/%EC%9E%AC%ED%9A%8D%ED%83%80%EC%9D%B4%EB%A8%B8.zip?dl=0

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
