import sys
import requests
import heapq
import random
import os
import sys
import time
import math
import winsound
import logging
import traceback

from PyQt5.QtWidgets import *
from PyQt5 import uic
from io import BytesIO
from PIL import Image
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtCore import QDateTime, Qt
from PyQt5.QtCore import QTimer

# NOTSET, DEBUG, INFO, ERROR, CRITICAL
logging.basicConfig(filename='./log/MSp1n9util_ERROR.log', level=logging.ERROR)

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def make_link_label_txt(link, tag):
    llt = '<a href="' + link + '">' + tag + '</a>'
    return llt

def is_int_number(val):
    int_num_flag = True
    try:
        num = int(val)
        if (math.isnan(num)):
            int_num_flag = False
        else:
            if (num >= 10 and num <= 7200):
                int_num_flag = True
            else:
                int_num_flag = False
    except:
        int_num_flag = False
    return int_num_flag


form = resource_path("resources/ui/MSp1n9ui.ui")
form_class = uic.loadUiType(form)[0]

class WindowClass(QMainWindow, form_class):
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(resource_path("resources/icon/favicon.ico")))
        self.datetime = QDateTime.currentDateTime()
        self.lb_livetime.setText(self.datetime.toString('hh:mm:ss - yy년 MM월 dd일'))
        self.livetime_timer = QTimer(self)
        self.livetime_timer.setInterval(1000)
        self.livetime_timer.timeout.connect(self.display_livetime)
        self.livetime_timer.start()


        self.setFixedSize(1600, 900)
        self.cb_prog_tab_hide.stateChanged.connect(self.ui_checbox_changed)
        self.cb_prog_mini.stateChanged.connect(self.ui_checbox_changed)
        self.cb_prog_on_top.stateChanged.connect(self.ui_checbox_changed)

        self.wa_wav_list = [
            "p",
            resource_path("resources/snd/wa_skill1.wav"), #1 short
            resource_path("resources/snd/wa_skill2.wav"), #2
            resource_path("resources/snd/wa_skill3.wav"), #3
            resource_path("resources/snd/wa_skill4.wav"), #4
            resource_path("resources/snd/wa_skill5.wav"), #5
            resource_path("resources/snd/wa_skill6.wav"), #6
            resource_path("resources/snd/wa_10m.wav"), #7
            resource_path("resources/snd/wa_20m.wav"), #8
            resource_path("resources/snd/wa_1h.wav"), #9
            resource_path("resources/snd/wa_2h.wav"), #10
            resource_path("resources/snd/wa_30m.wav"), #11 long
            resource_path("resources/snd/wa_15m.wav"), #12
            resource_path("resources/snd/wa_ealarm.wav"), #13
            resource_path("resources/snd/wa_palarm.wav"), #14
            resource_path("resources/snd/wa_100s.wav"), #15
        ]

        # tab_boss_kalos_wav_list
        self.b_kalos_wav_list = [
            "p",
            resource_path("resources/snd/boss_kalos_sa10.wav"), #1
            resource_path("resources/snd/boss_kalos_sa5.wav"), #2
            resource_path("resources/snd/boss_kalos_breath.wav"), #3
            resource_path("resources/snd/boss_kalos_right.wav"), #4
            resource_path("resources/snd/boss_kalos_left.wav"), #5
            resource_path("resources/snd/boss_kalos_if10.wav"), #6
            resource_path("resources/snd/boss_kalos_if5.wav"), #7
        ]

        # tab_watimer
        self.wa_alarm_heap = []

        self.txt_wa_s1.returnPressed.connect(self.clicked_btn_wa_s1)
        self.btn_wa_s1.clicked.connect(self.clicked_btn_wa_s1)
        self.cb_wa_s1.stateChanged.connect(self.skill_checkbox_changed)
        self.txt_wa_s2.returnPressed.connect(self.clicked_btn_wa_s2)
        self.btn_wa_s2.clicked.connect(self.clicked_btn_wa_s2)
        self.cb_wa_s2.stateChanged.connect(self.skill_checkbox_changed)
        self.txt_wa_s3.returnPressed.connect(self.clicked_btn_wa_s3)
        self.btn_wa_s3.clicked.connect(self.clicked_btn_wa_s3)
        self.cb_wa_s3.stateChanged.connect(self.skill_checkbox_changed)
        self.txt_wa_s4.returnPressed.connect(self.clicked_btn_wa_s4)
        self.btn_wa_s4.clicked.connect(self.clicked_btn_wa_s4)
        self.cb_wa_s4.stateChanged.connect(self.skill_checkbox_changed)
        self.txt_wa_s5.returnPressed.connect(self.clicked_btn_wa_s5)
        self.btn_wa_s5.clicked.connect(self.clicked_btn_wa_s5)
        self.cb_wa_s5.stateChanged.connect(self.skill_checkbox_changed)
        self.txt_wa_s6.returnPressed.connect(self.clicked_btn_wa_s6)
        self.btn_wa_s6.clicked.connect(self.clicked_btn_wa_s6)
        self.cb_wa_s6.stateChanged.connect(self.skill_checkbox_changed)

        self.wa_alarm_timer = QTimer(self)
        self.wa_alarm_timer.setInterval(1000)
        self.wa_alarm_timer.timeout.connect(self.activate_wa_alarm_timer)
        
        self.wa_timer = QTimer(self)
        self.wa_timer.setInterval(1000)
        self.wa_timer.timeout.connect(self.activate_wa_timer)
        self.btn_wa_start.clicked.connect(self.clicked_btn_wa_start)
        self.btn_wa_stop.clicked.connect(self.clicked_btn_wa_stop)
        self.wa_cnt = 0
        self.wa_pb_val = 0
        self.wa_total = 0
        self.wa_ss = 0
        self.wa_mm = 0
        self.wa_hh = 0
        self.wa_s1_ss = -1
        self.wa_s2_ss = -1
        self.wa_s3_ss = -1
        self.wa_s4_ss = -1
        self.wa_s5_ss = -1
        self.wa_s6_ss = -1

        self.wa_etimer = QTimer(self)
        self.wa_etimer.setInterval(1000)
        self.wa_etimer.timeout.connect(self.activate_wa_etimer)
        self.btn_wa_estart.clicked.connect(self.clicked_btn_wa_estart)
        self.btn_wa_estop.clicked.connect(self.clicked_btn_wa_estop)
        self.btn_wa_eclear.clicked.connect(self.clicked_btn_wa_eclear)
        self.wa_ecnt = 0
        self.wa_etotal = 0
        self.wa_ess = 0
        self.wa_emm = 0
        self.wa_ehh = 0

        self.wa_ptimer = QTimer(self)
        self.wa_ptimer.setInterval(1000)
        self.wa_ptimer.timeout.connect(self.activate_wa_ptimer)
        self.btn_wa_pstart.clicked.connect(self.clicked_btn_wa_pstart)
        self.btn_wa_pstop.clicked.connect(self.clicked_btn_wa_pstop)
        self.btn_wa_preset.clicked.connect(self.clicked_btn_wa_preset)
        self.btn_wa_ppm.clicked.connect(self.clicked_btn_btn_wa_ppm)
        self.btn_wa_epm.clicked.connect(self.clicked_btn_btn_wa_epm)
        self.btn_wa_fwm.clicked.connect(self.clicked_btn_btn_wa_fwm)
        self.btn_wa_ppp.clicked.connect(self.clicked_btn_btn_wa_ppp)
        self.btn_wa_epp.clicked.connect(self.clicked_btn_btn_wa_epp)
        self.btn_wa_fwp.clicked.connect(self.clicked_btn_btn_wa_fwp)

        self.wa_pss = 90
        self.wa_pflag = 1
        self.wa_pp_cnt = 15
        self.wa_ep_cnt = 5
        self.wa_fw_cnt = 5


        # tab_search
        api_key_file = open('./nexon_api_key/api_key_lts.txt', 'r')
        api_key_data = api_key_file.read()
        self.keys = api_key_data
        self.headers = {
            "x-nxopen-api-key": str(self.keys)
        }
        self.lb_api_key.setText('API키: ' + self.keys)
        api_key_file.close()

        self.txt_api_key.returnPressed.connect(self.clicked_btn_api_key_input)
        self.btn_api_key_input.clicked.connect(self.clicked_btn_api_key_input)

        s_arcane_img = QPixmap(resource_path("resources/img/stat_arcane.png"))
        self.lb_s_arcane.setPixmap(s_arcane_img)
        s_authentic_img = QPixmap(resource_path("resources/img/stat_authentic.png"))
        self.lb_s_authentic.setPixmap(s_authentic_img)
        s_drop_img = QPixmap(resource_path("resources/img/stat_drop.png"))
        self.lb_s_drop.setPixmap(s_drop_img)
        s_exp_img = QPixmap(resource_path("resources/img/stat_exp.png"))
        self.lb_s_exp.setPixmap(s_exp_img)
        s_meso_img = QPixmap(resource_path("resources/img/stat_meso.png"))
        self.lb_s_meso.setPixmap(s_meso_img)
        s_normd_img = QPixmap(resource_path("resources/img/stat_normd.png"))
        self.lb_s_normd.setPixmap(s_normd_img)
        s_starforce_img = QPixmap(resource_path("resources/img/stat_starforce.png"))
        self.lb_s_starforce.setPixmap(s_starforce_img)

        self.txt_c_name.returnPressed.connect(self.clicked_btn_c_search)
        self.btn_c_search.clicked.connect(self.clicked_btn_c_search)

        self.lb_api_guide.setText(make_link_label_txt('https://github.com/p1n9u/MapleStory-p1n9u-Utils/blob/main/nexon_api_key_guide/README.md', '발급방법'))
        self.lb_api_guide.setOpenExternalLinks(True)

        # tab_info_ward
        self.lb_l_ghome.setText(make_link_label_txt('https://maplestory.nexon.com/Home/Main', '메이플 공홈'))
        self.lb_l_ghome.setOpenExternalLinks(True)
        self.lb_l_gyt.setText(make_link_label_txt('https://www.youtube.com/@MapleStoryKR', '메이플 유튜브'))
        self.lb_l_gyt.setOpenExternalLinks(True)
        self.lb_l_dorosi.setText(make_link_label_txt('https://m.inven.co.kr/board/maple/2314?stype=nickname&svalue=%EB%A7%88%EB%B9%A1%EB%8F%84%EB%A1%9C%EC%8B%9C', '인벤m 마빡도로시'))
        self.lb_l_dorosi.setOpenExternalLinks(True)
        self.lb_l_malgum.setText(make_link_label_txt('https://www.youtube.com/@Malgum.', '맑음 유튜브'))
        self.lb_l_malgum.setOpenExternalLinks(True)
        self.lb_l_seollal.setText(make_link_label_txt('https://seollal.tistory.com/category/%EB%A9%94%EC%9D%B4%ED%94%8C%EC%8A%A4%ED%86%A0%EB%A6%AC', '한설날 티스토리 블로그'))
        self.lb_l_seollal.setOpenExternalLinks(True)
        self.lb_l_maplegg.setText(make_link_label_txt('https://maple.gg/', '메이플 지지 - 종합 통계'))
        self.lb_l_maplegg.setOpenExternalLinks(True)
        self.lb_l_mscouter.setText(make_link_label_txt('https://maplescouter.com/', '환산 주스탯'))
        self.lb_l_mscouter.setOpenExternalLinks(True)
        self.lb_l_chuchugg.setText(make_link_label_txt('https://chuchu.gg/starforce', '츄츄 지지 - 스타포스 히스토리'))
        self.lb_l_chuchugg.setOpenExternalLinks(True)
        self.lb_l_msupport.setText(make_link_label_txt('https://maple.support/', '메이플 서포트 - 큐브 히스토리'))
        self.lb_l_msupport.setOpenExternalLinks(True)
        self.lb_l_mavg.setText(make_link_label_txt('http://mapleaverage.dothome.co.kr/', '메이플 평균'))
        self.lb_l_mavg.setOpenExternalLinks(True)
        self.lb_l_guildreal.setText(make_link_label_txt('https://guildbon.github.io/', '길드원 본캐 찾기'))
        self.lb_l_guildreal.setOpenExternalLinks(True)
        self.lb_l_guildatk.setText(make_link_label_txt('https://www.yegangs.com/guildbon/', '길드원 전투력 스카우터'))
        self.lb_l_guildatk.setOpenExternalLinks(True)
        self.lb_l_nicklog.setText(make_link_label_txt('https://mapleagency.kr/', '닉네임 변경 로그'))
        self.lb_l_nicklog.setOpenExternalLinks(True)
        self.lb_l_badtradelog.setText(make_link_label_txt('https://faladine.com/main', '사기꾼 로그'))
        self.lb_l_badtradelog.setOpenExternalLinks(True)
        self.lb_l_unioncal.setText(make_link_label_txt('https://xenogents.github.io/LegionSolver/', '유니온 배치 계산기'))
        self.lb_l_unioncal.setOpenExternalLinks(True)
        self.lb_l_corecal.setText(make_link_label_txt('https://shalchoong.tistory.com/80', '5차 중첩 코강 계산기'))
        self.lb_l_corecal.setOpenExternalLinks(True)
        self.lb_l_bstonecal.setText(make_link_label_txt('https://boss.lastchan.kr/', '주보 결정 계산기'))
        self.lb_l_bstonecal.setOpenExternalLinks(True)
        self.lb_l_hmesocal.setText(make_link_label_txt('https://mapleroad.kr/utils/poa', '사냥 메소 계산기'))
        self.lb_l_hmesocal.setOpenExternalLinks(True)
        self.lb_l_heffcal.setText(make_link_label_txt('https://betweenmoon.github.io/maple_hyper/HTML/calcLevelUp.html', '사냥터 효율 계산기'))
        self.lb_l_heffcal.setOpenExternalLinks(True)
        self.lb_l_lpotioncal.setText(make_link_label_txt('https://maple.gazua.in/exp', '성장의 비약 계산기'))
        self.lb_l_lpotioncal.setOpenExternalLinks(True)
        self.lb_l_srangecal.setText(make_link_label_txt('https://icepeng.github.io/maple-calc/skill', '스킬 범위 계산기'))
        self.lb_l_srangecal.setOpenExternalLinks(True)
        self.lb_l_speceffcal.setText(make_link_label_txt('https://maplestats.com/home', '스펙 투자 효율 계산기'))
        self.lb_l_speceffcal.setOpenExternalLinks(True)
        self.lb_l_symhexcal.setText(make_link_label_txt('https://maple-util.web.app/hexa-calculator', '헥사스킬/심볼 계산기'))
        self.lb_l_symhexcal.setOpenExternalLinks(True)
        self.lb_l_artical.setText(make_link_label_txt('https://www.inven.co.kr/board/maple/2304/37006', '아티팩트 레벨업 계산기'))
        self.lb_l_artical.setOpenExternalLinks(True)
        self.lb_l_ucoincal.setText(make_link_label_txt('https://gubbib.github.io/MapleUnionCoin/', '유니온 코인 계산기'))
        self.lb_l_ucoincal.setOpenExternalLinks(True)
        self.lb_l_hstatcal.setText(make_link_label_txt('https://mapleroad.kr/utils/hstat', '하이퍼 스탯 계산기'))
        self.lb_l_hstatcal.setOpenExternalLinks(True)
        self.lb_l_surocal.setText(make_link_label_txt('https://141.kr/suro', '수로-무릉 환산기'))
        self.lb_l_surocal.setOpenExternalLinks(True)
        self.lb_l_problist.setText(make_link_label_txt('https://maplestory.nexon.com/Guide/CashShop/Probability/RoyalStyle', '메이플 공홈 - 가이드(확률)'))
        self.lb_l_problist.setOpenExternalLinks(True)
        self.lb_l_mmarket.setText(make_link_label_txt('https://xn--hz2b1j494a9mhnwh.com/', '메이플 경매장 - 메이플마켓.com'))
        self.lb_l_mmarket.setOpenExternalLinks(True)
        self.lb_l_mstime.setText(make_link_label_txt('https://time.navyism.com/?host=maplestory.nexon.com', '메이플 서버 시간 - 네이비즘'))
        self.lb_l_mstime.setOpenExternalLinks(True)
        self.lb_l_artiopti.setText(make_link_label_txt('https://m.inven.co.kr/board/maple/2304/36811', '아티팩트 최적 포인트 분배(정배)'))
        self.lb_l_artiopti.setOpenExternalLinks(True)
        self.lb_l_seedhelp.setText(make_link_label_txt('https://mapleutils.com/ko/seed/22', '더 시드 도우미'))
        self.lb_l_seedhelp.setOpenExternalLinks(True)
        self.lb_l_mcollhelp.setText(make_link_label_txt('https://www.moncol.kr/', '몬컬 도우미'))
        self.lb_l_mcollhelp.setOpenExternalLinks(True)
        self.lb_l_cweekhelp.setText(make_link_label_txt('https://maple.gg/info/muto', '츄츄 주간 도우미'))
        self.lb_l_cweekhelp.setOpenExternalLinks(True)
        self.lb_l_rweekhelp.setText(make_link_label_txt('https://in-fo.github.io/midnight-chaser-helper/', '레헬른 주간 도우미'))
        self.lb_l_rweekhelp.setOpenExternalLinks(True)
        self.lb_l_eweekhelp.setText(make_link_label_txt('https://mapleroad.kr/utils/esfera', '에스페라 주간 도우미'))
        self.lb_l_eweekhelp.setOpenExternalLinks(True)
        self.lb_l_puzzlemhelp.setText(make_link_label_txt('https://qr96.github.io/Puzzle-Master/', '퍼즐 마스터 도우미'))
        self.lb_l_puzzlemhelp.setOpenExternalLinks(True)
        self.lb_l_aopsimul.setText(make_link_label_txt('https://bnbmupload.github.io/maplerebirthflame/', '추옵 시뮬레이터'))
        self.lb_l_aopsimul.setOpenExternalLinks(True)
        self.lb_l_starsimul.setText(make_link_label_txt('https://mesu.live/sim/starforce', '스타포스 시뮬레이터'))
        self.lb_l_starsimul.setOpenExternalLinks(True)
        self.lb_l_cubesimul.setText(make_link_label_txt('https://cubemesu.co/', '큐브 시뮬레이터'))
        self.lb_l_cubesimul.setOpenExternalLinks(True)
        self.lb_l_hexasimul.setText(make_link_label_txt('https://memoday.github.io/hexaStat_Simulator/', '헥사스탯 시뮬레이터'))
        self.lb_l_hexasimul.setOpenExternalLinks(True)
        self.lb_l_gatchasimul.setText(make_link_label_txt('https://ganjang-chichen.github.io/BlackCow_Defender/', '가챠 시뮬레이터'))
        self.lb_l_gatchasimul.setOpenExternalLinks(True)
        self.lb_l_royalsimul.setText(make_link_label_txt('https://maple.gazua.in/', '로얄 시뮬레이터'))
        self.lb_l_royalsimul.setOpenExternalLinks(True)
        self.lb_l_dmgssimul.setText(make_link_label_txt('https://0407chan.github.io/maple-demage-skin-simulator/', '뎀스 시뮬레이터'))
        self.lb_l_dmgssimul.setOpenExternalLinks(True)
        self.lb_l_coordisimul.setText(make_link_label_txt('https://maple.gazua.in/coordi', '코디 시뮬레이터'))
        self.lb_l_coordisimul.setOpenExternalLinks(True)
        self.lb_l_lvsimul.setText(make_link_label_txt('https://ksw04052.github.io/levelsim/', '레벨 시뮬레이터(old)'))
        self.lb_l_lvsimul.setOpenExternalLinks(True)
        self.lb_l_itemsimul.setText(make_link_label_txt('https://itemsim.pages.dev/', '아이템 시뮬레이터'))
        self.lb_l_itemsimul.setOpenExternalLinks(True)

        # tab_copyrights
        cr_nexon_logo_img = QPixmap(resource_path("resources/img/nexon_logo.png"))
        self.lb_cr_nexon_logo.setPixmap(cr_nexon_logo_img)
        self.lb_cr_api.setText(make_link_label_txt('https://openapi.nexon.com/support/terms/', 'Data based on NEXON Open API'))
        self.lb_cr_api.setOpenExternalLinks(True)
        
        cr_server_logo_img = QPixmap(resource_path("resources/img/server_logo.png"))
        self.lb_cr_thx_serverimg.setPixmap(cr_server_logo_img)
        cr_git_logo_img = QPixmap(resource_path("resources/img/git_logo.png"))
        self.lb_cr_dev_gitimg.setPixmap(cr_git_logo_img)
        cr_guild_logo_img = QPixmap(resource_path("resources/img/guild_logo.png"))
        self.lb_cr_thx_guildimg.setPixmap(cr_guild_logo_img)
        cr_lic_img = QPixmap(resource_path("resources/img/repo_license.png"))
        self.lb_cr_licimg.setPixmap(cr_lic_img)
        boss_kalos_img = QPixmap(resource_path("resources/img/easy_evade.png"))
        self.lb_boss_kalos_img.setPixmap(boss_kalos_img)

        self.lb_cr_font.setText(make_link_label_txt('https://maplestory.nexon.com/Media/Font', 'Font'))
        self.lb_cr_font.setOpenExternalLinks(True)
        self.lb_cr_music1.setText(make_link_label_txt('https://www.youtube.com/watch?v=ixww1OHztbs', 'Music1'))
        self.lb_cr_music1.setOpenExternalLinks(True)
        self.lb_cr_music2.setText(make_link_label_txt('https://maplestory.nexon.com/Media/Music', 'Music2'))
        self.lb_cr_music2.setOpenExternalLinks(True)
        self.lb_cr_music3.setText(make_link_label_txt('https://downloads.khinsider.com/game-soundtracks/album/maplestory-music', 'Music3'))
        self.lb_cr_music3.setOpenExternalLinks(True)
        self.lb_cr_tts.setText(make_link_label_txt('https://xn--yq5bk9r.com/blog/text-speech-download', 'TTS'))
        self.lb_cr_tts.setOpenExternalLinks(True)
        self.lb_cr_dev_gitlink.setText(make_link_label_txt('https://github.com/p1n9u/MapleStory-p1n9u-Utils', 'Repo'))
        self.lb_cr_dev_gitlink.setOpenExternalLinks(True)
        self.lb_cr_dune.setText(make_link_label_txt('https://www.inven.co.kr/board/maple/2299/9759968', '듄쌤티콘'))
        self.lb_cr_dune.setOpenExternalLinks(True)

        # tab_boss_web
        self.lb_bw_black.setText(make_link_label_txt('https://ksw04052.github.io/blackmage/', '검은 마법사'))
        self.lb_bw_black.setOpenExternalLinks(True)
        self.lb_bw_jin1.setText(make_link_label_txt('https://jhanoo.github.io/JinHilla/', '진힐라 (화면공유 O)'))
        self.lb_bw_jin1.setOpenExternalLinks(True)
        self.lb_bw_jin2.setText(make_link_label_txt('https://jsfiddle.net/isaac917/6zdacrox/9/show', '진힐라 (화면공유 X)'))
        self.lb_bw_jin2.setOpenExternalLinks(True)
        self.lb_bw_kal1.setText(make_link_label_txt('https://hhykim.github.io/KalosTimer/', '칼로스 (화면공유 O)'))
        self.lb_bw_kal1.setOpenExternalLinks(True)
        self.lb_bw_kal2.setText(make_link_label_txt('http://kalos.dothome.co.kr/', '칼로스 (화면공유 X)'))
        self.lb_bw_kal2.setOpenExternalLinks(True)


        # tab_boss_kalos
        self.boss_kalos_alarm_heap = []

        # phase: 1
        self.boss_kalos_previous_phase = 0
        self.boss_kalos_current_phase = 0
        self.is_boss_kalos_changed_phase = 0

        self.btn_kalos_start.clicked.connect(self.clicked_btn_kalos_start)
        self.btn_kalos_reset.clicked.connect(self.clicked_btn_kalos_reset)
        self.btn_kalos_stop.clicked.connect(self.clicked_btn_kalos_stop)

        self.boss_kalos_main_timer = QTimer(self)
        self.boss_kalos_main_timer.setInterval(1000)
        self.boss_kalos_main_timer.timeout.connect(self.activate_boss_kalos_main_timer)

        self.boss_kalos_salvo_timer = QTimer(self)
        self.boss_kalos_salvo_timer.setInterval(1000)
        self.boss_kalos_salvo_timer.timeout.connect(self.activate_boss_kalos_salvo_timer)
        self.boss_kalos_salvo_sec = 0
        self.btn_kalos_salvo.clicked.connect(self.clicked_btn_kalos_salvo)
        self.btn_kalos_p50s.clicked.connect(self.clicked_btn_kalos_p50s)
        self.btn_kalos_p20s.clicked.connect(self.clicked_btn_kalos_p20s)
        self.btn_kalos_p10s.clicked.connect(self.clicked_btn_kalos_p10s)
        self.btn_kalos_p4s.clicked.connect(self.clicked_btn_kalos_p4s)
        self.btn_kalos_m50s.clicked.connect(self.clicked_btn_kalos_m50s)
        self.btn_kalos_m20s.clicked.connect(self.clicked_btn_kalos_m20s)
        self.btn_kalos_m10s.clicked.connect(self.clicked_btn_kalos_m10s)
        self.btn_kalos_m4s.clicked.connect(self.clicked_btn_kalos_m4s)

        self.boss_kalos_if_timer = QTimer(self)
        self.boss_kalos_if_timer.setInterval(1000)
        self.boss_kalos_if_timer.timeout.connect(self.activate_boss_kalos_if_timer)
        self.boss_kalos_if_sec = 0
        self.btn_kalos_if.clicked.connect(self.clicked_btn_kalos_if)

        self.boss_kalos_right_timer = QTimer(self)
        self.boss_kalos_right_timer.setInterval(1000)
        self.boss_kalos_right_timer.timeout.connect(self.activate_boss_kalos_right_timer)
        self.btn_kalos_right_on.clicked.connect(self.clicked_btn_right_on)
        self.btn_kalos_right_off.clicked.connect(self.clicked_btn_right_off)
        self.boss_kalos_right_sec = 0

        self.boss_kalos_left_timer = QTimer(self)
        self.boss_kalos_left_timer.setInterval(1000)
        self.boss_kalos_left_timer.timeout.connect(self.activate_boss_kalos_left_timer)
        self.btn_kalos_left_on.clicked.connect(self.clicked_btn_left_on)
        self.btn_kalos_left_off.clicked.connect(self.clicked_btn_left_off)
        self.boss_kalos_left_sec = 0

        self.boss_kalos_breath_timer = QTimer(self)
        self.boss_kalos_breath_timer.setInterval(1000)
        self.boss_kalos_breath_timer.timeout.connect(self.activate_boss_kalos_breath_timer)
        self.btn_kalos_breath_on.clicked.connect(self.clicked_btn_breath_on)
        self.btn_kalos_breath_off.clicked.connect(self.clicked_btn_breath_off)
        self.boss_kalos_breath_sec = 1557
        self.btn_kalos_phase2_1.clicked.connect(self.clicked_btn_kalos_phase2_1)
        self.btn_kalos_phase2_2.clicked.connect(self.clicked_btn_kalos_phase2_2)
        self.btn_kalos_phase2_3.clicked.connect(self.clicked_btn_kalos_phase2_3)


