## MapleStory Wealth Acquisition Timer - 메이플 재획 타이머

대충짠거 치고는 생각보다 잘 작동함 ww   

### nitial Interface
![img](./interface.png)

### Usage
1. 시작 / Start
2. 원하는 알람단위 체크 ( 도중에 체크/해제 가능 ) / Check the box you want to alarm
3. 체크된 단위마다 10초간 알람 / Starting alarm on checked time for 10s   
[ Angelic Buster Lyric : Star Bubble https://www.youtube.com/watch?v=ixww1OHztbs / SpotLight ]   
[ Town BGM : https://maplestory.nexon.com/Media/Music ]

### Build
1. ANACONDA.NAVIGATOR CMD.exe Prompt 0.1.1
2. Python 3.9.12 (main, Apr  4 2022, 05:22:27) [MSC v.1916 64 bit (AMD64)]
3. pyinstaller 5.1 ( pip install pyinstaller - Require PATH set & Kernel Reboot )
4. Build : pyinstaller -w -F --icon="resources/potion.ico" --add-data="resources/*;." wealth_acquisition_timer.py   
[ if you debugging without build, need to modify sound and ico path in source code resources/~ or copy them same directory (.py file) ] 
5. EXE file is in dist
6. you can clear build, dist, *.spec file
