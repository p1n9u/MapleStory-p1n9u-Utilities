import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

# added lib
import os
import sys
import winsound
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QDateTime, Qt
from PyQt5.QtCore import QTimer, QTime

# added func
def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# UI connection
form = resource_path("resources/ui/RHUI.ui")
form_class = uic.loadUiType(form)[0]

class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        # init
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(resource_path("resources/icon/potion.ico")))
        datetime = QDateTime.currentDateTime()
        self.lb_livetime_value.setText(datetime.toString('hh:mm:ss - yy년 MM월 dd일'))
        logo_img = QPixmap(resource_path("resources/img/logo.png"))
        self.lb_logo.setPixmap(logo_img)
        git_logo_img = QPixmap(resource_path("resources/img/github_logo.png"))
        self.lb_git_logo.setPixmap(git_logo_img)
        self.lb_dev_link.setText('<a href="https://github.com/p1n9u/MapleStory_Wealth_Acquisition_Timer">Link</a>')
        self.lb_dev_link.setOpenExternalLinks(True)
        self.setFixedSize(850, 720)

        self.wavlist = [
            "p",
            resource_path("resources/wav/aquarium.wav"), #1
            resource_path("resources/wav/title.wav"), #2
            resource_path("resources/wav/henesys.wav"), #3
            resource_path("resources/wav/sleepywood.wav"), #4
            resource_path("resources/wav/shop.wav"), #5
            resource_path("resources/wav/ellinia.wav"), #6
            resource_path("resources/wav/spotlight.wav"), #7
            resource_path("resources/wav/ludibrium.wav"), #8
            resource_path("resources/wav/starbubble.wav"), #9
            resource_path("resources/wav/orbis.wav"), #10
            resource_path("resources/wav/lithharbor.wav"), #11
            resource_path("resources/wav/coketown.wav"), #12
            resource_path("resources/wav/nxlogo.wav"), #13
        ]

        ## Livetime
        self.livetime_timer = QTimer(self)
        self.livetime_timer.setInterval(1000)
        self.livetime_timer.timeout.connect(self.display_livetime)
        self.livetime_timer.start()

        ## RHtime
        self.rh_cnt = 0
        self.pb_val = 0
        self.rhtime_timer = QTimer(self)
        self.rhtime_timer.setInterval(1000)
        self.rhtime_timer.timeout.connect(self.activate_rh)

        ## PPtime
        self.pptime_timer = QTimer(self)
        self.pptime_timer.setInterval(1000)
        self.pptime_timer.timeout.connect(self.activate_pp)

        ## EXPtime
        self.exp_cnt = 0
        self.exptime_timer = QTimer(self)
        self.exptime_timer.setInterval(1000)
        self.exptime_timer.timeout.connect(self.activate_exp)

        ## timer value
        self.total = 0
        self.ss = 0
        self.mm = 0
        self.hh = 0

        ## EXP timer value
        self.exptotal = 0
        self.expss = 0
        self.expmm = 0
        self.exphh = 0

        ## PP timer value
        self.ppdec = 90

        # event handle
        self.btn_start.clicked.connect(self.clicked_startbtn)
        self.btn_reset.clicked.connect(self.clicked_resetbtn)
        self.btn_start_exp.clicked.connect(self.clicked_expstartbtn)
        self.btn_reset_exp.clicked.connect(self.clicked_expresetbtn)
        self.btn_start_pp.clicked.connect(self.clicked_ppstartbtn)
        self.btn_reset_pp.clicked.connect(self.clicked_ppresetbtn)

    # event functions

    def display_livetime(self):
        datetime = QDateTime.currentDateTime()
        self.lb_livetime_value.setText(datetime.toString('hh:mm:ss - yy년 MM월 dd일'))

    def clicked_startbtn(self):
        self.rhtime_timer.start()
        self.lb_alarm_info.setText("Start, be Munchi!")

    def clicked_resetbtn(self):
        self.rhtime_timer.stop()
        self.rh_cnt = 0
        self.total = 0
        self.ss = 0
        self.mm = 0
        self.hh = 0
        self.lb_rhtime_value.setText("0:00:00")
        self.lb_rhcnt_value.setText("0")
        self.pb_val = 0
        self.pb_rhstatus.setValue(0)
        self.lb_alarm_info.setText("Reset done, harvest again")

    def activate_rh(self):
        alarm_flag = 0
        alarm_str = ""

        self.total += 1
        self.ss += 1
        self.pb_val += 1
        self.pb_rhstatus.setValue(self.pb_val)

        if ( self.total%7200 == 0 ):
            self.pb_val = 0
            self.pb_rhstatus.setValue(self.pb_val)

        if (self.ss == 60):
            self.mm += 1
            self.ss = 0

        if (self.mm == 60):
            self.hh += 1
            self.mm = 0

        rht_string = "{0}:{1:02}:{2:02}".format(self.hh, self.mm, self.ss)
        self.lb_rhtime_value.setText(rht_string)

        if ( self.cb_0025.isChecked() and ((self.total+5)%30) == 0 ):
            alarm_flag = 1
            alarm_str += "스킬 "
        if ( self.cb_0035.isChecked() and ((self.total+5)%40) == 0 ):
            alarm_flag = 1
            alarm_str += "스킬 "
        if ( self.cb_0045.isChecked() and ((self.total+5)%50) == 0 ):
            alarm_flag = 1
            alarm_str += "스킬 "
        if ( self.cb_0145.isChecked() and ((self.total+5)%150) == 0 ):
            alarm_flag = 1
            alarm_str += "스킬 "
        if ( self.cb_0195.isChecked() and ((self.total+5)%200) == 0 ):
            alarm_flag = 1
            alarm_str += "스킬 "
        if ( self.cb_0295.isChecked() and ((self.total+5)%300) == 0 ):
            alarm_flag = 1
            alarm_str += "스킬 "
        if ( self.cb_0055.isChecked() and ((self.total+5)%60) == 0 ):
            alarm_flag = 2
            alarm_str += "1분 "
        if ( self.cb_0115.isChecked() and ((self.total+5)%120) == 0 ):
            alarm_flag = 3
            alarm_str += "2분 "
        if ( self.cb_0175.isChecked() and ((self.total+5)%180) ==0 ):
            alarm_flag = 4
            alarm_str += "3분 "
        if ( self.cb_0100.isChecked() and self.total%100==0 ):
            alarm_flag = 5
            alarm_str += "메소 "
        if ( self.cb_0600.isChecked() and self.total%600==0 ):
            alarm_flag = 6
            alarm_str += "10분 "
        if ( self.cb_0900.isChecked() and self.total%900==0 ):
            alarm_flag = 7
            alarm_str += "15분 "
        if ( self.cb_1200.isChecked() and self.total%1200==0 ):
            alarm_flag = 8
            alarm_str += "20분 "
        if ( self.cb_1800.isChecked() and self.total%1800==0 ):
            alarm_flag = 9
            alarm_str += "30분 "
        if ( self.cb_3600.isChecked() and self.total%3600==0 ):
            alarm_flag = 10
            alarm_str += "1시간 "
        if ( self.cb_7200.isChecked() and self.total%7200==0 ):
            alarm_flag = 11
            alarm_str += "2시간 "
            self.rh_cnt += 1
            self.lb_rhcnt_value.setText(str(self.rh_cnt))

        if ( alarm_flag > 0 ):
            winsound.PlaySound(self.wavlist[alarm_flag], winsound.SND_ASYNC)
            self.lb_alarm_info.setText(alarm_str)

    def clicked_expstartbtn(self):
        self.exptime_timer.start()

    def clicked_expresetbtn(self):
        self.exptime_timer.stop()
        self.exptotal = 0
        self.expss = 0
        self.expmm = 0
        self.exphh = 0
        self.lb_exptime_value.setText("0:00:00")
        self.lb_expcnt_value.setText("0")

    def activate_exp(self):
        alarm_flag = 0

        self.exptotal += 1
        self.expss += 1

        if (self.expss == 60):
            self.expmm += 1
            self.expss = 0

        if (self.expmm == 60):
            self.exphh += 1
            self.expmm = 0

        exp_string = "{0}:{1:02}:{2:02}".format(self.exphh, self.expmm, self.expss)
        self.lb_exptime_value.setText(exp_string)

        if ( ((self.exptotal+60)%1800) == 0 ):
            alarm_flag = 12
            self.exp_cnt += 1
            self.lb_expcnt_value.setText(str(self.exp_cnt))

        if ( alarm_flag > 0 ):
            winsound.PlaySound(self.wavlist[alarm_flag], winsound.SND_ASYNC)

    def clicked_ppstartbtn(self):
        self.pptime_timer.start()

    def clicked_ppresetbtn(self):
        self.pptime_timer.stop()
        self.ppdec = 90
        self.lb_pptime_value.setText(str(self.ppdec))

    def activate_pp(self):
        alarm_flag = 0
        self.ppdec -= 1

        self.lb_pptime_value.setText(str(self.ppdec))
        if ( self.ppdec == 0 ):
            self.clicked_ppresetbtn()

        if ( self.ppdec == 20 ):
            alarm_flag = 13

        if ( alarm_flag > 0 ):
            winsound.PlaySound(self.wavlist[alarm_flag], winsound.SND_ASYNC)

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()