####################################################################################################################################################################
# ui main functions
        
    def display_livetime(self):
        datetime = QDateTime.currentDateTime()
        self.lb_livetime.setText(datetime.toString('hh:mm:ss - yy년 MM월 dd일'))
        
    def ui_checbox_changed(self):
        if (self.cb_prog_tab_hide.isChecked() and self.cb_prog_mini.isChecked()):
            self.setFixedSize(640, 100)
        elif (self.cb_prog_tab_hide.isChecked()):
            self.setFixedSize(640, 100)
        elif (self.cb_prog_mini.isChecked()):
            self.setFixedSize(640, 900)
        else:
            self.setFixedSize(1600, 900)
        if (self.cb_prog_on_top.isChecked()):
            self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
            self.show()
        else:
            self.setWindowFlag(Qt.WindowStaysOnTopHint, False)
            self.show()


####################################################################################################################################################################
# tab_watimer functions

    # wa functions
    def skill_checkbox_changed(self):
        if ((self.cb_wa_s1.isChecked()) and (not is_int_number(self.wa_s1_ss))):
            self.cb_wa_s1.setCheckState(0)
            log_num = str(random.randrange(1000, 9999))
            self.txt_wa_log.setPlainText('[스킬1]: 올바른 값 설정 필요 - ' + log_num)
        if ((self.cb_wa_s2.isChecked()) and (not is_int_number(self.wa_s2_ss))):
            self.cb_wa_s2.setCheckState(0)
            log_num = str(random.randrange(1000, 9999))
            self.txt_wa_log.setPlainText('[스킬2]: 올바른 값 설정 필요 - ' + log_num)
        if ((self.cb_wa_s3.isChecked()) and (not is_int_number(self.wa_s3_ss))):
            self.cb_wa_s3.setCheckState(0)
            log_num = str(random.randrange(1000, 9999))
            self.txt_wa_log.setPlainText('[스킬3]: 올바른 값 설정 필요 - ' + log_num)
        if ((self.cb_wa_s4.isChecked()) and (not is_int_number(self.wa_s4_ss))):
            self.cb_wa_s4.setCheckState(0)
            log_num = str(random.randrange(1000, 9999))
            self.txt_wa_log.setPlainText('[스킬4]: 올바른 값 설정 필요 - ' + log_num)
        if ((self.cb_wa_s5.isChecked()) and (not is_int_number(self.wa_s5_ss))):
            self.cb_wa_s5.setCheckState(0)
            log_num = str(random.randrange(1000, 9999))
            self.txt_wa_log.setPlainText('[스킬5]: 올바른 값 설정 필요 - ' + log_num)
        if ((self.cb_wa_s6.isChecked()) and (not is_int_number(self.wa_s6_ss))):
            self.cb_wa_s6.setCheckState(0)
            log_num = str(random.randrange(1000, 9999))
            self.txt_wa_log.setPlainText('[스킬6]: 올바른 값 설정 필요 - ' + log_num)
    
    # wa timer
    def clicked_btn_wa_start(self):
        self.wa_stop_progress()
        self.wa_alarm_timer.start()
        self.wa_timer.start()
        self.cb_prog_mini.setCheckState(2)
        
        log_num = str(random.randrange(1000, 9999))
        self.txt_wa_log.setPlainText('먼치의 삶 체험 시작 - ' + log_num)

    def wa_stop_progress(self):
        self.wa_alarm_heap.clear()
        self.wa_alarm_timer.stop()
        self.wa_timer.stop()
        self.wa_cnt = 0
        self.wa_total = 0
        self.wa_ss = 0
        self.wa_mm = 0
        self.wa_hh = 0
        self.wa_pb_val = 0
        self.pb_wa.setValue(0)
        
    def clicked_btn_wa_stop(self):
        self.cb_prog_mini.setCheckState(0)
        self.wa_stop_progress()
        self.lb_wa_time.setText('0:00:00')
        self.lb_wa_cnt.setText('0')
        log_num = str(random.randrange(1000, 9999))
        self.txt_wa_log.setPlainText('먼치의 삶 체험 종료 - ' + log_num)
        

    def activate_wa_timer(self):
        wa_log_str = ''

        self.wa_total += 1
        self.wa_ss += 1
        self.wa_pb_val += 1
        self.pb_wa.setValue(self.wa_pb_val)

        if (self.wa_total % 7200 == 0):
            self.wa_pb_val = 0
            self.pb_wa.setValue(self.wa_pb_val)

        if (self.wa_ss == 60):
            self.wa_mm += 1
            self.wa_ss = 0

        if (self.wa_mm == 60):
            self.wa_hh += 1
            self.wa_mm = 0

        wa_time_str = "{0}:{1:02}:{2:02}".format(self.wa_hh, self.wa_mm, self.wa_ss)
        self.lb_wa_time.setText(wa_time_str)

        # short
        if (self.cb_wa_s1.isChecked() and ((self.wa_total + 5) % self.wa_s1_ss) == 0):
            heapq.heappush(self.wa_alarm_heap, 1)
            wa_log_str += '스킬1 '
        if (self.cb_wa_s2.isChecked() and ((self.wa_total + 5) % self.wa_s2_ss) == 0):
            heapq.heappush(self.wa_alarm_heap, 2)
            wa_log_str += '스킬2 '
        if (self.cb_wa_s3.isChecked() and ((self.wa_total + 5) % self.wa_s3_ss) == 0):
            heapq.heappush(self.wa_alarm_heap, 3)
            wa_log_str += '스킬3 '
        if (self.cb_wa_s4.isChecked() and ((self.wa_total + 5) % self.wa_s4_ss) == 0):
            heapq.heappush(self.wa_alarm_heap, 4)
            wa_log_str += '스킬4 '
        if (self.cb_wa_s5.isChecked() and ((self.wa_total + 5) % self.wa_s5_ss) == 0):
            heapq.heappush(self.wa_alarm_heap, 5)
            wa_log_str += '스킬5 '
        if (self.cb_wa_s6.isChecked() and ((self.wa_total + 5) % self.wa_s6_ss) == 0):
            heapq.heappush(self.wa_alarm_heap, 6)
            wa_log_str += '스킬6 '
        if (self.cb_wa_10m.isChecked() and ((self.wa_total + 3) % 600) == 0):
            heapq.heappush(self.wa_alarm_heap, 7)
            wa_log_str += '10분 '
        if (self.cb_wa_20m.isChecked() and ((self.wa_total + 3) % 1200) == 0):
            heapq.heappush(self.wa_alarm_heap, 8)
            wa_log_str += '20분 '
        if (self.cb_wa_1h.isChecked() and ((self.wa_total + 3) % 3600) == 0):
            heapq.heappush(self.wa_alarm_heap, 9)
            wa_log_str += '1시간 '
        if (self.cb_wa_2h.isChecked() and ((self.wa_total + 3) % 7200) == 0):
            heapq.heappush(self.wa_alarm_heap, 10)
            wa_log_str += '2시간 '
            self.wa_cnt += 1
            self.lb_wa_cnt.setText(str(self.wa_cnt))
        # long
        if (self.cb_wa_30m.isChecked() and ((self.wa_total + 3) % 1800) == 0):
            heapq.heappush(self.wa_alarm_heap, 11)
            wa_log_str += '30분 '
            if (self.cb_wa_15m.isChecked() and ((self.wa_total + 3) % 900) == 0):
                wa_log_str += '15분 '
            if (self.cb_wa_100s.isChecked() and ((self.wa_total + 3) %100) == 0):
                wa_log_str += '메소! '
        elif (self.cb_wa_15m.isChecked() and ((self.wa_total + 3) % 900) == 0):
            heapq.heappush(self.wa_alarm_heap, 12)
            wa_log_str += '15분 '
            if (self.cb_wa_100s.isChecked() and ((self.wa_total + 3) %100) == 0):
                wa_log_str += '메소! '
        elif (((self.wa_etotal + 60) % 1800) == 0):
            heapq.heappush(self.wa_alarm_heap, 13)
            if (self.cb_wa_100s.isChecked() and ((self.wa_total + 3) %100) == 0):
                wa_log_str += '메소! '
        elif (self.wa_pss == 20 and self.wa_pflag):
            heapq.heappush(self.wa_alarm_heap, 14)
            if (self.cb_wa_100s.isChecked() and ((self.wa_total + 3) %100) == 0):
                wa_log_str += '메소! '
        elif (self.cb_wa_100s.isChecked() and ((self.wa_total + 3) %100) == 0):
            heapq.heappush(self.wa_alarm_heap, 15)
            wa_log_str += '메소! '
            
    # wa alarm timer
    def activate_wa_alarm_timer(self):
        if (len(self.wa_alarm_heap)):
            alarm_num = heapq.heappop(self.wa_alarm_heap)
            winsound.PlaySound(self.wa_wav_list[alarm_num], winsound.SND_ASYNC)

    # wa exp timer
    def clicked_btn_wa_estart(self):
        self.wa_estop_progress()
        self.wa_etimer.start()
        log_num = str(random.randrange(1000, 9999))
        self.lb_wa_ecnt.setText('1')
        self.txt_wa_log.setPlainText('연뿌 타이머 시작 - ' + log_num)

    def wa_estop_progress(self):
        self.wa_etimer.stop()
        self.wa_etotal = 0
        self.wa_ess = 0
        self.wa_emm = 0
        self.wa_ehh = 0
        
    def clicked_btn_wa_estop(self):
        self.wa_estop_progress()
        self.lb_wa_etime.setText('0:00:00')
        self.lb_wa_ecnt.setText('0')
        log_num = str(random.randrange(1000, 9999))
        self.txt_wa_log.setPlainText('연뿌 타이머 종료 - ' + log_num)

    def clicked_btn_wa_eclear(self):
        self.te_ememo.clear()
        log_num = str(random.randrange(1000, 9999))
        self.txt_wa_log.setPlainText('[경뿌]: 메모장 초기화 완료 - ' + log_num)

    def activate_wa_etimer(self):
        self.wa_etotal += 1
        self.wa_ess += 1

        if (self.wa_ess == 60):
            self.wa_emm += 1
            self.wa_ess = 0

        if (self.wa_emm == 60):
            self.wa_ehh += 1
            self.wa_emm = 0

        wa_etime_str = "{0}:{1:02}:{2:02}".format(self.wa_ehh, self.wa_emm, self.wa_ess)
        self.lb_wa_etime.setText(wa_etime_str)

        if (((self.wa_etotal + 60) % 1800) == 0):
            self.wa_ecnt += 1
            self.lb_expcnt_value.setText(str(self.wa_ecnt))

    # wa portal timer
    def clicked_btn_wa_pstart(self):
        self.wa_pstop_progress()
        self.wa_ptimer.start()
        log_num = str(random.randrange(1000, 9999))
        self.txt_wa_log.setPlainText('포탈 타이머 시작 - ' + log_num)

    def wa_pstop_progress(self):
        self.wa_ptimer.stop()
        self.wa_pflag = 1
        self.wa_pss = 90
        self.lb_wa_ptime.setText(str(self.wa_pss))
        self.lb_wa_ptime.setStyleSheet('color: black;')
        
    def clicked_btn_wa_pstop(self):
        self.wa_pstop_progress()
        log_num = str(random.randrange(1000, 9999))
        self.txt_wa_log.setPlainText('포탈 타이머 종료 - ' + log_num)

    def activate_wa_ptimer(self):
        if (self.wa_pflag):
            self.wa_pss -= 1
            self.lb_wa_ptime.setText(str(self.wa_pss))
            if (self.wa_pss == 0):
                self.wa_pflag = 0
                self.lb_wa_ptime.setStyleSheet('color: blue;')
        else:
            self.wa_pss += 1
            self.lb_wa_ptime.setText(str(self.wa_pss))
            if (self.wa_pss == 45):
                
                self.clicked_btn_wa_pstop()

    def clicked_btn_wa_preset(self):
        self.wa_pp_cnt = 15
        self.lb_wa_pp_cnt.setText(str(self.wa_pp_cnt))
        self.wa_ep_cnt = 5
        self.lb_wa_ep_cnt.setText(str(self.wa_ep_cnt))
        self.wa_fw_cnt = 5
        self.lb_wa_fw_cnt.setText(str(self.wa_fw_cnt))
        log_num = str(random.randrange(1000, 9999))
        self.txt_wa_log.setPlainText('[포탈]: 카운트 초기화 완료 - ' + log_num)

    def clicked_btn_btn_wa_ppm(self):
        self.wa_pp_cnt -= 1
        if (self.wa_pp_cnt == 1):
            log_num = str(random.randrange(1000, 9999))
            self.txt_wa_log.setPlainText('다음 입장 시 [폴로/프리토/에스페시아] 입장 불가 - ' + log_num)
        elif (self.wa_pp_cnt == 0):
            log_num = str(random.randrange(1000, 9999))
            self.txt_wa_log.setPlainText('[폴로/프리토/에스페시아]: 입장 불가 - ' + log_num)
        elif (self.wa_pp_cnt < 0):
            self.wa_pp_cnt = 0
            log_num = str(random.randrange(1000, 9999))
            self.txt_wa_log.setPlainText('[폴프]: Stop Press (-) Button - ' + log_num)
        self.lb_wa_pp_cnt.setText(str(self.wa_pp_cnt))

    def clicked_btn_btn_wa_epm(self):
        self.wa_ep_cnt -= 1
        if (self.wa_ep_cnt == 1):
            log_num = str(random.randrange(1000, 9999))
            self.txt_wa_log.setPlainText('다음 입장 시 [폴로/프리토/에스페시아] 입장 불가 - ' + log_num)
        elif (self.wa_ep_cnt == 0):
            log_num = str(random.randrange(1000, 9999))
            self.txt_wa_log.setPlainText('[폴로/프리토/에스페시아]: 입장 불가 - ' + log_num)
        elif (self.wa_ep_cnt < 0):
            self.wa_ep_cnt = 0
            log_num = str(random.randrange(1000, 9999))
            self.txt_wa_log.setPlainText('[에페]: Stop Press (-) Button - ' + log_num)
        self.lb_wa_ep_cnt.setText(str(self.wa_ep_cnt))

    def clicked_btn_btn_wa_fwm(self):
        self.wa_fw_cnt -= 1
        if (self.wa_fw_cnt == 1):
            log_num = str(random.randrange(1000, 9999))
            self.txt_wa_log.setPlainText('다음 입장 시 [불늑] 입장 불가 - ' + log_num)
        elif (self.wa_fw_cnt == 0):
            log_num = str(random.randrange(1000, 9999))
            self.txt_wa_log.setPlainText('[불늑]: 입장 불가 - ' + log_num)
        elif (self.wa_fw_cnt < 0):
            self.wa_fw_cnt = 0
            log_num = str(random.randrange(1000, 9999))
            self.txt_wa_log.setPlainText('[불늑]: Stop Press (-) Button - ' + log_num)
        self.lb_wa_fw_cnt.setText(str(self.wa_fw_cnt))
        
    def clicked_btn_btn_wa_ppp(self):
        self.wa_pp_cnt += 1
        if (self.wa_pp_cnt > 15):
            self.wa_pp_cnt = 15
            log_num = str(random.randrange(1000, 9999))
            self.txt_wa_log.setPlainText('[폴프]: Stop Press (+) Button - ' + log_num)
        self.lb_wa_pp_cnt.setText(str(self.wa_pp_cnt))

    def clicked_btn_btn_wa_epp(self):
        self.wa_ep_cnt += 1
        if (self.wa_ep_cnt > 15):
            self.wa_ep_cnt = 15
            log_num = str(random.randrange(1000, 9999))
            self.txt_wa_log.setPlainText('[폴프]: Stop Press (+) Button - ' + log_num)
        self.lb_wa_ep_cnt.setText(str(self.wa_ep_cnt))
    
    def clicked_btn_btn_wa_fwp(self):
        self.wa_fw_cnt += 1
        if (self.wa_fw_cnt > 15):
            self.wa_fw_cnt = 15
            log_num = str(random.randrange(1000, 9999))
            self.txt_wa_log.setPlainText('[폴프]: Stop Press (+) Button - ' + log_num)
        self.lb_wa_fw_cnt.setText(str(self.wa_fw_cnt))
        

    # custom skill functions
    def clicked_btn_wa_s1(self):
        custom_sec = self.txt_wa_s1.text()
        if (is_int_number(custom_sec)):
            self.lb_wa_s1_sec.setText(custom_sec)
            self.wa_s1_ss = int(custom_sec)
            log_num = str(random.randrange(1000, 9999))
            self.txt_wa_log.setPlainText('[스킬1]: 적용 성공 - ' + log_num)
        else:
            self.lb_wa_s1_sec.setText('-')
            self.wa_s1_ss = -1
            log_num = str(random.randrange(1000, 9999))
            self.txt_wa_log.setPlainText('[스킬1]: 양의 정수를 10~7200 (초)단위로 입력 - ' + log_num)

        self.txt_wa_s1.clear()

    def clicked_btn_wa_s2(self):
        custom_sec = self.txt_wa_s2.text()
        if (is_int_number(custom_sec)):
            self.lb_wa_s2_sec.setText(custom_sec)
            self.wa_s2_ss = int(custom_sec)
            log_num = str(random.randrange(1000, 9999))
            self.txt_wa_log.setPlainText('[스킬2]: 적용 성공 - ' + log_num)
        else:
            self.lb_wa_s2_sec.setText('-')
            self.wa_s2_ss = -1
            log_num = str(random.randrange(1000, 9999))
            self.txt_wa_log.setPlainText('[스킬2]: 양의 정수를 10~7200 (초)단위로 입력 - ' + log_num)

        self.txt_wa_s2.clear()

    def clicked_btn_wa_s3(self):
        custom_sec = self.txt_wa_s3.text()
        if (is_int_number(custom_sec)):
            self.lb_wa_s3_sec.setText(custom_sec)
            self.wa_s3_ss = int(custom_sec)
            log_num = str(random.randrange(1000, 9999))
            self.txt_wa_log.setPlainText('[스킬3]: 적용 성공 - ' + log_num)
        else:
            self.lb_wa_s3_sec.setText('-')
            self.wa_s3_ss = -1
            log_num = str(random.randrange(1000, 9999))
            self.txt_wa_log.setPlainText('[스킬3]: 양의 정수를 10~7200 (초)단위로 입력 - ' + log_num)

        self.txt_wa_s3.clear()

    def clicked_btn_wa_s4(self):
        custom_sec = self.txt_wa_s4.text()
        if (is_int_number(custom_sec)):
            self.lb_wa_s4_sec.setText(custom_sec)
            self.wa_s4_ss = int(custom_sec)
            log_num = str(random.randrange(1000, 9999))
            self.txt_wa_log.setPlainText('[스킬4]: 적용 성공 - ' + log_num)
        else:
            self.lb_wa_s4_sec.setText('-')
            self.wa_s4_ss = -1
            log_num = str(random.randrange(1000, 9999))
            self.txt_wa_log.setPlainText('[스킬4]: 양의 정수를 10~7200 (초)단위로 입력 - ' + log_num)

        self.txt_wa_s4.clear()

    def clicked_btn_wa_s5(self):
        custom_sec = self.txt_wa_s5.text()
        if (is_int_number(custom_sec)):
            self.lb_wa_s5_sec.setText(custom_sec)
            self.wa_s5_ss = int(custom_sec)
            log_num = str(random.randrange(1000, 9999))
            self.txt_wa_log.setPlainText('[스킬5]: 적용 성공 - ' + log_num)
        else:
            self.lb_wa_s5_sec.setText('-')
            self.wa_s5_ss = -1
            log_num = str(random.randrange(1000, 9999))
            self.txt_wa_log.setPlainText('[스킬5]: 양의 정수를 10~7200 (초)단위로 입력 - ' + log_num)

        self.txt_wa_s5.clear()

    def clicked_btn_wa_s6(self):
        custom_sec = self.txt_wa_s6.text()
        if (is_int_number(custom_sec)):
            self.lb_wa_s6_sec.setText(custom_sec)
            self.wa_s6_ss = int(custom_sec)
            log_num = str(random.randrange(1000, 9999))
            self.txt_wa_log.setPlainText('[스킬6]: 적용 성공 - ' + log_num)
        else:
            self.lb_wa_s6_sec.setText('-')
            self.wa_s6_ss = -1
            log_num = str(random.randrange(1000, 9999))
            self.txt_wa_log.setPlainText('[스킬6]: 양의 정수를 10~7200 (초)단위로 입력 - ' + log_num)

        self.txt_wa_s6.clear()



