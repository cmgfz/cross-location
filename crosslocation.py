# encoding:utf-8
import sys, sqlite3,os
if hasattr(sys,'frozen'):
    os.environ['PATH'] = sys._MEIPASS +";"+ os.environ['PATH']
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget,QApplication,QStackedWidget
from PyQt5.QtWidgets import QLabel,QComboBox,QLineEdit,QHBoxLayout,QPushButton,QVBoxLayout
#from PyQt5.QtWidgets import *
#from PyQt5.QtCore import *
from PyQt5.QtGui import QIntValidator,QDoubleValidator
from sympy import solve;
from sympy.abc import B, C, x, y, z;
import math;
from math import *;

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.initData()
        self.initEvent()

    def initData(self):
        conn = sqlite3.connect('data.db')
        curs = conn.cursor()
        query = 'SELECT * FROM data'
        curs.execute(query)
        data = curs.fetchall()
        for i in range(len(data)):
            self.station1.addItem(data[i][0])
            self.station2.addItem(data[i][0])
            self.childComboBox.addItem(data[i][0])
        conn.close()
        count2=self.childComboBox.currentIndex()
        self.childLongitude.setText(str(data[count2][1]))
        self.childLatitude.setText(str(data[count2][2]))


    def initEvent(self):
        # location.setCheckable(True)
        self.location.clicked.connect(self.locate)
        self.setting.clicked.connect(self.makesetting)
        self.backBtn.clicked.connect(self.backToMain)
        self.childAdd.clicked.connect(self.toThird)
        self.quitSecond.clicked.connect(self.makesetting)
        self.quitFirst.clicked.connect(self.backToMain)
        self.thirdConfirm.clicked.connect(self.Confirm)
        self.childComboBox.currentIndexChanged.connect(self.comboxChanged3)
        self.childChange.clicked.connect(self.makechildChange)
        self.childDelete.clicked.connect(self.makechildDelete)

    def initUI(self):
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("favicon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.setWindowTitle("交叉定位")
        # 设置字体
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(14)
        # 定义第一行表单
        self.label1 = QLabel('站名')
        self.label1.setFont(font)
        self.station1 = QComboBox()
        self.label3 = QLabel('方位')
        self.label3.setFont(font)
        self.direction1 = QLineEdit()
        self.label5 = QLabel('距离')
        self.label5.setFont(font)
        self.distance1 = QLineEdit()
        self.label7 = QLabel('经度E')
        self.label7.setFont(font)
        self.longitude = QLineEdit()
        self.station1Widget = QWidget()
        station1Layout = QHBoxLayout()
        #station1Layout.addStretch(1)
        station1Layout.addWidget(self.label1)
        station1Layout.addWidget(self.station1)
        station1Layout.addWidget(self.label3)
        station1Layout.addWidget(self.direction1)
        station1Layout.addWidget(self.label5)
        station1Layout.addWidget(self.distance1)
        station1Layout.addWidget(self.label7)
        station1Layout.addWidget(self.longitude)
        #station1Layout.addStretch(1)
        self.station1Widget.setLayout(station1Layout)
        # 定义第二行表单
        self.label2 = QLabel('站名')
        self.label2.setFont(font)
        self.station2 = QComboBox()
        self.label4 = QLabel('方位')
        self.label4.setFont(font)
        self.direction2 = QLineEdit()
        self.label6 = QLabel('距离')
        self.label6.setFont(font)
        self.distance2 = QLineEdit()
        self.label8 = QLabel('纬度N')
        self.label8.setFont(font)
        self.latitude = QLineEdit()
        self.station2Widget = QWidget()
        station2Layout = QHBoxLayout()
        #station2Layout.addStretch(1)
        station2Layout.addWidget(self.label2)
        station2Layout.addWidget(self.station2)
        station2Layout.addWidget(self.label4)
        station2Layout.addWidget(self.direction2)
        station2Layout.addWidget(self.label6)
        station2Layout.addWidget(self.distance2)
        station2Layout.addWidget(self.label8)
        station2Layout.addWidget(self.latitude)
        #station2Layout.addStretch(1)
        self.station2Widget.setLayout(station2Layout)
        # 定义底部按钮
        bottomLayout = QHBoxLayout()
        self.setting = QPushButton("站点设置")
        self.location = QPushButton("交叉定位")
        bottomLayout.addWidget(self.setting)
        bottomLayout.addWidget(self.location)

        # 主窗口总布局
        self.totalWidget = QWidget()
        totallayout = QVBoxLayout()
        totallayout.addStretch(1)
        totallayout.addWidget(self.station1Widget)
        totallayout.addWidget(self.station2Widget)
        totallayout.addLayout(bottomLayout)
        totallayout.addStretch(1)
        self.totalWidget.setLayout(totallayout);

        # 子窗口总布局
        self.childWidget = QWidget()
        self.childLabel1 = QLabel('经度')
        self.childLabel2 = QLabel('纬度')
        self.childLongitude = QLineEdit()
        self.childLatitude = QLineEdit()
        self.backBtn = QPushButton("返回主窗口")
        self.childComboBox = QComboBox()
        self.childAdd = QPushButton("增加站点")
        self.childChange = QPushButton("修改")
        self.childDelete = QPushButton("删除")
        # not use QVBoxLayout
        childTotalLayout = QHBoxLayout()
        # childTotalLayout.addStretch(1)
        childTotalLayout.addWidget(self.childComboBox)
        childTotalLayout.addWidget(self.childLabel1)
        childTotalLayout.addWidget(self.childLongitude)
        childTotalLayout.addWidget(self.childLabel2)
        childTotalLayout.addWidget(self.childLatitude)
        childTotalLayout.addWidget(self.childAdd)
        childTotalLayout.addWidget(self.childChange)
        childTotalLayout.addWidget(self.childDelete)
        childTotalLayout.addWidget(self.backBtn)
        # childTotalLayout.addStretch(1)
        self.childWidget.setLayout(childTotalLayout)

        # 二级子窗口布局
        self.thirdWidget = QWidget()
        self.thirdLabel1 = QLabel('站点')
        self.thirdStation = QLineEdit()
        self.thirdLabel2 = QLabel('经度')
        self.thirdLongitude = QLineEdit()
        self.thirdLabel3 = QLabel('纬度')
        self.thirdLatitude = QLineEdit()
        self.thirdConfirm = QPushButton("确定")
        self.quitSecond = QPushButton("返回二级窗口")
        self.quitFirst = QPushButton("返回一级窗口")
        thirdTotalLayout = QHBoxLayout()
        thirdTotalLayout.addWidget(self.thirdLabel1)
        thirdTotalLayout.addWidget(self.thirdStation)
        thirdTotalLayout.addWidget(self.thirdLabel2)
        thirdTotalLayout.addWidget(self.thirdLongitude)
        thirdTotalLayout.addWidget(self.thirdLabel3)
        thirdTotalLayout.addWidget(self.thirdLatitude)
        thirdTotalLayout.addWidget(self.thirdConfirm)
        thirdTotalLayout.addWidget(self.quitSecond)
        thirdTotalLayout.addWidget(self.quitFirst)
        self.thirdWidget.setLayout(thirdTotalLayout)

        # 定义堆叠窗口部件
        self.stackedWidget = QStackedWidget()
        self.stackedWidget.addWidget(self.totalWidget)
        self.stackedWidget.addWidget(self.childWidget)
        self.stackedWidget.addWidget(self.thirdWidget)
        
        #定义校验器
        intValidator1=QIntValidator(self)
        intValidator1.setRange(0,1800000)        
        self.childLongitude.setValidator(intValidator1)
        self.thirdLongitude.setValidator(intValidator1)
        intValidator2=QIntValidator(self)
        intValidator2.setRange(0,900000)
        self.childLatitude.setValidator(intValidator2)
        self.thirdLatitude.setValidator(intValidator2)
        doubleValidator=QDoubleValidator(self)
        doubleValidator.setRange(0,360)
        doubleValidator.setNotation(QDoubleValidator.StandardNotation)
        doubleValidator.setDecimals(2)
        self.direction1.setValidator(doubleValidator)
        self.direction2.setValidator(doubleValidator)

        # 插入定义好的堆叠窗口部件
        layout = QHBoxLayout()
        layout.addWidget(self.stackedWidget)
        self.setLayout(layout)

    def makesetting(self):
        self.stackedWidget.setCurrentIndex(1)

    def backToMain(self):
        self.stackedWidget.setCurrentIndex(0)

    def toThird(self):
        self.stackedWidget.setCurrentIndex(2)
            
    def locate(self):
        try:
            conn = sqlite3.connect('data.db')
            curs = conn.cursor()
            query = 'SELECT * FROM data'
            curs.execute(query)
            data = curs.fetchall()
            count1 = self.station1.currentIndex()
            j1 = data[count1][1]
            f1 = self.direction1.text()
            w1 = data[count1][2]
            count2 = self.station2.currentIndex()
            j2 = data[count2][1]
            f2 = self.direction2.text()
            w2 = data[count2][2]
            R = 6371
            j1 = j1 // 10000 + (j1 % 10000 // 100 / 60) + j1 % 100 / 3600
            w1 = w1 // 10000 + (w1 % 10000 // 100 / 60) + w1 % 100 / 3600
            j2 = j2 // 10000 + (j2 % 10000 // 100 / 60) + j2 % 100 / 3600
            w2 = w2 // 10000 + (w2 % 10000 // 100 / 60) + w2 % 100 / 3600
            j1 = radians(float(j1));
            w1 = radians(float(w1));
            f1 = radians(float(f1));
            j2 = radians(float(j2));
            w2 = radians(float(w2));
            f2 = radians(float(f2));
            # calculate the three point to get the first surface
            x1 = math.cos(j1) * math.cos(w1) * R
            y1 = math.sin(j1) * math.cos(w1) * R
            z1 = math.sin(w1) * R
            x2 = math.cos(j2) * math.cos(w2) * R
            y2 = math.sin(j2) * math.cos(w2) * R
            z2 = math.sin(w2) * R
            # a=solve([x**2+y**2+z**2-R**2,(z-R*math.sin(math.radians(w1)))*math.tan(math.radians(f1))-x*math.tan(math.radians(j1)),
            # (z-R*math.sin(math.radians(w2)))*math.tan(math.radians(f2))-x*math.tan(math.radians(j2))],[x,y,z]);
            # x+By+Cz=0
            a = solve([x1 + B * y1 + C * z1, z1 * (1 - cos(f1)) * x1 / sin(w1) / R - y1 * sin(f1) / sin(w1) \
                       + (z1 * (1 - cos(f1)) * y1 / sin(w1) / R + x1 * sin(f1) / sin(w1)) * B + (
                               z1 * (1 - cos(f1)) * z1 / sin(w1) / R + R * cos(f1) / sin(w1)) * C], [B, C])
            # print(a);
            B1, C1 = a[B], a[C]
            b = solve([x2 + B * y2 + C * z2, z2 * (1 - cos(f2)) * x2 / sin(w2) / R - y2 * sin(f2) / sin(w2) \
                       + (z2 * (1 - cos(f2)) * y2 / sin(w2) / R + x2 * sin(f2) / sin(w2)) * B + (
                               z2 * (1 - cos(f2)) * z2 / sin(w2) / R + R * cos(f2) / sin(w2)) * C], [B, C])
            # print(b);
            B2, C2 = b[B], b[C]
            # print(B2)
            c = solve([x ** 2 + y ** 2 + z ** 2 - R ** 2, x + B1 * y + C1 * z, x + B2 * y + C2 * z], [x, y, z])
            # print(c)
            x3, y3, z3 = c[0][0], c[0][1], c[0][2]
            w = asin(z3 / R)
            j = pi + atan(y3 / x3)
            d1 = R * (acos(sin(w1) * sin(w) + cos(w1) * cos(w) * cos(j1 - j)))
            d1=round(d1,2)
            d2 = R * (acos(sin(w2) * sin(w) + cos(w2) * cos(w) * cos(j2 - j)))
            d2=round(d2,2)
            j = degrees(j)
            w = degrees(w)
            z1=int((j - int(j // 1)) * 60 // 1)
            z2=int((j - int(j // 1)) * 60 % 1 * 60 // 1)
            z3=int((w - int(w // 1)) * 60 // 1)
            z4=int((w - int(w // 1)) * 60 % 1 * 60 // 1)
            j = str(int(j // 1)) + str(z1).zfill(2)+str(z2).zfill(2)
            w = str(int(w // 1)) + str(z3).zfill(2)+str(z4).zfill(2)
            result = (j, w, d1, d2)
            self.longitude.setText(str(result[0]))
            self.latitude.setText(str(result[1]))
            self.distance1.setText(str(result[2]))
            self.distance2.setText(str(result[3]))
        except:
            pass
 
    def Confirm(self):
        conn = sqlite3.connect('data.db')
        curs = conn.cursor()
        query = 'INSERT INTO data VALUES ("%s","%d","%d")' %(self.thirdStation.text(),int(self.thirdLongitude.text()),int(self.thirdLatitude.text()))
        curs.execute(query)
        self.station1.clear()
        self.station2.clear()
        self.childComboBox.clear()
        query = 'SELECT * FROM data'
        curs.execute(query)
        data = curs.fetchall()
        for i in range(len(data)):
            self.childComboBox.addItem(data[i][0])
            self.station1.addItem(data[i][0])
            self.station2.addItem(data[i][0])        
        conn.commit()
        conn.close()

    def comboxChanged3(self):
        conn = sqlite3.connect('data.db')
        curs = conn.cursor()
        query = 'SELECT * FROM data'
        curs.execute(query)
        data = curs.fetchall()        
        count2=self.childComboBox.currentIndex()
        self.childLongitude.setText(str(data[count2][1]))
        self.childLatitude.setText(str(data[count2][2]))

    def makechildChange(self):
        conn = sqlite3.connect('data.db')
        curs = conn.cursor()
        query='UPDATE data SET (longitude,latitude)=("%d","%d") WHERE station="%s"' %(int(self.childLongitude.text()),\
                                                                                      int(self.childLatitude.text()),self.childComboBox.currentText())
        curs.execute(query)
        conn.commit()
        conn.close()

    def makechildDelete(self):
        conn = sqlite3.connect('data.db')
        curs = conn.cursor()
        query='DELETE FROM data WHERE station="%s"' %(self.childComboBox.currentText())
        curs.execute(query)
        self.station1.clear()
        self.station2.clear()
        self.childComboBox.clear()
        query = 'SELECT * FROM data'
        curs.execute(query)
        data = curs.fetchall()
        for i in range(len(data)):
            self.childComboBox.addItem(data[i][0])
            self.station1.addItem(data[i][0])
            self.station2.addItem(data[i][0])
        conn.commit()
        conn.close()

if __name__ == '__main__':
        app = QApplication(sys.argv)
        ex = Example()
        ex.show()
        sys.exit(app.exec_())