####################################################################################################################################################################
# tab_boss_kalos fuctions

    # btn_kalos_start
    def clicked_btn_kalos_start(self):
        if (self.is_difficulty_selected()):
            # main timer start + log
            self.boss_kalos_stop_progress()
            self.cb_prog_mini.setCheckState(2)

            self.boss_kalos_main_timer.start()
            log_num = str(random.randrange(1000, 9999))
            self.txt_kalos_log.setPlainText('[칼로스 1페 입장] - ' + log_num)
            
            # salvo timer start, 155 sec
            self.boss_kalos_salvo_timer.start()
            self.lb_kalos_salvo.setText('[전탄]: 알림 시작')
            self.set_salvo_sec()

            # if timer start, 65 sec
            self.boss_kalos_if_timer.start()
            self.lb_kalos_if.setText('[간섭]: 알림 시작')
            self.set_if_sec()

            # current phase 1
            self.boss_kalos_current_phase = 0
            self.lb_kalos_cphase.setText('현재페이즈: 1')
        else:
            log_num = str(random.randrange(1000, 9999))
            self.txt_kalos_log.setPlainText('[난이도 선택란 획인] - ' + log_num)


    # btn_kalos_reset
    def clicked_btn_kalos_reset(self):
        if (self.is_difficulty_selected()):
            # stop and clear related to phase 1
            self.boss_kalos_stop_progress()
            self.cb_prog_mini.setCheckState(2)

            self.lb_kalos_right.setText('[오비]: 2페 진입')
            self.lb_kalos_left.setText('[왼비]: 2페 진입')
            self.lb_kalos_breath.setText('[브레스]: 2페 진입')

            # main timer restart
            self.boss_kalos_main_timer.start()
            log_num = str(random.randrange(1000, 9999))
            self.txt_kalos_log.setPlainText('[칼로스 2페 입장] - ' + log_num)

            # salvo timer start, 150 sec
            self.boss_kalos_salvo_timer.start()
            self.lb_kalos_salvo.setText('[전탄]: 2페 진입')
            self.reset_salvo_sec()

            # if timer start, 60 sec
            self.boss_kalos_if_timer.start()
            self.lb_kalos_if.setText('[간섭]: 2페 진입')
            self.reset_if_sec()

            # current phase 2-1
            self.boss_kalos_current_phase = 1
            self.lb_kalos_cphase.setText('현재페이즈: 2-1')
        else:
            log_num = str(random.randrange(1000, 9999))
            self.txt_kalos_log.setPlainText('[난이도 선택란 획인] - ' + log_num)

    def boss_kalos_stop_progress(self):
        self.boss_kalos_alarm_heap.clear()
        self.boss_kalos_main_timer.stop()
        self.boss_kalos_salvo_timer.stop()
        self.boss_kalos_if_timer.stop()
        self.boss_kalos_right_timer.stop()
        self.boss_kalos_left_timer.stop()
        self.boss_kalos_breath_timer.stop()

    # btn_kalos_stop
    def clicked_btn_kalos_stop(self):
        self.cb_prog_mini.setCheckState(0)
        self.boss_kalos_stop_progress()
        log_num = str(random.randrange(1000, 9999))
        self.txt_kalos_log.setPlainText('[타이머 중지] - ' + log_num)
        self.lb_kalos_right.setText('')
        self.lb_kalos_left.setText('[비석]: 2초전 알림')
        self.lb_kalos_breath.setText('[브레스]: 브레스 장전 5초전 알림')
        self.lb_kalos_salvo.setText('[전탄]: 10초/5초전 알림')
        self.lb_kalos_if.setText('[간섭]: 10초/5초전 알림')
        self.lb_kalos_cphase.setText('현재페이즈: 입장 전')


    # boss kalos main timer
    def activate_boss_kalos_main_timer(self):
        if (len(self.boss_kalos_alarm_heap)):
            alarm_num = heapq.heappop(self.boss_kalos_alarm_heap)
            winsound.PlaySound(self.b_kalos_wav_list[alarm_num], winsound.SND_ASYNC)


    # boss kalos salvo timer
    def reset_salvo_sec(self):
        self.boss_kalos_salvo_sec = 150

    def set_salvo_sec(self):
        self.boss_kalos_salvo_sec = 155

    def activate_boss_kalos_salvo_timer(self):
        self.lb_kalos_salvo.setText('[전탄]: ' + str(self.boss_kalos_salvo_sec) + '초 전')

        if (self.boss_kalos_salvo_sec == 10):
            heapq.heappush(self.boss_kalos_alarm_heap, 1)
        if (self.boss_kalos_salvo_sec == 5):
            heapq.heappush(self.boss_kalos_alarm_heap, 2)
            self.set_salvo_sec()

        self.boss_kalos_salvo_sec -= 1
        
    def clicked_btn_kalos_salvo(self):
        log_num = str(random.randrange(1000, 9999))
        self.txt_kalos_log.setPlainText('[전탄]: Reset - ' + log_num)
        self.reset_salvo_sec()

    def clicked_btn_kalos_p50s(self):
        log_num = str(random.randrange(1000, 9999))
        self.txt_kalos_log.setPlainText('[전탄]: (+)50초 - ' + log_num)
        self.boss_kalos_salvo_sec += 50

    def clicked_btn_kalos_p20s(self):
        log_num = str(random.randrange(1000, 9999))
        self.txt_kalos_log.setPlainText('[전탄]: (+)20초 - ' + log_num)
        self.boss_kalos_salvo_sec += 20

    def clicked_btn_kalos_p10s(self):
        log_num = str(random.randrange(1000, 9999))
        self.txt_kalos_log.setPlainText('[전탄]: (+)10초 - ' + log_num)
        self.boss_kalos_salvo_sec += 10

    def clicked_btn_kalos_p4s(self):
        log_num = str(random.randrange(1000, 9999))
        self.txt_kalos_log.setPlainText('[전탄]: (+)4초 - ' + log_num)
        self.boss_kalos_salvo_sec += 4

    def clicked_btn_kalos_m50s(self):
        log_num = str(random.randrange(1000, 9999))
        self.txt_kalos_log.setPlainText('[전탄]: (-)50초 - ' + log_num)
        self.boss_kalos_salvo_sec -= 50

    def clicked_btn_kalos_m20s(self):
        log_num = str(random.randrange(1000, 9999))
        self.txt_kalos_log.setPlainText('[전탄]: (-)20초 - ' + log_num)
        self.boss_kalos_salvo_sec -= 20

    def clicked_btn_kalos_m10s(self):
        log_num = str(random.randrange(1000, 9999))
        self.txt_kalos_log.setPlainText('[전탄]: (-)10초 - ' + log_num)
        self.boss_kalos_salvo_sec -= 10

    def clicked_btn_kalos_m4s(self):
        log_num = str(random.randrange(1000, 9999))
        self.txt_kalos_log.setPlainText('[전탄]: (-)4초 - ' + log_num)
        self.boss_kalos_salvo_sec -= 4


    # boss kalos if timer
    def reset_if_sec(self):
        self.boss_kalos_if_sec = 60

    def set_if_sec(self):
        self.boss_kalos_if_sec = 65

    def activate_boss_kalos_if_timer(self):
        self.lb_kalos_if.setText('[간섭]: ' + str(self.boss_kalos_if_sec) + '초 전')

        if (self.boss_kalos_if_sec == 10):
            if (not self.cb_kalos_if_alarm_off.isChecked()):
                heapq.heappush(self.boss_kalos_alarm_heap, 6)
        if (self.boss_kalos_if_sec == 5):
            if (not self.cb_kalos_if_alarm_off.isChecked()):
                heapq.heappush(self.boss_kalos_alarm_heap, 7)
            self.set_if_sec()

        self.boss_kalos_if_sec -= 1

    def clicked_btn_kalos_if(self):
        log_num = str(random.randrange(1000, 9999))
        self.txt_kalos_log.setPlainText('[간섭]: Reset - ' + log_num)
        self.reset_if_sec()


    # boss kalos right timer
    def set_right_sec(self):
        if (self.cb_kalos_easy.isChecked() or self.cb_kalos_normal.isChecked()):
            self.boss_kalos_right_sec = 15
        elif (self.cb_kalos_chaos.isChecked() or self.cb_kalos_extreme.isChecked()):
            self.boss_kalos_right_sec = 12
        else:
            self.boss_kalos_right_timer.stop()
            self.lb_kalos_right.setText('[오비]: 난이도 확인')

    def clicked_btn_right_on(self):
        self.boss_kalos_right_timer.stop()
        self.boss_kalos_right_timer.start()
        self.lb_kalos_right.setText('[오비]: 활성화')
        self.set_right_sec()

    def clicked_btn_right_off(self):
        self.lb_kalos_right.setText('[오비]: 비활성화')
        self.boss_kalos_right_timer.stop()

    def activate_boss_kalos_right_timer(self):
        if (self.boss_kalos_right_sec == 0):
            self.set_right_sec()

        self.lb_kalos_right.setText('[오비]: ' + str(self.boss_kalos_right_sec) + '초 전')

        if (self.boss_kalos_right_sec == 2):
            heapq.heappush(self.boss_kalos_alarm_heap, 4)

        self.boss_kalos_right_sec -= 1


    # left
    def set_left_sec(self):
        if (self.cb_kalos_easy.isChecked() or self.cb_kalos_normal.isChecked()):
            self.boss_kalos_left_sec = 15
        elif (self.cb_kalos_chaos.isChecked() or self.cb_kalos_extreme.isChecked()):
            self.boss_kalos_left_sec = 12
        else:
            self.boss_kalos_left_timer.stop()
            self.lb_kalos_left.setText('[왼비]: 난이도 확인')

    def clicked_btn_left_on(self):
        self.boss_kalos_left_timer.stop()
        self.boss_kalos_left_timer.start()
        self.lb_kalos_left.setText('[왼비]: 활성화')
        self.set_left_sec()

    def clicked_btn_left_off(self):
        self.lb_kalos_left.setText('[왼비]: 비활성화')
        self.boss_kalos_left_timer.stop()

    def activate_boss_kalos_left_timer(self):
        if (self.boss_kalos_left_sec == 0):
            self.set_left_sec()

        self.lb_kalos_left.setText('[왼비]: ' + str(self.boss_kalos_left_sec) + '초 전')

        if (self.boss_kalos_left_sec == 2):
            heapq.heappush(self.boss_kalos_alarm_heap, 5)

        self.boss_kalos_left_sec -= 1


    # breath
    def clicked_btn_breath_on(self):
        self.boss_kalos_breath_sec = 1557
        self.boss_kalos_breath_timer.stop()
        self.boss_kalos_breath_timer.start()
        self.lb_kalos_breath.setText('[브레스]: 활성화')
        match(self.boss_kalos_current_phase):
            case 0:
                self.lb_kalos_breath.setText('[브레스]: 2페이즈가 아닙니다.')
                self.boss_kalos_breath_timer.stop()
            case 1:
                self.boss_kalos_breath_sec = 60
            case 2:
                self.boss_kalos_breath_sec = 45
            case 3:
                self.boss_kalos_breath_sec = 30

    def clicked_btn_breath_off(self):
        self.lb_kalos_breath.setText('[브레스]: 비활성화')
        self.boss_kalos_breath_sec = 1557
        self.boss_kalos_breath_timer.stop()

    def activate_boss_kalos_breath_timer(self):
        match(self.is_boss_kalos_changed_phase):
            case 2:
                # 2-1 to 2-2
                if (self.boss_kalos_previous_phase == 1):
                    self.boss_kalos_breath_sec -= 15
                    self.is_boss_kalos_changed_phase = 0
            case 3:
                # 2-1 to 2-3
                if (self.boss_kalos_previous_phase == 1):
                    self.boss_kalos_breath_sec -= 30
                    self.is_boss_kalos_changed_phase = 0
                # 2-2 to 2-3
                elif (self.boss_kalos_previous_phase == 2):
                    self.boss_kalos_breath_sec -= 15
                    self.is_boss_kalos_changed_phase = 0
            case _:
                self.is_boss_kalos_changed_phase = 0

        self.lb_kalos_breath.setText('[브레스]: ' + str(self.boss_kalos_breath_sec) + '초 전')

        if (self.boss_kalos_breath_sec <= 5):
            heapq.heappush(self.boss_kalos_alarm_heap, 3)
            self.clicked_btn_breath_off()

        self.boss_kalos_breath_sec -= 1

    # phase for breath
    def clicked_btn_kalos_phase2_1(self):
        # phase: 2-1
        self.boss_kalos_current_phase = 1
        self.lb_kalos_cphase.setText('현재페이즈: 2-1')
        
    def clicked_btn_kalos_phase2_2(self):
        # phase: 2-2
        self.boss_kalos_previous_phase = self.boss_kalos_current_phase
        self.boss_kalos_current_phase = 2
        self.is_boss_kalos_changed_phase = 2
        self.lb_kalos_cphase.setText('현재페이즈: 2-2')
        
    def clicked_btn_kalos_phase2_3(self):
        # phase: 2-3
        self.boss_kalos_previous_phase = self.boss_kalos_current_phase
        self.boss_kalos_current_phase = 3
        self.is_boss_kalos_changed_phase = 3
        self.lb_kalos_cphase.setText('현재페이즈: 2-3(4)')

    def is_difficulty_selected(self):
        if ((self.cb_kalos_easy.isChecked()) and (not self.cb_kalos_normal.isChecked()) and (not self.cb_kalos_chaos.isChecked()) and (not self.cb_kalos_extreme.isChecked())):
            return True
        elif ((not self.cb_kalos_easy.isChecked()) and (self.cb_kalos_normal.isChecked()) and (not self.cb_kalos_chaos.isChecked()) and (not self.cb_kalos_extreme.isChecked())):
            return True
        elif ((not self.cb_kalos_easy.isChecked()) and (not self.cb_kalos_normal.isChecked()) and (self.cb_kalos_chaos.isChecked()) and (not self.cb_kalos_extreme.isChecked())):
            return True
        elif ((not self.cb_kalos_easy.isChecked()) and (not self.cb_kalos_normal.isChecked()) and (not self.cb_kalos_chaos.isChecked()) and (self.cb_kalos_extreme.isChecked())):
            return True
        else:
            return False
            

####################################################################################################################################################################
# tab_search functions
        
    def clicked_btn_api_key_input(self):
        api_key = self.txt_api_key.text()
        self.set_api_key(api_key)
        self.txt_api_key.clear()
        

    def set_api_key(self, api_key):
        api_key_file = open('./nexon_api_key/api_key_lts.txt', 'w')
        api_key_file.write(api_key)
        api_key_file.close()
        self.keys = api_key
        self.headers = {
            "x-nxopen-api-key": str(self.keys)
        }
        self.lb_api_key.setText('API키: ' + api_key)

    def make_c_url(self, tag, ocid, time):
        c_url = "https://open.api.nexon.com/maplestory/v1/character/"
        c_url += str(tag) + '?ocid=' + ocid + "&date=" + time

        return c_url


    def make_u_url(self, tag, ocid, time):
        c_url = "https://open.api.nexon.com/maplestory/v1/user/"
        c_url += str(tag) + '?ocid=' + ocid + "&date=" + time

        return c_url


    # server image load function
    def display_s_img(self, server):
        s_img = QPixmap(resource_path("resources/img/none.gif"))
        
        match (server):
            case '아케인':
                s_img = QPixmap(resource_path("resources/img/arcane.gif"))
            case '오로라':
                s_img = QPixmap(resource_path("resources/img/aurora.gif"))
            case '베라':
                s_img = QPixmap(resource_path("resources/img/bera.gif"))
            case '크로아':
                s_img = QPixmap(resource_path("resources/img/croa.gif"))
            case '엘리시움':
                s_img = QPixmap(resource_path("resources/img/elysium.gif"))
            case '이노시스':
                s_img = QPixmap(resource_path("resources/img/enosis.gif"))
            case '루나':
                s_img = QPixmap(resource_path("resources/img/luna.gif"))
            case '노바':
                s_img = QPixmap(resource_path("resources/img/nova.gif"))
            case '리부트':
                s_img = QPixmap(resource_path("resources/img/reboot.gif"))
            case '리부트2':
                s_img = QPixmap(resource_path("resources/img/reboot.gif"))
            case '레드':
                s_img = QPixmap(resource_path("resources/img/red.gif"))
            case '스카니아':
                s_img = QPixmap(resource_path("resources/img/scania.gif"))
            case '유니온':
                s_img = QPixmap(resource_path("resources/img/union.gif"))
            case '제니스':
                s_img = QPixmap(resource_path("resources/img/zenith.gif"))
        
        self.lb_c_server_img.setPixmap(s_img)


    # display 1-million, 10-thousand unit funtion
    def add_atkpow_unit(self, atkpow):
        strlen = len(atkpow)
        if (strlen > 0 and strlen <= 4):
            return atkpow
        elif (strlen > 4 and strlen <= 8):
            low = atkpow[-4:]
            high = atkpow[:-4]
            res =  high + '만 ' + low
            return res
        elif (strlen > 8):
            low = atkpow[-4:]
            mid = atkpow[-8:-4]
            high = atkpow[:-8]
            res = high + '억 ' + mid + '만 ' + low
            return res


    # character stat display function
    def display_stat(self, stat_name, stat_value):
        match (stat_name):
            case '최대 스탯공격력':
                # make ',' per 3-num
                form_num = '{0:,}'.format(int(stat_value))
                self.lb_c_max_spow.setText('최대 스공: ' + form_num)
            case '최소 스탯공격력':
                form_num = '{0:,}'.format(int(stat_value))
                self.lb_c_min_spow.setText('최소 스공: ' + form_num)
            case '데미지':
                self.lb_c_dmg.setText(stat_name + ': ' + stat_value + '%')
            case '보스 몬스터 데미지':
                self.lb_c_bdmg.setText('보뎀: ' + stat_value + '%')
            case '크리티컬 데미지':
                self.lb_c_cdmg.setText('크뎀: ' + stat_value + '%')
            case '상태이상 추가 데미지':
                self.lb_c_sdmg.setText('상추뎀: ' + stat_value + '%')
            case '방어율 무시':
                self.lb_c_defig.setText('방무: ' + stat_value + '%')
            case '버프 지속시간':
                self.lb_c_buf.setText(stat_name + ': ' + stat_value + '%')
            case '재사용 대기시간 감소 (초)':
                self.lb_c_resec.setText('재감 (초): ' + stat_value + '초')
            case '재사용 대기시간 감소 (%)':
                self.lb_c_reper.setText('재감 (%): ' + stat_value + '%')
            case '재사용 대기시간 미적용':
                self.lb_c_renon.setText('재감 미적용: ' + stat_value + '%')
            case '상태이상 내성':
                self.lb_c_sdef.setText('상태 이상 내성: ' + stat_value)
            case '속성 내성 무시':
                self.lb_c_elmig.setText(stat_name + ': ' + stat_value + '%')
            case '크리티컬 확률':
                self.lb_c_crper.setText('크확: ' + stat_value + '%')
            case '공격력':
                form_num = '{0:,}'.format(int(stat_value))
                self.lb_c_atk.setText('공: ' + form_num)
            case '마력':
                form_num = '{0:,}'.format(int(stat_value))
                self.lb_c_mag.setText('마: ' + form_num)
            case 'STR':
                form_num = '{0:,}'.format(int(stat_value))
                self.lb_c_str.setText(stat_name + ': ' + form_num)
            case 'DEX':
                form_num = '{0:,}'.format(int(stat_value))
                self.lb_c_dex.setText(stat_name + ': ' + form_num)
            case 'INT':
                form_num = '{0:,}'.format(int(stat_value))
                self.lb_c_int.setText(stat_name + ': ' + form_num)
            case 'LUK':
                form_num = '{0:,}'.format(int(stat_value))
                self.lb_c_luk.setText(stat_name + ': ' + form_num)
            case 'HP':
                form_num = '{0:,}'.format(int(stat_value))
                self.lb_c_hp.setText(stat_name + ': ' + form_num)
            case 'MP':
                if (stat_value == None):
                    self.lb_c_mp.setText('MP: -')
                else:
                    form_num = '{0:,}'.format(int(stat_value))
                    self.lb_c_mp.setText(stat_name + ': ' + form_num)
            case '스타포스':
                self.lb_c_star_txt.setText(stat_value)
            case '아케인포스':
                self.lb_c_arc_txt.setText(stat_value)
            case '어센틱포스':
                self.lb_c_atc_txt.setText(stat_value)
            case '일반 몬스터 데미지':
                self.lb_c_ndmg_txt.setText(stat_value + '%')
            case '아이템 드롭률':
                 self.lb_c_item_txt.setText(stat_value + '%')
            case '메소 획득량':
                 self.lb_c_meso_txt.setText(stat_value + '%')
            case '추가 경험치 획득':
                 self.lb_c_expbuf_txt.setText(stat_value + '%')
            case '소환수 지속시간 증가':
                self.lb_c_summ.setText(stat_name + ': ' + stat_value + '%')
            case '스탠스':
                self.lb_c_stan.setText(stat_name + ': ' + stat_value + '%')
            case '방어력':
                form_num = '{0:,}'.format(int(stat_value))
                self.lb_c_def.setText(stat_name + ': ' + form_num)
            case '이동속도':
                self.lb_c_mvspd.setText('이속: ' + stat_value + '%')
            case '점프력':
                self.lb_c_jppow.setText(stat_name + ': ' + stat_value + '%')
            case '공격 속도':
                self.lb_c_atspd.setText('공속: ' + stat_value + '단계')
            case '최종 데미지':
                self.lb_c_fdmg.setText('최종뎀: ' + stat_value + '%')
            case '무기 숙련도':
                self.lb_c_wppro.setText(stat_name + ': ' + stat_value + '%')
            case '전투력':
                # display 1-million, 10-thousand unit funtion call
                self.lb_c_atkpow.setText(stat_name + ': ' + self.add_atkpow_unit(stat_value))


    # character hyper stat display function
    def display_hyper_stat(self, stat_type, stat_increase):
        if (stat_increase is None):
            stat_increase = '-'

        match (stat_type):
            case 'STR':
                self.lb_h_str.setText(stat_increase)
            case 'DEX':
                self.lb_h_dex.setText(stat_increase)
            case 'INT':
                self.lb_h_int.setText(stat_increase)
            case 'LUK':
                self.lb_h_luk.setText(stat_increase)
            case 'HP':
                self.lb_h_hp.setText(stat_increase)
            case 'MP':
                self.lb_h_mp.setText(stat_increase)
            case 'DF/TF/PP':
                self.lb_h_dftfpp.setText(stat_increase)
            case '크리티컬 확률':
                self.lb_h_crper.setText(stat_increase)
            case '크리티컬 데미지':
                self.lb_h_cdmg.setText(stat_increase)
            case '방어율 무시':
                self.lb_h_defig.setText(stat_increase)
            case '데미지':
                self.lb_h_dmg.setText(stat_increase)
            case '보스 몬스터 공격 시 데미지 증가':
                self.lb_h_bdmg.setText(stat_increase)
            case '상태 이상 내성':
                self.lb_h_sdef.setText(stat_increase)
            case '공격력/마력':
                self.lb_h_atkmag.setText(stat_increase)
            case '획득 경험치':
                self.lb_h_expbuf.setText(stat_increase)
            case '아케인포스':
                self.lb_h_arc.setText(stat_increase)
            case '일반 몬스터 공격 시 데미지 증가':
                self.lb_h_ndmg.setText(stat_increase)


    # ability color display function
    def define_ability_color(self, ability_grade):
        ability_color = 'background-color: '
        match(ability_grade):
            case '레전드리':
                ability_color += '#aaff00'
            case '유니크':
                ability_color += '#ffaa00'
            case '에픽':
                ability_color += '#aa00ff'
            case '레어':
                ability_color += '#55ffff'
        return ability_color


    # character ability display function
    def display_ability(self, ability_no, ability_grade, ability_value):
        match (ability_no):
            case '1':
                # ability color display function call by grade string
                self.lb_ab_fst.setStyleSheet(self.define_ability_color(ability_grade))
                self.lb_ab_fst.setText('  ' + ability_value)
            case '2':
                self.lb_ab_snd.setStyleSheet(self.define_ability_color(ability_grade))
                self.lb_ab_snd.setText('  ' + ability_value)
            case '3':
                self.lb_ab_trd.setStyleSheet(self.define_ability_color(ability_grade))
                self.lb_ab_trd.setText('  ' + ability_value)


    # character equip item display function
    def display_equip(self, obj):
        equip_slot_txt = obj.get('item_equipment_slot')
        equip_txt1 = equip_slot_txt + ": " + obj.get('item_name')

        # equip_txt1: item name & starforce
        equip_star_txt = obj.get('starforce')
        is_amzstar = obj.get('starforce_scroll_flag')
        if (equip_star_txt != '0'):
            if (is_amzstar == '미사용'):
                equip_txt1 += ' [ ' + equip_star_txt + '성 ]'
            else:
                equip_txt1 += ' [ 놀 ' + equip_star_txt + '성 ]'
        else:
            equip_txt1 += ' [ 스타포스 X ]'

        self.w_list_item.addItem(equip_txt1)

        # equip_txt2: potential option
        equip_txt2 = obj.get('potential_option_grade')

        if (equip_txt2 is not None):
            equip_txt2 = '  ㄴ 윗잠(' + equip_txt2 + ') [ '

            is_first = obj.get('potential_option_1')
            if (is_first is None):
                equip_txt2 += '잠재 능력 감정 필요 ]'
            else:
                equip_txt2 += is_first
                is_second = obj.get('potential_option_2')
                if (is_second is None):
                    equip_txt2 += ' ]'
                else:
                    equip_txt2 += ' / ' + is_second
                    is_third = obj.get('potential_option_3')
                    if (is_third is None):
                        equip_txt2 += ' ]'
                    else:
                        equip_txt2 += ' / ' + is_third  + ' ]'

            self.w_list_item.addItem(equip_txt2)
        
        # equip_txt3: additional potential option
        equip_txt3 = obj.get('additional_potential_option_grade')

        if (equip_txt3 is not None):
            equip_txt3 = '  ㄴ 밑잠(' + equip_txt3 + ') [ '

            is_first = obj.get('additional_potential_option_1')
            if (is_first is None):
                equip_txt3 += '잠재 능력 감정 필요 ]'
            else:
                equip_txt3 += is_first
                is_second = obj.get('additional_potential_option_2')
                if (is_second is None):
                    equip_txt3 += ' ]'
                else:
                    equip_txt3 += ' / ' + is_second
                    is_third = obj.get('additional_potential_option_3')
                    if (is_third is None):
                        equip_txt3 += ' ]'
                    else:
                        equip_txt3 += ' / ' + is_third  + ' ]'

            self.w_list_item.addItem(equip_txt3)

        # equip_txt4: add option
        equip_txt4_json = obj.get('item_add_option')

        if (equip_txt4_json is not None):
            equip_add_list = [ equip_txt4_json.get('str'), equip_txt4_json.get('dex'), equip_txt4_json.get('int'), equip_txt4_json.get('luk'), equip_txt4_json.get('max_hp'), equip_txt4_json.get('max_mp'), equip_txt4_json.get('attack_power'), equip_txt4_json.get('magic_power'), equip_txt4_json.get('boss_damage'), equip_txt4_json.get('damage'), equip_txt4_json.get('all_stat') ]
            equip_txt4 = '  ㄴ 추옵 [ '
            add_idx = 0
            add_cnt = 0
            for i in equip_add_list:
                if (i != '0'):
                    add_cnt += 1
                    if (add_idx == 0):
                        equip_txt4 += '힘: +' + i + ' / '
                    elif (add_idx == 1):
                        equip_txt4 += '덱: +' + i + ' / '
                    elif (add_idx == 2):
                        equip_txt4 += '인: +' + i + ' / '
                    elif (add_idx == 3):
                        equip_txt4 += '럭: +' + i + ' / '
                    elif (add_idx == 4):
                        equip_txt4 += 'HP: +' + i + ' / '
                    elif (add_idx == 5):
                        equip_txt4 += 'MP: +' + i + ' / '
                    elif (add_idx == 6):
                        equip_txt4 += '공: +' + i + ' / '
                    elif (add_idx == 7):
                        equip_txt4 += '마: +' + i + ' / '
                    elif (add_idx == 8):
                        equip_txt4 += '보뎀: +' + i + '% / '
                    elif (add_idx == 9):
                        equip_txt4 += '뎀: +' + i + '% / '
                    elif (add_idx == 10):
                        equip_txt4 += '올: +' + i + '% / '
                add_idx += 1

            equip_txt4 = equip_txt4[:-2] + ']'

            if (add_cnt):
                self.w_list_item.addItem(equip_txt4)

        # equip_txt5: scroll option
        equip_txt5_json = obj.get('item_etc_option')

        if (equip_txt5_json is not None):
            equip_etc_list = [ equip_txt5_json.get('str'), equip_txt5_json.get('dex'), equip_txt5_json.get('int'), equip_txt5_json.get('luk'), equip_txt5_json.get('max_hp'), equip_txt5_json.get('max_mp'), equip_txt5_json.get('attack_power'), equip_txt5_json.get('magic_power') ]
            equip_txt5 = '  ㄴ 작 [ '
            etc_idx = 0
            etc_cnt = 0
            for i in equip_etc_list:
                if (i != '0'):
                    etc_cnt += 1
                    if (etc_idx == 0):
                        equip_txt5 += '힘: +' + i + ' / '
                    elif (etc_idx == 1):
                        equip_txt5 += '덱: +' + i + ' / '
                    elif (etc_idx == 2):
                        equip_txt5 += '인: +' + i + ' / '
                    elif (etc_idx == 3):
                        equip_txt5 += '럭: +' + i + ' / '
                    elif (etc_idx == 4):
                        equip_txt5 += 'HP: +' + i + ' / '
                    elif (etc_idx == 5):
                        equip_txt5 += 'MP: +' + i + ' / '
                    elif (etc_idx == 6):
                        equip_txt5 += '공: +' + i + ' / '
                    elif (etc_idx == 7):
                        equip_txt5 += '마: +' + i + ' / '
                etc_idx += 1

            equip_txt5 = equip_txt5[:-2] + ']'

            if (etc_cnt):
                self.w_list_item.addItem(equip_txt5)

        self.w_list_item.addItem('-----------------------------------------------------------------------------------------------------------------------')


    # character equip symbol display function
    def display_symbol(self, symbol_name, symbol_level):
        match(symbol_name):
            case '아케인심볼 : 소멸의 여로':
                sy_img_pixmap = QPixmap(resource_path("resources/img/sy_yr.png"))
                self.lb_sy_yr.setPixmap(sy_img_pixmap)
                self.lb_sy_yr_txt.setText(str(symbol_level) + ' lv')
            case '아케인심볼 : 츄츄 아일랜드':
                sy_img_pixmap = QPixmap(resource_path("resources/img/sy_cc.png"))
                self.lb_sy_cc.setPixmap(sy_img_pixmap)
                self.lb_sy_cc_txt.setText(str(symbol_level) + ' lv')
            case '아케인심볼 : 레헬른':
                sy_img_pixmap = QPixmap(resource_path("resources/img/sy_rh.png"))
                self.lb_sy_rh.setPixmap(sy_img_pixmap)
                self.lb_sy_rh_txt.setText(str(symbol_level) + ' lv')
            case '아케인심볼 : 에스페라':
                sy_img_pixmap = QPixmap(resource_path("resources/img/sy_es.png"))
                self.lb_sy_es.setPixmap(sy_img_pixmap)
                self.lb_sy_es_txt.setText(str(symbol_level) + ' lv')
            case '아케인심볼 : 모라스':
                sy_img_pixmap = QPixmap(resource_path("resources/img/sy_mr.png"))
                self.lb_sy_mr.setPixmap(sy_img_pixmap)
                self.lb_sy_mr_txt.setText(str(symbol_level) + ' lv')
            case '아케인심볼 : 아르카나':
                sy_img_pixmap = QPixmap(resource_path("resources/img/sy_ar.png"))
                self.lb_sy_ar.setPixmap(sy_img_pixmap)
                self.lb_sy_ar_txt.setText(str(symbol_level) + ' lv')
            case '어센틱심볼 : 세르니움':
                sy_img_pixmap = QPixmap(resource_path("resources/img/sy_sr.png"))
                self.lb_sy_sr.setPixmap(sy_img_pixmap)
                self.lb_sy_sr_txt.setText(str(symbol_level) + ' lv')
            case '어센틱심볼 : 아르크스':
                sy_img_pixmap = QPixmap(resource_path("resources/img/sy_ht.png"))
                self.lb_sy_ht.setPixmap(sy_img_pixmap)
                self.lb_sy_ht_txt.setText(str(symbol_level) + ' lv')
            case '어센틱심볼 : 오디움':
                sy_img_pixmap = QPixmap(resource_path("resources/img/sy_od.png"))
                self.lb_sy_od.setPixmap(sy_img_pixmap)
                self.lb_sy_od_txt.setText(str(symbol_level) + ' lv')
            case '어센틱심볼 : 도원경':
                sy_img_pixmap = QPixmap(resource_path("resources/img/sy_dw.png"))
                self.lb_sy_dw.setPixmap(sy_img_pixmap)
                self.lb_sy_dw_txt.setText(str(symbol_level) + ' lv')
            case '어센틱심볼 : 아르테리아':
                sy_img_pixmap = QPixmap(resource_path("resources/img/sy_at.png"))
                self.lb_sy_at.setPixmap(sy_img_pixmap)
                self.lb_sy_at_txt.setText(str(symbol_level) + ' lv')
            case '어센틱심볼 : 카르시온':
                sy_img_pixmap = QPixmap(resource_path("resources/img/sy_kr.png"))
                self.lb_sy_kr.setPixmap(sy_img_pixmap)
                self.lb_sy_kr_txt.setText(str(symbol_level) + ' lv')


    # character skill display function
    def display_skill(self, obj):
        skill_txt = '    '
        skill_name_txt = obj.get('skill_name')
        skill_lv_txt = str(obj.get('skill_level'))
        if (skill_lv_txt != '0'):
            skill_txt += skill_name_txt + ': ' + str(obj.get('skill_level'))
            if (skill_name_txt == 'HEXA 스탯'):
                skill_txt += '슬롯'
            else:
                skill_txt += 'lv'
            self.w_list_skill.addItem(skill_txt)


    def display_hexastat(self, obj):
        slot_id = int(obj.get('slot_id')) + 1
        slot_id_str = str(slot_id) + '번 슬롯: ' + str(obj.get('stat_grade')) + 'lv'
        main_stat = '  ㄴ메인: ' + obj.get('main_stat_name') + ' ' + str(obj.get('main_stat_level')) + 'lv'
        sub_stat_1 = '  ㄴ서브1: ' + obj.get('sub_stat_name_1') + ' ' + str(obj.get('sub_stat_level_1')) + 'lv'
        sub_stat_2 = '  ㄴ서브2: ' + obj.get('sub_stat_name_2') + ' ' + str(obj.get('sub_stat_level_2')) + 'lv'
        self.w_list_skill.addItem(slot_id_str)
        self.w_list_skill.addItem(main_stat)
        self.w_list_skill.addItem(sub_stat_1)
        self.w_list_skill.addItem(sub_stat_2)


    def reset_search_tap(self):
        self.txt_c_log.clear()
        self.txt_c_name.clear()
        self.w_list_item.clear()
        self.w_list_skill.clear()
        self.w_list_union.clear()


        self.te_is_real_you.clear()
        self.lb_c_atkpow.setText('전투력측정중')
        self.pb_exp.setValue(0)
        self.lb_c_exp.clear()
        self.lb_c_server_img.clear()


        self.lb_c_img.clear()
        self.lb_c_name.clear()
        self.lb_c_server.setText('서버:')
        self.lb_c_class.setText('직업:')
        self.lb_c_gen.setText('성별:')
        self.lb_c_level.setText('레벨:')
        self.lb_c_gname.setText('길드:')
        self.lb_c_pop.setText('인기도:')
        self.lb_c_dojang.setText('무릉:')
        self.lb_c_stime.setText('검색 기준시:')


        self.lb_c_max_spow.setText('최대 스공')
        self.lb_c_min_spow.setText('최소 스공')
        self.lb_c_dmg.setText('데미지')
        self.lb_c_bdmg.setText('보뎀')
        self.lb_c_cdmg.setText('크뎀')
        self.lb_c_sdmg.setText('상추뎀')
        self.lb_c_defig.setText('방무')
        self.lb_c_buf.setText('버프 지속시간')
        self.lb_c_resec.setText('재감 (초)')
        self.lb_c_reper.setText('재감 (%)')
        self.lb_c_renon.setText('재감 미적용')
        self.lb_c_sdef.setText('상태 이상 내성')
        self.lb_c_elmig.setText('속성 내성 무시')
        self.lb_c_crper.setText('크확')
        self.lb_c_atk.setText('공')
        self.lb_c_mag.setText('마')
        self.lb_c_str.setText('STR')
        self.lb_c_dex.setText('DEX')
        self.lb_c_int.setText('INT')
        self.lb_c_luk.setText('LUK')
        self.lb_c_hp.setText('HP')
        self.lb_c_mp.setText('MP')
        self.lb_c_star_txt.clear()
        self.lb_c_arc_txt.clear()
        self.lb_c_atc_txt.clear()
        self.lb_c_ndmg_txt.clear()
        self.lb_c_item_txt.clear()
        self.lb_c_meso_txt.clear()
        self.lb_c_expbuf_txt.clear()
        self.lb_c_summ.setText('소환수 지속시간 증가')
        self.lb_c_stan.setText('스탠스')
        self.lb_c_def.setText('방어력')
        self.lb_c_mvspd.setText('이속')
        self.lb_c_jppow.setText('점프력')
        self.lb_c_atspd.setText('공속')
        self.lb_c_fdmg.setText('최종뎀')
        self.lb_c_wppro.setText('무기 숙련도')


        self.lb_h_str.setText('STR')
        self.lb_h_dex.setText('DEX')
        self.lb_h_int.setText('INT')
        self.lb_h_luk.setText('LUK')
        self.lb_h_hp.setText('HP')
        self.lb_h_mp.setText('MP')
        self.lb_h_dftfpp.setText('DF/TF/PP')
        self.lb_h_crper.setText('크리티컬 확률')
        self.lb_h_cdmg.setText('크리티컬 데미지')
        self.lb_h_defig.setText('방어율 무시')
        self.lb_h_dmg.setText('데미지')
        self.lb_h_bdmg.setText('보스 몬스터 공격 시 데미지 증가')
        self.lb_h_sdef.setText('상태 이상 내성')
        self.lb_h_atkmag.setText('공격력/마력')
        self.lb_h_expbuf.setText('획득 경험치')
        self.lb_h_arc.setText('아케인포스')
        self.lb_h_ndmg.setText('일반 몬스터 공격 시 데미지 증가')
        self.lb_h_pnum.setText('    적용중인 프리셋')
        self.lb_h_tpnt.setText('총 스탯 포인트')
        self.lb_h_upnt.setText('사용 스탯 포인트')
        self.lb_h_apnt.setText('잔여 스탯 포인트')


        self.lb_pp_chm.setText('매력')
        self.lb_pp_crm.setText('카리스마')
        self.lb_pp_hdc.setText('손재주')
        self.lb_pp_ist.setText('통찰력')
        self.lb_pp_ssb.setText('감성')
        self.lb_pp_wln.setText('의지')


        self.lb_ab_fst.clear()
        self.lb_ab_snd.clear()
        self.lb_ab_trd.clear()


        self.lb_sy_yr.clear()
        self.lb_sy_yr_txt.clear()
        self.lb_sy_cc.clear()
        self.lb_sy_cc_txt.clear()
        self.lb_sy_rh.clear()
        self.lb_sy_rh_txt.clear()
        self.lb_sy_es.clear()
        self.lb_sy_es_txt.clear()
        self.lb_sy_mr.clear()
        self.lb_sy_mr_txt.clear()
        self.lb_sy_ar.clear()
        self.lb_sy_ar_txt.clear()
        self.lb_sy_sr.clear()
        self.lb_sy_sr_txt.clear()
        self.lb_sy_ht.clear()
        self.lb_sy_ht_txt.clear()
        self.lb_sy_od.clear()
        self.lb_sy_od_txt.clear()
        self.lb_sy_dw.clear()
        self.lb_sy_dw_txt.clear()
        self.lb_sy_at.clear()
        self.lb_sy_at_txt.clear()
        self.lb_sy_kr.clear()
        self.lb_sy_kr_txt.clear()


    # search main/sub charactor function
    def is_real_you(self, search_name, search_ocid, search_json, base_time):
        search_server_str = search_json.get('world_name')
        if (search_server_str is None):
            search_server_str = '?'
        self.te_is_real_you.appendPlainText('=======================================================================================================================')
        self.te_is_real_you.appendPlainText(' ')
        self.te_is_real_you.appendPlainText('                                                   검색중: 모든 정보 로딩까지 약 5초 정도 소요됩니다.')
        self.te_is_real_you.appendPlainText(' ')
        self.te_is_real_you.appendPlainText('=======================================================================================================================')
        self.te_is_real_you.appendPlainText('                             [ Ctrl + a (전체선택) -> Ctrl + c (복사) -> Ctrl + v (붙여넣기) ] : 본/부캐 창만 가능 합니다.')
        self.te_is_real_you.appendPlainText('-----------------------------------------------------------------------------------------------------------------------')
        self.te_is_real_you.appendPlainText('[검색 결과]')
        self.te_is_real_you.appendPlainText('    검색 캐릭터 명: ' + search_name)
        self.te_is_real_you.appendPlainText('    검색 캐릭터 ocid: ' + search_ocid)
        self.te_is_real_you.appendPlainText('    검색 캐릭터 서버: ' + search_server_str)
        self.te_is_real_you.appendPlainText('-----------------------------------------------------------------------------------------------------------------------')


        # ranking union
        url_string = "https://open.api.nexon.com/maplestory/v1/ranking/union?ocid=" + search_ocid + "&date=" + base_time
        union_base_req = requests.get(url_string, headers = self.headers)

        if (union_base_req.status_code == 200):
            self.te_is_real_you.appendPlainText('[유니온 기반 검색]')
            union_base_json = union_base_req.json()
            union_base_obj = union_base_json.get('ranking')
            if (len(union_base_obj) != 0):
                for obj in union_base_obj:
                    self.te_is_real_you.appendPlainText("    본캐: " + obj.get('character_name'))
                    self.te_is_real_you.appendPlainText("    서버: " + obj.get('world_name'))
            else:
                self.te_is_real_you.appendPlainText("    갱신필요")
        else:
            search_log += 'sub 0: 유니온 랭킹 정보 조회 실패 GET(' + str(union_base_req.status_code) + ')'
            self.te_is_real_you.appendPlainText(search_log)
            return


        self.te_is_real_you.appendPlainText('-----------------------------------------------------------------------------------------------------------------------')


        # ranking achievement
        url_string = "https://open.api.nexon.com/maplestory/v1/ranking/achievement?date=" + base_time + "&ocid=" + search_ocid
        achive_base_req = requests.get(url_string, headers = self.headers)

        if (achive_base_req.status_code == 200):
            self.te_is_real_you.appendPlainText('[업적 기반 검색]')
            achive_base_json = achive_base_req.json()
            achive_base_obj = achive_base_json.get('ranking')
            if (len(achive_base_obj) != 0):
                for obj in achive_base_obj:
                    self.te_is_real_you.appendPlainText("    공홈 대표 캐릭터: " + obj.get('character_name'))
                    self.te_is_real_you.appendPlainText("    서버: " + obj.get('world_name'))
            else:
                self.te_is_real_you.appendPlainText("    갱신필요")
        else:
            search_log += 'sub 1: 업적 랭킹 정보 조회 실패 GET(' + str(achive_base_req.status_code) + ')'
            self.te_is_real_you.appendPlainText(search_log)
            return


        self.te_is_real_you.appendPlainText('=======================================================================================================================')


    # search function
    def clicked_btn_c_search(self):
        # input data, base time, log init
        search_start_time = time.time()
        c_name = self.txt_c_name.text()
        base_time = QDateTime.currentDateTime().addDays(-1)
        base_time_str = base_time.toString('yyyy-MM-dd')
        search_log = ''


        # reset previous data
        self.reset_search_tap()
        

        # character ocid request
        url_str = "https://open.api.nexon.com/maplestory/v1/id?character_name=" + str(c_name)
        ocid_req = requests.get(url_str, headers = self.headers)

        if (ocid_req.status_code == 200):
            ocid_json = ocid_req.json()
            ocid_str = ocid_json.get('ocid')
            

            # character basic request
            url_str = self.make_c_url('basic', ocid_str, base_time_str)
            c_basic_req = requests.get(url_str, headers = self.headers)

            if (c_basic_req.status_code == 200):
                c_basic_json = c_basic_req.json()
                basic_c_stime = c_basic_json.get('date')
                basic_c_stime = basic_c_stime.split('T')[0]
                self.lb_c_stime.setText('검색 기준시: ' + basic_c_stime)

                basic_c_name = c_basic_json.get('character_name')
                self.lb_c_name.setText(basic_c_name)

                # search main/sub charactor function call
                self.is_real_you(basic_c_name, ocid_str, c_basic_json, base_time_str)

                basic_c_server_str = c_basic_json.get('world_name')
                if (basic_c_server_str is not None):
                    basic_c_server = '서버:       ' + basic_c_server_str
                    # server image load function call
                    self.display_s_img(basic_c_server_str)
                else:
                    basic_c_server = '?'
                self.lb_c_server.setText(basic_c_server)

                basic_c_gen = '성별: ' + c_basic_json.get('character_gender') + '캐'
                self.lb_c_gen.setText(basic_c_gen)

                basic_c_class = '직업: ' + c_basic_json.get('character_class')
                self.lb_c_class.setText(basic_c_class)

                # progress bar support only integer type
                basic_c_level = '레벨: ' + str(c_basic_json.get('character_level'))
                self.lb_c_level.setText(basic_c_level)
                basic_c_exp = float(c_basic_json.get('character_exp_rate'))
                basic_c_exp_pb = round(basic_c_exp)
                basic_c_exp = str(basic_c_exp) + '%'
                self.lb_c_exp.setText(basic_c_exp)
                self.pb_exp.setValue(basic_c_exp_pb)
                
                basic_c_gname_str = c_basic_json.get('character_guild_name')
                if (basic_c_gname_str is not None):
                    basic_c_gname = '길드: ' + c_basic_json.get('character_guild_name')
                    self.lb_c_gname.setText(basic_c_gname)
                else:
                    self.lb_c_gname.setText('길드: (없음)')

                # character image
                c_img_url = c_basic_json.get('character_image')
                c_img_res = requests.get(c_img_url)
                if (c_img_res.status_code == 200):
                    c_img_content = Image.open(BytesIO(c_img_res.content))
                    c_img_content = c_img_content.convert("RGBA")
                    c_img_data = c_img_content.tobytes("raw", "RGBA")
                    c_img_qt = QImage(c_img_data, c_img_content.size[0], c_img_content.size[1], QImage.Format_RGBA8888)
                    c_img_pixmap = QPixmap.fromImage(c_img_qt)
                    self.lb_c_img.setPixmap(c_img_pixmap)
                else:
                    self.lb_c_img.setText(str(c_img_res.status_code))
            else:
                search_log += '1: 캐릭터 기본 정보 조회 실패 GET(' + str(c_basic_req.status_code) + ')'
                self.txt_c_log.setPlainText(search_log)
                return


            # character popularity request
            url_str = self.make_c_url('popularity', ocid_str, base_time_str)
            c_pop_req = requests.get(url_str, headers = self.headers)

            if (c_pop_req.status_code == 200):
                c_pop_json = c_pop_req.json()

                pop_c_pop_str = '인기도: ' + str(c_pop_json.get('popularity'))
                self.lb_c_pop.setText(pop_c_pop_str)
            else:
                search_log += '2: 캐릭터 인기도 정보 조회 실패 GET(' + str(c_pop_req.status_code) + ')'
                self.txt_c_log.setPlainText(search_log)
                return


            # character stat request
            url_str = self.make_c_url('stat', ocid_str, base_time_str)
            c_stat_req = requests.get(url_str, headers = self.headers)

            if (c_stat_req.status_code == 200):
                c_stat_json = c_stat_req.json()
                c_stat_obj = c_stat_json.get('final_stat')
                for obj in c_stat_obj:
                    # character stat display function call, stat_value is type(str)
                    self.display_stat(obj.get('stat_name'), obj.get('stat_value'))
            else:
                search_log += '3: 캐릭터 종합 능력치 정보 조회 실패 GET(' + str(c_stat_req.status_code) + ')'
                self.txt_c_log.setPlainText(search_log)
                return


            # character hyper stat request
            url_str = self.make_c_url('hyper-stat', ocid_str, base_time_str)
            c_hyper_req = requests.get(url_str, headers = self.headers)

            if (c_hyper_req.status_code == 200):
                c_hyper_json = c_hyper_req.json()
                
                c_hyper_pnum = str(c_hyper_json.get('use_preset_no'))
                self.lb_h_pnum.setText('    적용중인 프리셋: ' + c_hyper_pnum)
                c_hyper_tpnt = int(c_hyper_json.get('use_available_hyper_stat'))
                c_hyper_apnt_tag = 'hyper_stat_preset_' + c_hyper_pnum + '_remain_point'
                c_hyper_apnt = int(c_hyper_json.get(c_hyper_apnt_tag))
                c_hyper_upnt = c_hyper_tpnt - c_hyper_apnt
                self.lb_h_tpnt.setText('총 스탯 포인트: ' + str(c_hyper_tpnt))
                self.lb_h_upnt.setText('사용 스탯 포인트: ' + str(c_hyper_upnt))
                self.lb_h_apnt.setText('잔여 스탯 포인트: ' + str(c_hyper_apnt))

                c_hyper_obj_str = 'hyper_stat_preset_' + c_hyper_pnum
                c_hyper_obj = c_hyper_json.get(c_hyper_obj_str)
                for obj in c_hyper_obj:
                    # character hyper stat display function call, stat_increase is type(str)
                    self.display_hyper_stat(obj.get('stat_type'), obj.get('stat_increase'))
            else:
                search_log += '4: 캐릭터 하이퍼스탯 정보 조회 실패 GET(' + str(c_hyper_req.status_code) + ')'
                self.txt_c_log.setPlainText(search_log)
                return


            # character propensity request
            url_str = self.make_c_url('propensity', ocid_str, base_time_str)
            c_prop_req = requests.get(url_str, headers = self.headers)

            if (c_prop_req.status_code == 200):
                c_prop_json = c_prop_req.json()
                prop_c_chm = str(c_prop_json.get('charm_level'))
                self.lb_pp_chm.setText('매력: ' + prop_c_chm + ' lv')
                prop_c_crm = str(c_prop_json.get('charisma_level'))
                self.lb_pp_crm.setText('카리스마: ' + prop_c_crm + ' lv')
                prop_c_hdc = str(c_prop_json.get('handicraft_level'))
                self.lb_pp_hdc.setText('손재주: ' + prop_c_hdc + ' lv')
                prop_c_ist = str(c_prop_json.get('insight_level'))
                self.lb_pp_ist.setText('통찰력: ' + prop_c_ist + ' lv')
                prop_c_ssb = str(c_prop_json.get('sensibility_level'))
                self.lb_pp_ssb.setText('감성: ' + prop_c_ssb + ' lv')
                prop_c_wln = str(c_prop_json.get('willingness_level'))
                self.lb_pp_wln.setText('의지: ' + prop_c_wln + ' lv')
            else:
                search_log += '5: 캐릭터 성향 정보 조회 실패 GET(' + str(c_prop_req.status_code) + ')'
                self.txt_c_log.setPlainText(search_log)
                return
            

            # character ability request
            url_str = self.make_c_url('ability', ocid_str, base_time_str)
            c_abil_req = requests.get(url_str, headers = self.headers)

            if (c_abil_req.status_code == 200):
                c_abil_json = c_abil_req.json()
                c_abil_obj = c_abil_json.get('ability_info')
                for obj in c_abil_obj:
                    # character ability display function call, ability_no is type(str)
                    self.display_ability(obj.get('ability_no'), obj.get('ability_grade'), obj.get('ability_value'))
            else:
                search_log += '6: 캐릭터 어빌리티 정보 조회 실패 GET(' + str(c_abil_req.status_code) + ')'
                self.txt_c_log.setPlainText(search_log)
                return


            # start: equip list
            self.w_list_item.addItem('=======================================================================================================================')


            # character equip item request - mechanic, evan equipments do not supoort
            url_str = self.make_c_url('item-equipment', ocid_str, base_time_str)
            c_ieq_req = requests.get(url_str, headers = self.headers)

            if (c_ieq_req.status_code == 200):
                c_ieq_json = c_ieq_req.json()
                c_ieq_obj = c_ieq_json.get('item_equipment')
                for obj in c_ieq_obj:
                    # character equip item display function call
                    self.display_equip(obj)

                ieq_title = c_ieq_json.get('title')
                if (ieq_title is not None):
                    ieq_title_txt = ieq_title.get('title_name')
                    self.w_list_item.addItem('칭호: <' + ieq_title_txt + '>')
            else:
                search_log += '7: 캐릭터 장착 장비 정보 조회 실패 GET(' + str(c_ieq_req.status_code) + ')'
                self.txt_c_log.setPlainText(search_log)
                return


            # end: equip list
            self.w_list_item.addItem('=======================================================================================================================')


            # character equip symbol request
            url_str = self.make_c_url('symbol-equipment', ocid_str, base_time_str)
            c_seq_req = requests.get(url_str, headers = self.headers)

            if (c_seq_req.status_code == 200):
                c_seq_json = c_seq_req.json()
                c_seq_obj = c_seq_json.get('symbol')
                for obj in c_seq_obj:
                    # character equip symbol display function call
                    self.display_symbol(obj.get('symbol_name'), obj.get('symbol_level'))
            else:
                search_log += '8: 캐릭터 장착 심볼 정보 조회 실패 GET(' + str(c_seq_req.status_code) + ')'
                self.txt_c_log.setPlainText(search_log)
                return

            # start: skill list
            self.w_list_skill.addItem('=======================================================================================================================')


            # character hyper passive skill request
            url_str = self.make_c_url('skill', ocid_str, base_time_str)
            url_str += '&character_skill_grade=hyperpassive'
            c_hpass_req = requests.get(url_str, headers = self.headers)

            if (c_hpass_req.status_code == 200):
                c_hpass_json = c_hpass_req.json()
                c_hpass_obj = c_hpass_json.get('character_skill')
                if (len(c_hpass_obj) != 0):
                    self.w_list_skill.addItem('[하이퍼 패시브 스킬]')
                    for obj in c_hpass_obj:
                        # character skill display function call
                        self.display_skill(obj)
                    self.w_list_skill.addItem('-----------------------------------------------------------------------------------------------------------------------')
            else:
                search_log += '9: 캐릭터 하이퍼 패시브 스킬 정보 조회 실패 GET(' + str(c_hpass_req.status_code) + ')'
                self.txt_c_log.setPlainText(search_log)
                return


            # character 5-grade skill request
            url_str = self.make_c_url('skill', ocid_str, base_time_str)
            url_str += '&character_skill_grade=5'
            c_5skill_req = requests.get(url_str, headers = self.headers)

            if (c_5skill_req.status_code == 200):
                c_5skill_json = c_5skill_req.json()
                c_5skill_obj = c_5skill_json.get('character_skill')
                if (len(c_5skill_obj) != 0):
                    self.w_list_skill.addItem('[5차 스킬]')
                    for obj in c_5skill_obj:
                        # character skill display function call
                        self.display_skill(obj)
                    self.w_list_skill.addItem('-----------------------------------------------------------------------------------------------------------------------')
            else:
                search_log += '10: 캐릭터 5차 스킬 정보 조회 실패 GET(' + str(c_5skill_req.status_code) + ')'
                self.txt_c_log.setPlainText(search_log)
                return


            # character 6-grade skill request
            url_str = self.make_c_url('skill', ocid_str, base_time_str)
            url_str += '&character_skill_grade=6'
            c_6skill_req = requests.get(url_str, headers = self.headers)

            if (c_6skill_req.status_code == 200):
                c_6skill_json = c_6skill_req.json()
                c_6skill_obj = c_6skill_json.get('character_skill')
                if (len(c_6skill_obj) != 0):
                    self.w_list_skill.addItem('[6차 스킬]')
                    for obj in c_6skill_obj:
                        # character skill display function call
                        self.display_skill(obj)
                    self.w_list_skill.addItem('-----------------------------------------------------------------------------------------------------------------------')
            else:
                search_log += '11: 캐릭터 6차 스킬 정보 조회 실패 GET(' + str(c_6skill_req.status_code) + ')'
                self.txt_c_log.setPlainText(search_log)
                return
            

            # character 6-stat request
            url_str = self.make_c_url('hexamatrix-stat', ocid_str, base_time_str)
            c_hexastat_req = requests.get(url_str, headers = self.headers)
            
            if (c_hexastat_req.status_code == 200):
                c_hexastat_json = c_hexastat_req.json()
                c_hexastat_obj = c_hexastat_json.get('character_hexa_stat_core')
                if (len(c_hexastat_obj) != 0):
                    self.w_list_skill.addItem('[헥사 스탯]')
                    for obj in c_hexastat_obj:
                        # character 6-stat display function call
                        self.display_hexastat(obj)
            else:
                search_log += '12: 캐릭터 헥사 스탯 정보 조회 실패 GET(' + str(c_hexastat_req.status_code) + ')'
                self.txt_c_log.setPlainText(search_log)
                return
            

            # end: skill list
            self.w_list_skill.addItem('=======================================================================================================================')


            # character dojang request
            url_str = self.make_c_url('dojang', ocid_str, base_time_str)
            c_dojang_req = requests.get(url_str, headers = self.headers)

            if (c_dojang_req.status_code == 200):
                c_dojang_json = c_dojang_req.json()
                c_dojang_floor = c_dojang_json.get('dojang_best_floor')
                c_dojang_rtime = c_dojang_json.get('date_dojang_record')
                if (c_dojang_floor is not None and c_dojang_rtime is not None):
                    c_dojang_rtime = c_dojang_rtime.split('T')[0]
                    c_dojang_floor_str = '무릉: ' + str(c_dojang_floor) + '층 / ' + c_dojang_rtime + ' 갱신'
                    self.lb_c_dojang.setText(c_dojang_floor_str)
                else:
                    c_dojang_floor_str = '무릉: (기록없음)'
                    self.lb_c_dojang.setText(c_dojang_floor_str)
            else:
                search_log += '13: 캐릭터 무릉 정보 조회 실패 GET(' + str(c_dojang_req.status_code) + ')'
                self.txt_c_log.setPlainText(search_log)
                return


            # start: union list
            self.w_list_union.addItem('=======================================================================================================================')


            # character union request
            url_str = self.make_u_url('union', ocid_str, base_time_str)
            u_union_req = requests.get(url_str, headers = self.headers)

            if (u_union_req.status_code == 200):
                u_union_json = u_union_req.json()
                u_union_grade = u_union_json.get('union_grade')
                u_union_level = u_union_json.get('union_level')
                if (u_union_grade is not None and u_union_level is not None):
                    self.w_list_union.addItem('[' + u_union_grade + ']: ' + str(u_union_level) + 'lv')
                    self.w_list_union.addItem('-----------------------------------------------------------------------------------------------------------------------')
                else:
                    self.w_list_union.addItem('유니온 정보 갱신 필요')
            else:
                search_log += '14: 캐릭터 유니온 정보 조회 실패 GET(' + str(u_union_req.status_code) + ')'
                self.txt_c_log.setPlainText(search_log)
                return


            # character union raider request
            url_str = self.make_u_url('union-raider', ocid_str, base_time_str)
            u_raider_req = requests.get(url_str, headers = self.headers)

            if (u_raider_req.status_code == 200):
                u_raider_json = u_raider_req.json()

                u_occupied_list = u_raider_json.get('union_occupied_stat')
                if (len(u_occupied_list) != 0):
                    self.w_list_union.addItem('[공격대 점령 효과]')
                    for obj in u_occupied_list:
                        self.w_list_union.addItem('    ' + obj)
                    self.w_list_union.addItem('-----------------------------------------------------------------------------------------------------------------------')

                u_raider_list = u_raider_json.get('union_raider_stat')
                if (len(u_raider_list) != 0):
                    self.w_list_union.addItem('[공격대원 효과]')
                    for obj in u_raider_list:
                        self.w_list_union.addItem('    ' + obj)
                    
            else:
                search_log += '15: 유니온 효과 조회 실패 GET(' + str(u_raider_req.status_code) + ')'
                self.txt_c_log.setPlainText(search_log)
                return


            # end: union list
            self.w_list_union.addItem('=======================================================================================================================')


            search_end_time = time.time()
            search_log += '검색 성공: ' + f'{search_end_time - search_start_time:.2f} sec'
            self.txt_c_log.setPlainText(search_log)


        else:
            search_log += '0: API 키 또는 캐릭터 갱신/닉네임 입력 확인 - OCID 조회 실패 GET(' + str(ocid_req.status_code) + ')'
            self.txt_c_log.setPlainText(search_log)


####################################################################################################################################################################
# global

if __name__ == "__main__" :
    try:
        app = QApplication(sys.argv)
        myWindow = WindowClass()
        myWindow.show()
        app.exec_()
    except:
        logging.error(traceback.format_exc())