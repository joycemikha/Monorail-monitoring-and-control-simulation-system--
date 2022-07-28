import os
from lib2to3.pgen2.token import EQUAL
import math
from train import train
from ECs import ec
from collections import defaultdict
from re import M
from tracemalloc import start
from matplotlib.pyplot import draw, flag
import pygame
from pygame.locals import *
import mysql.connector
import sys
import time
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from Control import Ui_Dialog
import realtime
import webbrowser
import pygame.mixer
import re
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog , QApplication
from datetime import datetime
import tkinter
pygame.display.set_caption('Monorail')
app = QtWidgets.QApplication(sys.argv)
SCREENSIZE = tkinter.Tk()
Dialog = QtWidgets.QDialog()
ui = Ui_Dialog()
ui.setupUi(Dialog)
EC_list=["516","517","518","816","817","818"]

ui.comboBox.addItems(EC_list)
ui.comboBox_2.addItems(["Emergency center 1", "Emergency center 2", "Emergency center 3", "Emergency center 4"])
pygame.init()
sound = pygame.mixer.Sound('EmergencyAlertSound.mp3')
def dynamicwinpos(x=0, y=30):
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
#==========================================================
#   all about the screen and background and icon
#==========================================================
icon = pygame.image.load('Picture2.png')
pygame.display.set_icon(icon)
width = 1500
height = 700
width2 = SCREENSIZE.winfo_screenwidth()
height2 = SCREENSIZE.winfo_screenheight()
x , y = (0.26* 700)-(0.25*700), 0.35* height2-(0.35*700)
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
screen = pygame.display.set_mode((width, height),10 ,20)
pygame.init()
linecolor = 161, 39, 72
linecolor1 = 33, 33, 163
bgcolor = 214, 219, 223
bg = pygame.image.load("map3.jpg")
bg = pygame.transform.scale(bg, (width, height))
screen = pygame.display.set_mode((width, height),pygame.RESIZABLE)
bl_color= 235, 33, 33

#==========================================================
#==========================================================
#==========================================================
#==========================================================
def gotoscreen1():
        print("hello")
        widget.setVisible(True)
        Dialog.hide()
        mainWindow2=MainWindow()
        widget.addWidget(mainWindow2)
        widget.setCurrentIndex(widget.currentIndex()+1)
ui.pushButton_22.clicked.connect(gotoscreen1)

class MainWindow(QDialog):
    f=0
    def __init__(self):
        super(MainWindow,self).__init__()
        loadUi("New_Login.ui",self)
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        widget.setWindowTitle("LogIn")
        self.pushButton.clicked.connect(self.buttonclicked)

    def buttonclicked(self):
        username = self.lineEdit.text() #UserName
        userpassword = self.lineEdit_2.text() #Password
        print(username,userpassword)
        data = (username,userpassword)
        cursor = conn.cursor()
        csql = "SELECT * FROM  operator where  OP_username = %s and OP_password = %s"
        cursor.execute(csql,data)
        result = cursor.fetchall()

        csql2 = "SELECT * FROM  Admins where  Admin_username = %s and Admin_password = %s"
        cursor.execute(csql2,data)
        result2 = cursor.fetchall()

        if result:
            now = datetime.now()
            csql = "SELECT OP_username FROM  operator where  OP_username = %s and OP_password = %s"
            cursor.execute(csql,data)
            OP_user = cursor.fetchone()

            csql = "SELECT OP_password FROM  operator where  OP_username = %s and OP_password = %s"
            cursor.execute(csql,data)
            Op_pass = cursor.fetchone()

            username5 = [str(OP_user[0])]
            operatorpass5=[str(Op_pass[0])]
            logintime=[now]
            cursor = conn.cursor()
            csql = "INSERT IGNORE INTO logins(Login_Username,Login_Password,Login_Time) VALUES (%s,%s,%s)"
            val = (username5[0],operatorpass5[0],logintime[0])
            cursor.execute(csql,val)
            conn.commit()

            widget.setHidden(True)
            Dialog.move(1510, 8)
            Dialog.show()

        elif result2:
            now2 = datetime.now()
            csql = "SELECT Admin_username FROM  admins where  Admin_username = %s and Admin_password = %s"
            cursor.execute(csql,data)
            Ad_user = cursor.fetchone()

            csql = "SELECT Admin_password FROM  admins where  Admin_username = %s and Admin_password = %s"
            cursor.execute(csql,data)
            Ad_pass = cursor.fetchone()

            Adusername = [str(Ad_user[0])]
            ADpass=[str(Ad_pass[0])]
            logintime2=[now2]
            cursor = conn.cursor()
            csql = "INSERT IGNORE INTO logins(Login_Username,Login_Password,Login_Time) VALUES (%s,%s,%s)"
            val = (Adusername[0],ADpass[0],logintime2[0])
            cursor.execute(csql,val)
            conn.commit()

            screen2=Screen2()
            widget.addWidget(screen2)
            widget.setCurrentIndex(widget.currentIndex()+1)
            widget.setWindowTitle("SignUp")
        else:
            print("failure")

class Screen2(QDialog):
    def __init__(self):
        super(Screen2,self).__init__()
        loadUi("New_SignUp.ui",self)
        #userinput = self.lineditname.text()
        self.lineEdit_4.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pushButton_2.clicked.connect(self.gotoscreen1)
        self.pushButton.clicked.connect(self.buttonclicked)
        #self.pushButton.clicked.connect(self.label.setText('Button clicked.'))

    def buttonclicked(self):
        userinput2 = self.lineEdit_2.text() #UserName
        userinput3 = self.lineEdit_3.text() #Operator Name
        userinput4 = self.lineEdit_4.text() #operator password
        print(userinput2,userinput3,userinput4)

        username = [str(userinput2)]
        operatorname=[str(userinput3)]
        operatorpassword=[str(userinput4)]
        cursor = conn.cursor()
        csql = "INSERT IGNORE INTO operator(OP_username,OP_name,OP_password) VALUES (%s,%s,%s)"
        val = (username[0],operatorname[0],operatorpassword[0])
        cursor.execute(csql,val)
        conn.commit()

    def gotoscreen1(self):
        mainWindow=MainWindow()
        widget.addWidget(mainWindow)
        widget.setCurrentIndex(widget.currentIndex()+1)

widget=QtWidgets.QStackedWidget()
mainWindow=MainWindow()
widget.addWidget(mainWindow)
widget.setWindowFlags(QtCore.Qt.FramelessWindowHint)
widget.setAttribute(QtCore.Qt.WA_TranslucentBackground)
widget.setFixedHeight(600)
widget.setFixedWidth(950)
widget.show()

class Graph:
    def __init__(self):

        self.edges = defaultdict(list)
        self.weights = {}

    def add_edge(self, from_node, to_node, weight):
        # Note: assumes edges are bi-directional
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.weights[(from_node, to_node)] = weight
        self.weights[(to_node, from_node)] = weight

    def shortpath(graph, initial, end):
        # shortest paths is a dict of nodes
        # whose value is a tuple of (previous node, weight)
        shortest_paths = {initial: (None, 0)}
        current_node = initial
        visited = set()
        path = []
        while current_node != end:
            visited.add(current_node)
            destinations = graph.edges[current_node]
            weight_to_current_node = shortest_paths[current_node][1]

            for next_node in destinations:
                weight = graph.weights[(current_node, next_node)] + weight_to_current_node
                if next_node not in shortest_paths:
                    shortest_paths[next_node] = (current_node, weight)
                else:
                    current_shortest_weight = shortest_paths[next_node][1]
                    if current_shortest_weight > weight:
                        shortest_paths[next_node] = (current_node, weight)

            next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
            if not next_destinations:
                return "Route Not Possible"
            # next node is the destination with the lowest weight
            current_node = min(next_destinations, key=lambda k: next_destinations[k][1])

        # Work back through destinations in shortest path

        while current_node is not None:
            path.append(current_node)
            next_node = shortest_paths[current_node][0]
            current_node = next_node
        # Reverse path
        path = path[::-1]
        return path

graph = Graph()
edges = [
    #EM2
    #route1
    ('A', 'B', 410),
    ('B', 'E', 205),
    #route 2
    ('A', 'B1', 183),
    ('B1', 'E', 260),
    #EM1
    #route1
    ('X', 'Y', 205),
    ('Y', 'E2', 88),
    #route 2
    ('X', 'Y1', 120),
    ('Y1', 'E2', 140),
    #route 3
    ('X', 'Y2', 60),
    ('Y2', 'E2', 236),
    #EM3
    #route1
    ('W', 'F', 185),
    ('F', 'E3', 149),
    # route2
    ('W', 'F1', 250),
    ('F1', 'E3', 149),
    # route3
    ('W', 'F2', 210),
    ('F2', 'E3', 153),
    # EM4
    # route1
    ('M', 'K', 203),
    ('K', 'E4', 245),
    # route2
    ('M', 'K1', 188),
    ('K1', 'E4', 330),
    # route3
    ('M', 'K2', 455),
    ('K2', 'E4', 360),
]
for edge in edges:
    graph.add_edge(*edge)

newx = 1
newy = 1
class emergency:
    def __init__(self,id):
        self.T1 = 1160
        self.R1 = 132
        self.T2 = 595
        self.T22 = 595
        self.T222 = 595
        self.R2 = 195
        self.R22 = 195
        self.R222 = 195
        self.T33 = 1255
        self.R3 = 525
        self.T3 = 1255
        self.R33 = 525
        self.T333 = 1255
        self.R333 = 525
        self.T4 = 350
        self.R4 = 545
        self.T444 = 350
        self.R444 = 545
        self.T44 = 350
        self.R44 = 545
        self.T5 = 1162
        self.R5 = 132
        self.T2 = 595
        self.R2 = 195
        self.id=id
        self.r=255
        self.h=255
        self.r1=0
        self.h1=0
        self.a=255
        self.b=255
        self.a1=0
        self.b1=0
        self.c=255
        self.d=255
        self.c1=0
        self.d1=0
        self.e=255
        self.f=255
        self.e1=0
        self.f1=0
        self.help=0
        self.newt=421
        self.newr=119
        self.newt1=360
        self.newr1=119
        self.newt22=282
        self.newr22=42
        self.newt2=410
        self.newr2=190
        self.newt33=313
        self.newr33=195
        self.newt3=625
        self.newr3=310
        self.newt4=675
        self.newr4=155
        self.newt14=410
        self.newr14=420
        self.newt34=760
        self.newr34=550
        self.newt44=480
        self.newr44=515
        self.newt5=985
        self.newr5=210
        self.newt6=790
        self.newr6=71
        self.newt221=903
        self.newr221=124
        self.newt222=790
        self.newr222=170
        self.newt2222=1265
        self.newr2222=87
        self.newt7=1070
        self.newr7=585
        self.newt8=900
        self.newr8=460
        self.newt88=1297
        self.newr88=437
        self.newt888=1197
        self.newr888=595
        self.newt8888 = 1000
        self.newr8888 = 503
        self.newt88888 = 1080
        self.newr88888 = 511
        self.newt888888 = 890
        self.newr888888 = 593
        self.XR = 255
        self.XR1 = 0
        self.px = 255
        self.px1 = 0
    def draw_line_dashed(surface, color, start_pos, end_pos, width = 1, dash_length = 10, exclude_corners = True):
        # convert tuples to numpy arrays
        start_pos = np.array(start_pos)
        end_pos   = np.array(end_pos)
        # get euclidian distance between start_pos and end_pos
        length = np.linalg.norm(end_pos - start_pos)
        # get amount of pieces that line will be split up in (half of it are amount of dashes)
        dash_amount = int(length / dash_length)
        # x-y-value-pairs of where dashes start (and on next, will end)
        dash_knots = np.array([np.linspace(start_pos[i], end_pos[i], dash_amount) for i in range(2)]).transpose()
        return [pygame.draw.line(surface, color, tuple(dash_knots[n]), tuple(dash_knots[n+1]), width)
                for n in range(int(exclude_corners), dash_amount - int(exclude_corners), 2)]

    def route(self):
        global newx
        global newy
        global reroutee
        global reroutee2
        global reroutee3
        global reroutee4
        #x=max(len(twest),len(twest))
        for i in range(len(twest)):
            if(twest[i].flagStop==1):

                if(twest[i].x < newx * 680 and twest[i].y <newy * 320):
                    if (self.r==255 and self.h==255):
                        self.r1 = -5
                        self.h1 = -5
                    elif (self.r==0 and self.h==0):
                        self.r1 = 5
                        self.h1 = 5
                    self.r = self.r + self.r1
                    self.h = self.h + self.h1
                    Graph.shortpath(graph, 'X', 'E2')
                    if (Graph.shortpath(graph, 'X', 'E2') == ['X', 'Y', 'E2'] or counter == 2 ):
                        # route1
                        emergency.draw_line_dashed(screen, (255, 128, 0), (newx * 420, newy * 195), (newx * 625,newy * 195), 4)  # 205
                        emergency.draw_line_dashed(screen, (255, 128, 0), (newx * 420, newy * 195), (newx * 420, newy * 283), 4)  # 88
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.T2, newy * self.R2), 5, 0)
                        if (self.T2 <= 595 and self.T2 > 422):
                            self.T2 = self.T2 - 0.3
                        elif (self.T2 <= 422 and self.R2 >= 195 and self.R2 < 278):
                            self.R2 = self.R2 + 0.3
                    if (Graph.shortpath(graph, 'X', 'E2') == ['X', 'Y1', 'E2'] and counter == 1):
                        # route2
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 490,newy * 195), (newx * 600, newy * 195), 4)  # 110
                        pygame.draw.line(screen, (204, 0, 102), (newx * 490, newy * 195), (newx * 490, newy * 205), 4)  # 10
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx *490,newy * 206), (newx * 520, newy * 206), 4)  # 30
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx *526,newy * 206), (newx * 526 , newy * 300), 4)  # 94
                        pygame.draw.line(screen, (204, 0, 102), (newx * 526, newy * 310), (newx * 510, newy * 310), 4)  # 16
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.T22, newy * self.R22), 5, 0)

                        if (self.T22 <= 595 and self.T22 >= 492 and self.R22 >= 195 and self.R22 < 208):
                            self.T22 = self.T22 - 0.3
                        elif (self.T22 < 492 and self.R22 < 208):
                            self.R22 = self.R22 + 0.3
                        elif (self.T22 < 527 and self.R22 >= 208 and self.R22 < 310):
                            self.T22 = self.T22 + 0.3
                        elif (self.T22 >= 527 and self.R22 >= 208 and self.R22 < 310):
                            self.R22 = self.R22 + 0.3
                        elif (self.R22 >= 310 and self.T22 <= 528 and self.T22 >= 515):
                            self.T22 = self.T22 - 0.3

                    if (Graph.shortpath(graph, 'X', 'E2') == ['X', 'Y2', 'E2'] or counter == 3):
                        # route3
                        emergency.draw_line_dashed(screen, (0, 102, 102), (newx * 580,newy * 195), (newx * 640,newy * 195), 4)  # 60
                        pygame.draw.arc(screen, (0, 102, 102), [ newx * 624, newy * 200, 17, 17], 0, 3.14 / 2, 3)
                        pygame.draw.arc(screen, (0, 102, 102), [newx * 624, newy * 200, 17, 17], 3 * 3.14 / 2, 2 * 3.14, 3)
                        emergency.draw_line_dashed(screen, (0, 102, 102), (newx * 630, newy * 210), (newx * 630, newy * 316), 4)  # 106
                        emergency.draw_line_dashed(screen, (0, 102, 102), (newx * 500, newy * 310), (newx * 630, newy * 310), 4)  # 130
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.T222, newy * self.R222), 5, 0)  # train

                        if (self.T222 >= 595 and self.T222 < 630 and self.R222 == 195):
                            self.T222 = self.T222 + 0.3
                        elif (self.R222 >= 195 and self.R222 < 310):
                            self.R222 = self.R222 + 0.3
                        elif (self.R222 >= 310 and self.T222 > 505):
                            self.T222 = self.T222 - 0.3
                    if EC1[0].ex == 580 and EC1[0].ey == 185:
                        reroutee=0
                    if EC1[0].ex == 430 and EC1[0].ey == 119:
                        reroutee=1
                        emergency.draw_line_dashed(screen, (250, 1, 203), (newx * 420,newy * 119), (newx * 420,newy * 280), 4)#rnew1
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt, newy * self.newr), 5, 0)  # train
                        if (self.newr < 266):
                            self.newr = self.newr + 0.3
                    if EC1[0].ex == 355 and EC1[0].ey == 119:
                        reroutee=1
                        emergency.draw_line_dashed(screen, (250, 1, 203), (newx * 350,newy * 119), (newx * 403,newy * 119), 4)#rnew1
                        emergency.draw_line_dashed(screen, (250, 1, 203), (newx * 403,newy * 119), (newx * 403,newy * 270), 4)#rnew1
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt1, newy * self.newr1), 5, 0)  # train
                        if (self.newt1 < 402):
                            self.newt1 = self.newt1 + 0.3
                        if (self.newt1 >= 402 and self.newr1 < 268):
                            self.newr1 = self.newr1 + 0.3
                    if EC1[0].ex == 275 and EC1[0].ey == 55:
                        reroutee=1
                        emergency.draw_line_dashed(screen, (250, 1, 203), (newx * 275,newy * 40), (newx * 403,newy * 40), 4)#rnew1
                        emergency.draw_line_dashed(screen, (250, 1, 203), (newx * 403,newy * 40), (newx * 403,newy * 270), 4)#rnew1
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt22, newy * self.newr22), 5, 0)  # train
                        if (self.newt22 < 402):
                            self.newt22 = self.newt22 + 0.3
                        if (self.newt22 >= 402 and self.newr22 < 266):
                            self.newr22 = self.newr22 + 0.3
                    if EC1[0].ex == 378 and EC1[0].ey == 208:
                        reroutee=1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 410,newy * 179), (newx * 410,newy * 270), 4)#rnew2
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt2, newy * self.newr2), 5, 0)  # train
                        if (self.newr2 < 266):
                            self.newr2 = self.newr2 + 0.3
                    if EC1[0].ex == 313 and EC1[0].ey == 195:
                        reroutee=1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 313,newy * 195), (newx * 400,newy * 195), 4)#rnew2
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 400,newy * 195), (newx * 400,newy * 270), 4)#rnew2
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt33, newy * self.newr33), 5, 0)  # train
                        if (self.newt33 < 400):
                            self.newt33 = self.newt33 + 0.3
                        if (self.newt33 >= 400 and self.newr33 < 266):
                            self.newr33 = self.newr33 + 0.3
                    if EC1[0].ex == 324 and EC1[0].ey == 208:
                        reroutee=1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 410,newy * 179), (newx * 410,newy * 270), 4)#rnew2
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt2, newy * self.newr2), 5, 0)  # train
                        if (self.newr2 < 266):
                            self.newr2 = self.newr2 + 0.3
                    if EC1[0].ex ==  602 and EC1[0].ey == 310:
                        reroutee=1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 620,newy * 310), (newx * 510,newy * 310), 4)#rnew3
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt3, newy * self.newr3), 5, 0)
                        if (self.newr3 >= 310 and self.newt3 > 505):
                            self.newt3 = self.newt3 - 0.3
                    if EC1[0].ex == 675 and EC1[0].ey == 156:
                        reroutee=1
                        emergency.draw_line_dashed(screen, (250, 1, 203), (newx * 628,newy * 223), (newx * 675,newy * 155), 4)#rnew4
                        emergency.draw_line_dashed(screen, (250, 1, 203), (newx * 630, newy * 210), (newx * 630, newy * 316), 4)
                        emergency.draw_line_dashed(screen, (250, 1, 203), (newx * 500, newy * 310), (newx * 630, newy * 310), 4)
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt4, newy * self.newr4), 5, 0)
                        if self.newt4 <= 675 and self.newt4 > 625 and self.newr4 >= 155 and self.newr4 < 220:
                            self.newr4 = self.newr4 + 0.3
                            self.newt4 = self.newt4 - 0.2
                        elif (self.newr4 >= 195 and self.newr4 < 310):
                            self.newr4 = self.newr4 + 0.3
                        elif (self.newr4 >= 310 and self.newt4 > 505):
                            self.newt4 = self.newt4 - 0.3

                if(twest[i].x>=680 and twest[i].x <1470 and twest[i].y <320):
                    if (self.a==255 and self.b==255):
                        self.a1 = -5
                        self.b1 = -5

                    elif (self.a==0 and self.b==0):

                        self.a1 = 5
                        self.b1 = 5
                    self.a = self.a + self.a1
                    self.b = self.b + self.b1
                    Graph.shortpath(graph, 'A', 'E')
                    if (Graph.shortpath(graph, 'A', 'E') == ['A', 'B', 'E'] or counter2 == 2):
                        emergency.draw_line_dashed(screen, (255, 128, 0), (newx * 880, newy * 132), (newx * 1160,newy * 132), 4)
                        emergency.draw_line_dashed(screen, (255, 128, 0), (newx * 880, newy * 135), (newx * 880, newy * 85), 4)
                        emergency.draw_line_dashed(screen, (255, 128, 0), (newx * 880,newy * 85), (newx * 800, newy * 85), 4)  # 410
                        emergency.draw_line_dashed(screen, (255, 128, 0), (newx * 800, newy * 85), (newx * 800, newy * 290), 4)  # 205
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.T1,newy * self.R1), 5, 0)
                        if (self.T1 >= 880 and self.T1 <= 1160):
                            self.T1 = self.T1 - 1
                        if (self.T1 == 879 and self.R1 >= 85 and self.R1 <= 135):
                            self.R1 = self.R1 - 1
                        if (self.T1 >= 801 and self.T1 <= 879 and self.R1 == 84):
                            self.T1 = self.T1 - 1
                        if (self.T1 == 800 and self.R1 >= 84 and self.R1 <= 283):
                            self.R1 = self.R1 + 1

                    if (Graph.shortpath(graph, 'A', 'E') == ['A', 'B1', 'E'] and counter2 == 1):
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 1162, newy * 132), (newx * 1162, newy * 315), 4)  # 183
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 900, newy * 312), (newx * 1160, newy * 312), 4)  # 260
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.T5, newy * self.R5), 5, 0)
                        if (self.T5 == 1162 and self.R5 >= 132 and self.R5 <= 312):
                            self.R5 = self.R5 + 1
                        if (self.T5 >= 903 and self.T5 <= 1162 and self.R5 == 313):
                            self.T5 = self.T5 - 1
                    if EC1[1].ex == 1126 and EC1[1].ey == 117:
                            reroutee2=0
                    if EC1[1].ex == 985 and EC1[1].ey == 225:
                            reroutee2=1
                            emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 985,newy * 225), (newx * 985,newy * 125), 4)#rnew1
                            emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 985,newy * 132), (newx * 882,newy * 132), 4)#rnew1
                            emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 882,newy * 132), (newx * 882,newy * 85), 4)#rnew1
                            emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 882,newy * 85), (newx * 780,newy * 85), 4)#rnew1
                            emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 790,newy * 85), (newx * 790,newy * 300), 4)#rnew1
                            pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt5, newy * self.newr5), 5, 0)
                            if self.newt5 == 985 and self.newr5 > 132 and self.newr4 <= 155:
                                self.newr5 = self.newr5 - 0.3
                                # self.newt5 = self.newt5 - 0.2
                            elif (self.newr5 < 132 and self.newt5 <= 985 and self.newt5 > 882):
                                self.newt5 = self.newt5 - 0.3
                                # print ("Remon",self.newt5)
                            elif (self.newt5 == 881.8000000000156 and self.newr5 < 132 and self.newr5 > 85):
                                self.newr5 = self.newr5 - 0.3
                            elif (self.newr5 < 85 and self.newt5 <= 882 and self.newt5 > 790):
                                self.newt5 = self.newt5 - 0.3
                            elif (self.newt5 <= 790 and self.newr5 >= 84 and self.newr5 < 300):
                                self.newr5 = self.newr5 + 0.4
                    if EC1[1].ex == 798 and EC1[1].ey == 71:
                            reroutee2=1
                            emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 790,newy * 71), (newx * 790,newy * 300), 4)#rnew1
                            pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt6, newy * self.newr6), 5, 0)
                            if (self.newt6 <= 790 and self.newr6 >= 71 and self.newr6 < 300):
                                    self.newr6 = self.newr6 + 0.4
                    if EC1[1].ex == 903 and EC1[1].ey == 124:
                        reroutee2=1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 905,newy * 124), (newx * 1145,newy * 124), 4)#rnew1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 1145,newy * 124), (newx * 1145,newy * 310), 4)#rnew1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 1145,newy * 310), (newx * 897,newy * 310), 4)#rnew1
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt221, newy * self.newr221), 5, 0)
                        if (self.newt221 <= 1145 and self.newr221 <= 310 ):
                                self.newt221 = self.newt221 + 0.4
                        if (self.newt221 > 1145 and self.newr221 <=310 ):
                                self.newr221 = self.newr221 + 0.4
                        if (self.newr221 > 310 and self.newt221 >=900 ):
                                self.newt221 = self.newt221 - 0.4
                    if EC1[1].ex == 795 and EC1[1].ey == 170:
                        reroutee2=1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 790,newy * 165), (newx * 790,newy * 290), 4)#rnew1
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt222, newy * self.newr222), 5, 0)
                        if (self.newr222 <= 282 ):
                                self.newr222 = self.newr222 + 0.4
                    if EC1[1].ex == 1265 and EC1[1].ey == 87:
                        reroutee2=1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 1265,newy * 87), (newx * 1185,newy * 87), 4)#rnew1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 1185,newy * 87), (newx * 1185,newy * 306), 4)#rnew1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 1185,newy * 306), (newx * 900,newy * 306), 4)#rnew1
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt2222, newy * self.newr2222), 5, 0)
                        if (self.newt2222 >= 1185 ):
                                self.newt2222 = self.newt2222 - 0.4
                        if (self.newt2222 < 1185 and self.newr2222 <= 306 ):
                                self.newr2222 = self.newr2222 + 0.4
                        if (self.newt2222 >= 904 and self.newt2222 < 1185 and self.newr2222 > 306):
                                self.newt2222 = self.newt2222 - 0.4
                if(twest[i].x>745 and twest[i].y <400 and twest[i].y > 320 ):
                    if (self.c==255 and self.d==255):
                        self.c1 = -5
                        self.d1 = -5

                    elif (self.c==0 and self.d==0):
                        self.c1 = 5
                        self.d1 = 5
                    self.c = self.c + self.c1
                    self.d = self.d + self.d1
                    Graph.shortpath(graph, 'W', 'E3')
                    # route1
                    if (Graph.shortpath(graph, 'W', 'E3') == ['W', 'F', 'E3'] and counter3 == 1):
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 1255, newy * 525), (newx * 1070, newy * 525), 4)  # 185
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 1070, newy * 525), (newx * 1070, newy * 376), 4)  # 149
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.T3, newy * self.R3), 5, 0)
                        if (self.T3 >= 1073 and self.T3 <= 1255):
                            self.T3 = self.T3 - 1
                        if (self.T3 == 1072 and self.R3 >= 386 and self.R3 <= 525):
                            self.R3 = self.R3 - 1
                    if EC1[2].ex == 1230 and EC1[2].ey == 510:
                        reroutee3=0
                    if EC1[2].ex == 1030 and EC1[2].ey == 585:
                        reroutee3=1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 1070,newy * 585), (newx * 1070,newy * 370), 4)#rnew1
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt7, newy * self.newr7), 5, 0)
                        if (self.newt7 <= 1070 and self.newr7 > 380 and self.newr7 <= 585):
                                self.newr7 = self.newr7 - 0.3
                    if EC1[2].ex == 880 and EC1[2].ey == 460:
                        reroutee3=1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 900,newy * 460), (newx * 940,newy * 460), 4)#rnew1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 940,newy * 460), (newx * 940,newy * 410), 4)#rnew1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 940,newy * 410), (newx * 1000,newy * 410), 4)#rnew1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 1000,newy * 410), (newx * 1000,newy * 360), 4)#rnew1
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt8, newy * self.newr8), 5, 0)
                        if (self.newr8 <= 460 and self.newt8 >= 900 and self.newt8 < 941):
                                self.newt8 = self.newt8 + 0.3

                        if (self.newt8 == 941.0999999999938 and self.newr8 > 411 and self.newr8 <= 460):
                                self.newr8 = self.newr8 - 0.3
                        if (self.newr8 <= 411 and self.newt8 >= 941.0999999999938 and self.newt8 < 1000):
                                self.newt8 = self.newt8 + 0.3
                                print('REMON', self.newt8)

                        if (self.newt8 == 1000.1999999999848 and self.newr8 >= 360 and self.newr8 < 411):
                                self.newr8 = self.newr8 - 0.3
                    if EC1[2].ex == 1304 and EC1[2].ey == 437:
                        reroutee3=1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 1295,newy * 437), (newx * 1295,newy * 513), 4)#rnew1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 1295,newy * 513), (newx * 1070,newy * 513), 4)#rnew1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 1070,newy * 513), (newx * 1070,newy * 379), 4)#rnew1
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt88, newy * self.newr88), 5, 0)
                        if (self.newr88 <= 513 and self.newt88 == 1297 ):
                                self.newr88 = self.newr88 + 0.3

                        if (self.newt88 <= 1297 and self.newr88 > 513 and self.newt88 >=1070):
                                self.newt88 = self.newt88 - 0.3
                                print('REMON', self.newt88)
                        if (self.newr88 >= 378 and self.newt88 < 1070 and self.newr88 < 514  ):
                                self.newr88 = self.newr88 - 0.3
                                print('WEMON', self.newt88)
                    if EC1[2].ex == 1199 and EC1[2].ey == 595:
                        reroutee3=1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 1195,newy * 595), (newx * 1195,newy * 536), 4)#rnew1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 1195,newy * 536), (newx * 1074,newy * 536), 4)#rnew1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 1074,newy * 536), (newx * 1074,newy * 379), 4)#rnew1
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt888, newy * self.newr888), 5, 0)
                        if (self.newr888 >= 536 and self.newt888 == 1197 ):
                                self.newr888 = self.newr888 - 0.3

                        if (self.newt888 <= 1197 and self.newr888 < 536 and self.newt888 >=1074):
                                self.newt888 = self.newt888 - 0.3
                                print('Karim', self.newt888)
                        if (self.newr888 >= 378 and self.newt888 < 1074 and self.newr888 < 537  ):
                                self.newr888 = self.newr888 - 0.3
                                print('Karmala', self.newt888)
                    if EC1[2].ex == 951 and EC1[2].ey == 503:
                        reroutee3=1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 1000,newy * 503), (newx * 1000,newy * 375), 4)#rnew1
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt8888, newy * self.newr8888), 5, 0)
                        if (self.newr8888 >= 375 and self.newt8888 == 1000 ):
                                self.newr8888 = self.newr8888 - 0.3
                    if EC1[2].ex == 1086 and EC1[2].ey == 511:
                        reroutee3=1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 1080,newy * 511), (newx * 1080,newy * 380), 4)#rnew1
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt88888, newy * self.newr88888), 5, 0)
                        if (self.newr88888 >= 380 and self.newt88888 == 1080 ):
                                self.newr88888 = self.newr88888 - 0.3
                    if EC1[2].ex == 892 and EC1[2].ey == 593:
                        reroutee3=1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 890,newy * 593), (newx * 890,newy * 537), 4)#rnew1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 890,newy * 537), (newx * 1002,newy * 537), 4)#rnew1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 1002,newy * 537), (newx * 1002,newy * 378), 4)#rnew1
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt888888, newy * self.newr888888), 5, 0)
                        if (self.newr888888 >= 537 and self.newt888888 == 890 ):
                                self.newr888888 = self.newr888888 - 0.3

                        if (self.newt888888 <= 1002 and self.newr888888 < 537 and self.newt888888 >=890):
                                self.newt888888 = self.newt888888 + 0.3
                                print('Remon', self.newt888888)
                        if (self.newr888888 >= 378 and self.newt888888 == 1002.199999999983 and self.newr888888 < 538  ):
                                self.newr888888 = self.newr888888 - 0.3
                                print('Remo', self.newt888888)
                    # route2
                    if (Graph.shortpath(graph, 'W', 'E3') == ['W', 'F1', 'E3'] or counter3 == 3):
                        emergency.draw_line_dashed(screen, (0, 102, 102), (newx * 1255, newy*525), (newx * 1005, newy * 525), 4)  # 250
                        emergency.draw_line_dashed(screen, (0, 102, 102), (newx * 1005, newy*525), (newx * 1005, newy * 376), 4)  # 149
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.T33, newy * self.R33), 5, 0)
                        if (self.T33 >= 1005 and self.T33 <= 1255):
                            self.T33 = self.T33 - 1
                        if (self.T33 == 1004 and self.R33 >= 386 and self.R33 <= 525):
                            self.R33 = self.R33 - 1
                            # route3
                    if (Graph.shortpath(graph, 'W', 'E3') == ['W', 'F2', 'E3'] or counter3 == 2):
                        emergency.draw_line_dashed(screen, (255, 128, 0), (newx * 1255, newy * 525), (newx * 1170, newy * 525), 4)  # 85
                        emergency.draw_line_dashed(screen, (255, 128, 0), (newx * 1180, newy * 525), (newx * 1180, newy * 400), 4)  # 125
                        emergency.draw_line_dashed(screen, (255, 128, 0), (newx * 1180, newy * 405), (newx * 1075, newy * 405), 4)  # 105
                        emergency.draw_line_dashed(screen, (255, 128, 0), (newx * 1075, newy * 420), (newx * 1075, newy * 372), 4)  # 48
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.T333, newy * self.R333), 5, 0)
                        if (self.T333 >= 1181 and self.T333 <= 1255):
                            self.T333 = self.T333 - 0.5
                        if (self.T333 == 1180.5 and self.R333 >= 405 and self.R333 <= 525):
                            self.R333 = self.R333 - 0.5
                        if (self.T333 >= 1076 and self.T333 <= 1180.5 and self.R333 == 405):
                            self.T333 = self.T333 - 0.5
                        if (self.T333 <= 1076 and self.R333 >= 380 and self.R333 <= 420):
                            self.R333 = self.R333 - 0.5
                    if EC1[3].ex == 350 and EC1[3].ey == 610:
                        reroutee4=0
                    if EC1[3].ex==350 and EC1[3].ey==480:
                        reroutee4=1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 410, newy * 525), (newx * 410, newy * 400), 3)
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 400, newy * 525), (newx * 489, newy * 525), 3)
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 480, newy * 525), (newx * 480, newy * 350), 3)
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 480, newy * 350), (newx * 530, newy * 350), 3)
                        pygame.draw.line(screen,(204, 0, 102), (newx * 535, newy * 358), (newx * 535, newy * 350), 3)
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 535,newy * 350), (newx * 535, newy * 380), 3)
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 530,newy * 380), (newx * 630, newy * 380), 3)
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt14, newy * self.newr14), 5, 0)

                        if (self.newt14 >= 410 and self.newt14 <= 480 and self.newr14 <= 525):
                            self.newr14 = self.newr14 + 0.5
                        elif (self.newt14 >= 410 and self.newt14 <= 480 and self.newr14 >= 525):
                            self.newt14 = self.newt14 + 0.5
                        elif (self.newt14 >= 480 and self.newt14 < 535 and self.newr14 >= 350):
                            self.newr14 = self.newr14 - 0.5
                        elif (self.newt14 >= 480 and self.newt14 <= 535 and self.newr14 == 349.5):
                            self.newt14 = self.newt14 + 0.5
                        elif (self.newt14 >= 535 and self.newr14 >= 349.5 and self.newr14 <= 380):
                            self.newr14 = self.newr14 + 1
                        elif (self.newt14 >= 535 and self.newt14 <= 630 and self.newr14 >= 380):
                            self.newt14 = self.newt14 + 1
                    if EC1[3].ex==510 and EC1[3].ey==500:
                        reroutee4=1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 480, newy * 525), (newx * 480, newy * 350), 3)
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 480, newy * 350), (newx * 530, newy * 350), 3)
                        pygame.draw.line(screen, (204, 0, 102), (newx * 535, newy * 358), (newx * 535, newy * 350), 3)
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 535,newy * 350), (newx * 535, newy * 380), 3)
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 530,newy * 380), (newx * 630, newy * 380), 3)
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt44, newy * self.newr44), 5, 0)

                        if (self.newt44 >= 480 and self.newt44 < 535 and self.newr44 >= 350):
                            self.newr44 = self.newr44 - 0.5
                        elif (self.newt44 >= 480 and self.newt44 <= 535 and self.newr44 == 349.5):
                            self.newt44 = self.newt44 + 0.5
                        elif (self.newt44 >= 535 and self.newr44 >= 349.5 and self.newr44 <= 380):
                            self.newr44 = self.newr44 + 1
                        elif (self.newt44 >= 535 and self.newt44 <= 630 and self.newr44 >= 380):
                            self.newt44 = self.newt44 + 1
                    if EC1[3].ex==760 and EC1[3].ey==580:
                        reroutee4=1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 760, newy * 550), (newx * 830, newy * 550), 3)
                        pygame.draw.line(screen, (204, 0, 102), (newx * 830, newy * 550), (newx * 830, newy * 528), 3)
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 830, newy * 528), (newx * 480, newy * 528), 3)
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 480, newy * 528), (newx * 480, newy * 350), 3)
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 480, newy * 350), (newx * 530, newy * 350), 3)
                        pygame.draw.line(screen, (204, 0, 102), (newx * 535, newy * 358), (newx * 535, newy * 350), 3)
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 535,newy * 350), (newx * 535, newy * 380), 3)
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 530,newy * 380), (newx * 630, newy * 380), 3)
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt34, newy * self.newr34), 5, 0)
                        if(self.newt34 >= 760 and self.newt34 < 830 and self.newr34 >= 550):
                            self.newt34=self.newt34+0.5
                        elif(self.newt34 >= 830 and self.newr34 <= 550 and self.newr34 >= 528 ):
                            self.newr34=self.newr34-0.5
                        elif(self.newt34 <= 830 and self.newt34 > 480 and self.newr34 <= 528 and self.newr34 > 381):
                            self.newt34=self.newt34-0.5
                        elif (self.newt34 >= 480 and self.newt34 < 535 and self.newr34 >= 350):
                            self.newr34 = self.newr34 - 0.5
                        elif (self.newt34 >= 480 and self.newt34 <= 535 and self.newr34 == 349.5):
                            self.newt34 = self.newt34 + 0.5
                        elif (self.newt34 >= 535 and self.newr34 >= 349.5 and self.newr34 <= 380):
                            self.newr34 = self.newr34 + 1
                        elif (self.newt34 >= 535 and self.newt34 <= 630 and self.newr34 >= 380):
                            self.newt34 = self.newt34 + 1


                if(twest[i].x<=745 and twest[i].x > 30 and twest[i].y <400 and twest[i].y > 320):
                    if (self.e==255 and self.f==255):
                        self.e1 = -5
                        self.f1 = -5
                    elif (self.e==0 and self.f==0):
                        self.e1 = 5
                        self.f1 = 5
                    self.e = self.e + self.e1
                    self.f = self.f + self.f1
                    Graph.shortpath(graph, 'M', 'E4')
                    # route1 w da kamn
                    if (Graph.shortpath(graph, 'M', 'E4') == ['M', 'K', 'E4'] and counter4 == 1):
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 350, newy * 545), (newx * 420, newy * 545), 3)
                        pygame.draw.line(screen, (204, 0, 102), (newx * 423, newy * 541), (newx * 423, newy * 525), 3)
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 420, newy * 525), (newx * 665, newy * 525), 3)
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 660,newy * 525), (newx * 660,newy * 460), 3)
                        pygame.draw.arc(screen, (204, 0, 102), [newx * 652, newy * 450, 17, 17], 0, 3.14 / 2, 3)
                        pygame.draw.arc(screen, (204, 0, 102), [newx * 652, newy * 450, 17, 17], 3 * 3.14 / 2, 2 * 3.14, 3)
                        pygame.draw.line(screen, (204, 0, 102), (newx * 655, newy * 450), (newx * 637, newy * 450), 3)
                        pygame.draw.line(screen, (204, 0, 102), (newx * 633, newy * 450), (newx * 625, newy * 435), 3)
                        pygame.draw.line(screen, (204, 0, 102), (newx * 625, newy * 388), (newx * 625, newy * 378), 3)
                        pygame.draw.line(screen, (204, 0, 102), (newx * 625, newy * 396), (newx * 625, newy * 407), 3)
                        pygame.draw.line(screen, (204, 0, 102), (newx * 625, newy * 417), (newx * 625, newy * 430), 3)
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.T4, newy * self.R4), 5, 0)
                        if (self.T4 >=  340 and self.T4 <=  423):
                            self.T4 = self.T4 + 0.5
                        if (self.T4 >=  423 and self.R4 >=  525):
                            self.R4 = self.R4 - 0.5
                        if (self.T4 >=  423 and self.T4 <=  660 and self.R4 ==  524.5):
                            self.T4 = self.T4 + 0.5
                        if (self.T4 >=  660 and self.R4 >=  450):
                            self.R4 = self.R4 - 0.5
                        if (self.T4 >= 633 and self.T4 <= 660 and self.R4 == 449.5):
                            self.T4 = self.T4 - 0.5
                        if (self.T4 >=  625 and self.T4 <= 633 and self.R4 <=  450):
                            self.T4 = self.T4 - 0.06
                            self.R4 = self.R4 - 0.5
                    # route2 w da kamn
                    if (Graph.shortpath(graph, 'M', 'E4') == ['M', 'K1', 'E4'] or counter4 == 2):
                        emergency.draw_line_dashed(screen, (255, 128, 0), (newx * 350, newy * 545), (newx * 420, newy * 545), 3)
                        pygame.draw.line(screen, (255, 128, 0), (newx * 423, newy * 541), (newx * 423, newy * 525), 3)
                        emergency.draw_line_dashed(screen, (255, 128, 0), (newx * 420, newy * 525), (newx * 489, newy * 525), 3)
                        emergency.draw_line_dashed(screen, (255, 128, 0), (newx * 480, newy * 525), (newx * 480, newy * 350), 3)
                        emergency.draw_line_dashed(screen, (255, 128, 0), (newx * 480, newy * 350), (newx * 530, newy * 350), 3)
                        pygame.draw.line(screen, (255, 128, 0), (newx * 535, newy * 358), (newx * 535, newy * 350), 3)
                        emergency.draw_line_dashed(screen, (255, 128, 0), (newx * 535,newy * 350), (newx * 535, newy * 380), 3)
                        emergency.draw_line_dashed(screen, (255, 128, 0), (newx * 530,newy * 380), (newx * 630, newy * 380), 3)
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.T44, newy * self.R44), 5, 0)
                        if (self.T44 >= 340 and self.T44 <= 423):
                            self.T44 = self.T44 + 0.5
                        if (self.T44 >= 423 and self.R44 >= 525):
                            self.R44 = self.R44 - 0.5
                        if (self.T44 >= 423 and self.T44 <= 480 and self.R44 == 524.5):
                            self.T44 = self.T44 + 0.5
                        if (self.T44 >= 480 and self.R44 >= 350):
                            self.R44 = self.R44 - 0.5
                        if (self.T44 >= 480 and self.T44 <= 535 and self.R44 == 349.5):
                            self.T44 = self.T44 + 0.5
                        if (self.T44 >= 535.5 and self.R44 >= 349.5 and self.R44 <= 380):
                            self.R44 = self.R44 + 1
                        if (self.T44 >= 535 and self.T44 <= 623 and self.R44 == 381):
                            self.T44 = self.T44 + 1
                        #if(self.T44 >=535 and self.R44<=358 and self.R44>=350):
                        #   self.T44 = self.T44 - 1
                    # route3 kan comment
                    if (Graph.shortpath(graph, 'M', 'E4') == ['M', 'K2', 'E4'] or counter4 == 3):
                        emergency.draw_line_dashed(screen, (0, 102, 102), (newx * 350, newy * 545), (newx * 420, newy * 545), 3)
                        pygame.draw.line(screen, (0, 102, 102), (newx * 423, newy * 541), (newx * 423,newy * 525), 3)
                        emergency.draw_line_dashed(screen, (0, 102, 102), (newx * 420, newy * 525), (newx * 780, newy * 525 ), 3)
                        pygame.draw.line(screen, (0, 102, 102), (newx * 774, newy * 525), (newx * 776, newy * 520), 3)
                        pygame.draw.line(screen, (0, 102, 102), (newx * 779, newy * 515), (newx * 784, newy * 500), 3)
                        pygame.draw.line(screen, (0, 102, 102), (newx * 784, newy * 497), (newx * 780, newy * 485), 3)
                        pygame.draw.line(screen, (0, 102, 102), (newx * 775, newy * 483), (newx * 765, newy * 480), 3)
                        pygame.draw.line(screen, (0, 102, 102), (newx * 775, newy * 483), (newx * 765, newy * 480), 3)
                        pygame.draw.line(screen, (0, 102, 102), (newx * 761, newy * 478), (newx * 761, newy * 470), 3)
                        pygame.draw.line(screen, (0, 102, 102), (newx * 755, newy * 465), (newx * 740, newy * 458), 3)
                        emergency.draw_line_dashed(screen, (0, 102, 102), (newx * 740, newy * 458), (newx * 740, newy * 380 ), 3)
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.T444,  newy * self.R444), 5, 0)
                        if (self.T444 >= 340 and self.T444 <= 423):
                            self.T444 = self.T444 + 0.5
                        if (self.T444 >= 423 and self.R444 >= 525):
                            self.R444 = self.R444 - 0.5
                        if (self.T444 >= 423 and self.T444 <= 774 and self.R444 == 524.5):
                            self.T444 = self.T444 + 2
                        if (self.T444 >= 774 and self.T444 <= 784 and self.R444 >= 507):
                            self.T444 = self.T444 + 0.2
                            self.R444 = self.R444 - 0.4
                        if ( self.R444 < 508 and self.T444 >= 767 and self.T444 <= 784 ):
                            self.T444 = self.T444 - 0.2
                            self.R444 = self.R444 - 0.4
                        if ( self.R444 <= 479.3 and self.R444 >= 469 and self.T444 == 768):
                            self.R444 = self.R444 - 0.5
                        if ( self.T444 < 767 and self.T444 >= 741 and self.R444 < 507):
                            self.T444 = self.T444 - 0.3
                            self.R444 = self.R444 - 0.2
                        if ( self.R444 < 456 and self.R444 >= 380 ):
                            self.R444 = self.R444 - 0.5
                        if ( self.T444 < 741 and self.T444 >= 680 and self.R444 < 382):
                            self.T444 = self.T444 - 0.5
                    if EC1[3].ex == 350 and EC1[3].ey == 610:
                        reroutee4=0
                    if EC1[3].ex==350 and EC1[3].ey==480:
                        reroutee4=1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 410, newy * 525), (newx * 410, newy * 400), 3)
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 400, newy * 525), (newx * 489, newy * 525), 3)
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 480, newy * 525), (newx * 480, newy * 350), 3)
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 480, newy * 350), (newx * 530, newy * 350), 3)
                        pygame.draw.line(screen, (204, 0, 102), (newx * 535, newy * 358), (newx * 535, newy * 350), 3)
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 535,newy * 350), (newx * 535, newy * 380), 3)
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 530,newy * 380), (newx * 630, newy * 380), 3)
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt14, newy * self.newr14), 5, 0)

                        if (self.newt14 >= 410 and self.newt14 <= 480 and self.newr14 <= 525):
                            self.newr14 = self.newr14 + 0.5
                        elif (self.newt14 >= 410 and self.newt14 <= 480 and self.newr14 >= 525):
                            self.newt14 = self.newt14 + 0.5
                        elif (self.newt14 >= 480 and self.newt14 < 535 and self.newr14 >= 350):
                            self.newr14 = self.newr14 - 0.5
                        elif (self.newt14 >= 480 and self.newt14 <= 535 and self.newr14 == 349.5):
                            self.newt14 = self.newt14 + 0.5
                        elif (self.newt14 >= 535 and self.newr14 >= 349.5 and self.newr14 <= 380):
                            self.newr14 = self.newr14 + 1
                        elif (self.newt14 >= 535 and self.newt14 <= 630 and self.newr14 >= 380):
                            self.newt14 = self.newt14 + 1
                    if EC1[3].ex==510 and EC1[3].ey==500:
                        reroutee4=1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 480, newy * 525), (newx * 480, newy * 350), 3)
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 480, newy * 350), (newx * 530, newy * 350), 3)
                        pygame.draw.line(screen, (204, 0, 102), (newx * 535, newy * 358), (newx * 535, newy * 350), 3)
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 535,newy * 350), (newx * 535, newy * 380), 3)
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 530,newy * 380), (newx * 630, newy * 380), 3)
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt44, newy * self.newr44), 5, 0)

                        if (self.newt44 >= 480 and self.newt44 < 535 and self.newr44 >= 350):
                            self.newr44 = self.newr44 - 0.5
                        elif (self.newt44 >= 480 and self.newt44 <= 535 and self.newr44 == 349.5):
                            self.newt44 = self.newt44 + 0.5
                        elif (self.newt44 >= 535 and self.newr44 >= 349.5 and self.newr44 <= 380):
                            self.newr44 = self.newr44 + 1
                        elif (self.newt44 >= 535 and self.newt44 <= 630 and self.newr44 >= 380):
                            self.newt44 = self.newt44 + 1
                    if EC1[3].ex==760 and EC1[3].ey==580:
                        reroutee4=1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 760, newy * 550), (newx * 830, newy * 550), 3)
                        pygame.draw.line(screen, (204, 0, 102), (newx * 830, newy * 550), (newx * 830, newy * 528), 3)
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 830, newy * 528), (newx * 480, newy * 528), 3)
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 480, newy * 528), (newx * 480, newy * 350), 3)
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 480, newy * 350), (newx * 530, newy * 350), 3)
                        pygame.draw.line(screen, (204, 0, 102), (newx * 535, newy * 358), (newx * 535, newy * 350), 3)
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 535,newy * 350), (newx * 535, newy * 380), 3)
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 530,newy * 380), (newx * 630, newy * 380), 3)
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt34, newy * self.newr34), 5, 0)
                        if(self.newt34 >= 760 and self.newt34 < 830 and self.newr34 >= 550):
                            self.newt34=self.newt34+0.5
                        elif(self.newt34 >= 830 and self.newr34 <= 550 and self.newr34 >= 528 ):
                            self.newr34=self.newr34-0.5
                        elif(self.newt34 <= 830 and self.newt34 > 480 and self.newr34 <= 528 and self.newr34 > 381):
                            self.newt34=self.newt34-0.5
                        elif (self.newt34 >= 480 and self.newt34 < 535 and self.newr34 >= 350):
                            self.newr34 = self.newr34 - 0.5
                        elif (self.newt34 >= 480 and self.newt34 <= 535 and self.newr34 == 349.5):
                            self.newt34 = self.newt34 + 0.5
                        elif (self.newt34 >= 535 and self.newr34 >= 349.5 and self.newr34 <= 380):
                            self.newr34 = self.newr34 + 1
                        elif (self.newt34 >= 535 and self.newt34 <= 630 and self.newr34 >= 380):
                            self.newt34 = self.newt34 + 1
                        #     self.T44 = self.T44 + 1
        for i in range (len(teast)):
            if(teast[i].flagStop==1):
                if(teast[i].x<680 and teast[i].y <320):
                    if (self.r==255 and self.h==255):
                        print("D",self.r,self.h)
                        self.r1 = -5
                        self.h1 = -5
                        print('Done')

                    elif (self.r==0 and self.h==0):
                        print("D",self.r,self.h)
                        self.r1 = 5
                        self.h1 = 5
                    self.r = self.r + self.r1
                    self.h = self.h + self.h1
                    Graph.shortpath(graph, 'X', 'E2')
                    if (Graph.shortpath(graph, 'X', 'E2') == ['X', 'Y', 'E2'] or counter == 2):
                        # route1
                        emergency.draw_line_dashed(screen, (255, 128, 0), (newx * 420, newy * 195), (newx * 625,newy * 195), 4)  # 205
                        emergency.draw_line_dashed(screen, (255, 128, 0), (newx * 420, newy * 195), (newx * 420, newy * 283), 4)  # 88
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.T2, newy * self.R2), 5, 0)
                        if (self.T2 <= 595 and self.T2 > 422):
                            self.T2 = self.T2 - 0.3
                        elif (self.T2 <= 422 and self.R2 >= 195 and self.R2 < 278):
                            self.R2 = self.R2 + 0.3

                    if (Graph.shortpath(graph, 'X', 'E2') == ['X', 'Y1', 'E2'] and counter == 1):
                        # route2
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 490,newy * 195), (newx * 600, newy * 195), 4)  # 110
                        pygame.draw.line(screen, (204, 0, 102), (newx * 490, newy * 195), (newx * 490, newy * 205), 4)  # 10
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx *490,newy * 206), (newx * 520, newy * 206), 4)  # 30
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx *526,newy * 206), (newx * 526 , newy * 300), 4)  # 94
                        pygame.draw.line(screen, (204, 0, 102), (newx * 526, newy * 310), (newx * 510, newy * 310), 4)  # 16
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.T22, newy * self.R22), 5, 0)

                        if (self.T22 <= 595 and self.T22 >= 492 and self.R22 >= 195 and self.R22 < 208):
                            self.T22 = self.T22 - 0.3
                        elif (self.T22 < 492 and self.R22 < 208):
                            self.R22 = self.R22 + 0.3
                        elif (self.T22 < 527 and self.R22 >= 208 and self.R22 < 310):
                            self.T22 = self.T22 + 0.3
                        elif (self.T22 >= 527 and self.R22 >= 208 and self.R22 < 310):
                            self.R22 = self.R22 + 0.3
                        elif (self.R22 >= 310 and self.T22 <= 528 and self.T22 >= 515):
                            self.T22 = self.T22 - 0.3
                            # if (T2<=490 and R2 >= 195 and R2 <= 206):
                        #      R2 = R2 + 1
                        # if (R2>=206 and T2 >=490 and T2 <521):
                        #     T2 = T2 + 1
                    if (Graph.shortpath(graph, 'X', 'E2') == ['X', 'Y2', 'E2'] or counter == 3):
                        # route3
                        emergency.draw_line_dashed(screen, (0, 102, 102), (newx * 580,newy * 195), (newx * 640,newy * 195), 4)  # 60
                        pygame.draw.arc(screen, (0, 102, 102), [newx * 624, newy * 200, 17, 17], 0, 3.14 / 2, 3)
                        pygame.draw.arc(screen, (0, 102, 102), [newx * 624, newy * 200, 17, 17], 3 * 3.14 / 2, 2 * 3.14, 3)
                        emergency.draw_line_dashed(screen, (0, 102, 102), (newx * 630, newy * 210), (newx * 630, newy * 316), 4)  # 106
                        emergency.draw_line_dashed(screen, (0, 102, 102), (newx * 500, newy * 310), (newx * 630, newy * 310), 4)  # 130
                        pygame.draw.circle(screen, (0, 102, 102), (newx * self.T222, newy * self.R222), 5, 0)  # train

                        if (self.T222 >= 595 and self.T222 < 630 and self.R222 == 195):
                            self.T222 = self.T222 + 0.3
                        elif (self.R222 >= 195 and self.R222 < 310):
                            self.R222 = self.R222 + 0.3
                        elif (self.R222 >= 310 and self.T222 > 505):
                            self.T222 = self.T222 - 0.3
                    if EC1[0].ex == 580 and EC1[0].ey == 185:
                        reroutee=0
                    if EC1[0].ex == 430 and EC1[0].ey == 119:
                        reroutee=1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 420,newy * 119), (newx * 420,newy * 280), 4)#rnew1
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt, newy * self.newr), 5, 0)  # train
                        if (self.newr < 266):
                            self.newr = self.newr + 0.3

                    # if EC1[0].ex == 430 and EC1[0].ey == 119:
                    #     emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 420,newy * 119), (newx * 420,newy * 280), 4)#rnew1
                    #     pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt, newy * self.newr), 5, 0)  # train
                    #     if (self.newr < 266):
                    #         self.newr = self.newr + 0.3

                    if EC1[0].ex == 378 and EC1[0].ey == 208:
                        reroutee=1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 410,newy * 179), (newx * 410,newy * 270), 4)#rnew2
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt2, newy * self.newr2), 5, 0)  # train
                        if (self.newr2 < 266):
                            self.newr2 = self.newr2 + 0.3
                    if EC1[0].ex ==  602 and EC1[0].ey == 310:
                        reroutee=1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 620,newy * 310), (newx * 510,newy * 310), 4)#rnew3
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt3, newy * self.newr3), 5, 0)
                        if (self.newr3 >= 310 and self.newt3 > 505):
                            self.newt3 = self.newt3 - 0.3
                    if EC1[0].ex == 675 and EC1[0].ey == 156:
                        reroutee=1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 628,newy * 223), (newx * 675,newy * 155), 4)#rnew4
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 630, newy * 210), (newx * 630, newy * 316), 4)
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 500, newy * 310), (newx * 630, newy * 310), 4)
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt4, newy * self.newr4), 5, 0)
                        if self.newt4 <= 675 and self.newt4 > 625 and self.newr4 >= 155 and self.newr4 < 220:
                            self.newr4 = self.newr4 + 0.3
                            self.newt4 = self.newt4 - 0.2
                        elif (self.newr4 >= 195 and self.newr4 < 310):
                            self.newr4 = self.newr4 + 0.3
                        elif (self.newr4 >= 310 and self.newt4 > 505):
                            self.newt4 = self.newt4 - 0.3
                    if EC1[0].ex == 430 and EC1[0].ey == 119:
                        reroutee=1
                        emergency.draw_line_dashed(screen, (250, 1, 203), (newx * 420,newy * 119), (newx * 420,newy * 280), 4)#rnew1
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt, newy * self.newr), 5, 0)  # train
                        if (self.newr < 266):
                            self.newr = self.newr + 0.3
                    if EC1[0].ex == 355 and EC1[0].ey == 119:
                        reroutee=1
                        emergency.draw_line_dashed(screen, (250, 1, 203), (newx * 350,newy * 119), (newx * 403,newy * 119), 4)#rnew1
                        emergency.draw_line_dashed(screen, (250, 1, 203), (newx * 403,newy * 119), (newx * 403,newy * 270), 4)#rnew1
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt1, newy * self.newr1), 5, 0)  # train
                        if (self.newt1 < 402):
                            self.newt1 = self.newt1 + 0.3
                        if (self.newt1 >= 402 and self.newr1 < 268):
                            self.newr1 = self.newr1 + 0.3
                    if EC1[0].ex == 275 and EC1[0].ey == 55:
                        reroutee=1
                        emergency.draw_line_dashed(screen, (250, 1, 203), (newx * 275,newy * 40), (newx * 403,newy * 40), 4)#rnew1
                        emergency.draw_line_dashed(screen, (250, 1, 203), (newx * 403,newy * 40), (newx * 403,newy * 270), 4)#rnew1
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt22, newy * self.newr22), 5, 0)  # train
                        if (self.newt22 < 402):
                            self.newt22 = self.newt22 + 0.3
                        if (self.newt22 >= 402 and self.newr22 < 266):
                            self.newr22 = self.newr22 + 0.3
                    if EC1[0].ex == 378 and EC1[0].ey == 208:
                        reroutee=1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 410,newy * 179), (newx * 410,newy * 270), 4)#rnew2
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt2, newy * self.newr2), 5, 0)  # train
                        if (self.newr2 < 266):
                            self.newr2 = self.newr2 + 0.3
                    if EC1[0].ex == 313 and EC1[0].ey == 195:
                        reroutee=1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 313,newy * 195), (newx * 400,newy * 195), 4)#rnew2
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 400,newy * 195), (newx * 400,newy * 270), 4)#rnew2
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt33, newy * self.newr33), 5, 0)  # train
                        if (self.newt33 < 400):
                            self.newt33 = self.newt33 + 0.3
                        if (self.newt33 >= 400 and self.newr33 < 266):
                            self.newr33 = self.newr33 + 0.3
                    if EC1[0].ex == 324 and EC1[0].ey == 208:
                        reroutee=1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 410,newy * 179), (newx * 410,newy * 270), 4)#rnew2
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt2, newy * self.newr2), 5, 0)  # train
                        if (self.newr2 < 266):
                            self.newr2 = self.newr2 + 0.3
                    if EC1[0].ex ==  602 and EC1[0].ey == 310:
                        reroutee=1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 620,newy * 310), (newx * 510,newy * 310), 4)#rnew3
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt3, newy * self.newr3), 5, 0)
                        if (self.newr3 >= 310 and self.newt3 > 505):
                            self.newt3 = self.newt3 - 0.3
                    if EC1[0].ex == 675 and EC1[0].ey == 156:
                        reroutee=1
                        emergency.draw_line_dashed(screen, (250, 1, 203), (newx * 628,newy * 223), (newx * 675,newy * 155), 4)#rnew4
                        emergency.draw_line_dashed(screen, (250, 1, 203), (newx * 630, newy * 210), (newx * 630, newy * 316), 4)
                        emergency.draw_line_dashed(screen, (250, 1, 203), (newx * 500, newy * 310), (newx * 630, newy * 310), 4)
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt4, newy * self.newr4), 5, 0)
                        if self.newt4 <= 675 and self.newt4 > 625 and self.newr4 >= 155 and self.newr4 < 220:
                            self.newr4 = self.newr4 + 0.3
                            self.newt4 = self.newt4 - 0.2
                        elif (self.newr4 >= 195 and self.newr4 < 310):
                            self.newr4 = self.newr4 + 0.3
                        elif (self.newr4 >= 310 and self.newt4 > 505):
                            self.newt4 = self.newt4 - 0.3

                if(teast[i].x>=680 and teast[i].x <1470 and teast[i].y <320):
                    if (self.a==255 and self.b==255):
                        self.a1 = -5
                        self.b1 = -5

                    elif (self.a==0 and self.b==0):

                        self.a1 = 5
                        self.b1 = 5
                    self.a = self.a + self.a1
                    self.b = self.b + self.b1
                    Graph.shortpath(graph, 'A', 'E')
                    if (Graph.shortpath(graph, 'A', 'E') == ['A', 'B', 'E'] or counter2 == 2):
                        emergency.draw_line_dashed(screen, (255, 128, 0), (newx * 880, newy * 132), (newx * 1160,newy * 132), 4)
                        emergency.draw_line_dashed(screen, (255, 128, 0), (newx * 880, newy * 135), (newx * 880, newy * 85), 4)
                        emergency.draw_line_dashed(screen, (255, 128, 0), (newx * 880,newy * 85), (newx * 800, newy * 85), 4)  # 410
                        emergency.draw_line_dashed(screen, (255, 128, 0), (newx * 800, newy * 85), (newx * 800, newy * 290), 4)  # 205
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.T1, newy * self.R1), 5, 0)
                        if (self.T1 >= 880 and self.T1 <= 1160):
                            self.T1 = self.T1 - 1
                        if (self.T1 == 879 and self.R1 >= 85 and self.R1 <= 135):
                            self.R1 = self.R1 - 1
                        if (self.T1 >= 801 and self.T1 <= 879 and self.R1 == 84):
                            self.T1 = self.T1 - 1
                        if (self.T1 == 800 and self.R1 >= 84 and self.R1 <= 283):
                            self.R1 = self.R1 + 1
                        # route2
                    if (Graph.shortpath(graph, 'A', 'E') == ['A', 'B1', 'E'] and counter2 == 1):
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 1162, newy * 132), (newx * 1162, newy * 315), 4)  # 183
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 900, newy * 312), (newx * 1160, newy * 312), 4)  # 260
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.T5, newy * self.R5), 5, 0)
                        if (self.T5 == 1162 and self.R5 >= 132 and self.R5 <= 312):
                            self.R5 = self.R5 + 1
                        if (self.T5 >= 903 and self.T5 <= 1162 and self.R5 == 313):
                            self.T5 = self.T5 - 1
                    if EC1[1].ex == 1126 and EC1[1].ey == 117:
                        reroutee2=0
                    if EC1[1].ex == 985 and EC1[1].ey == 225:
                            reroutee2=1
                            emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 985,newy * 225), (newx * 985,newy * 125), 4)#rnew1
                            emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 985,newy * 132), (newx * 882,newy * 132), 4)#rnew1
                            emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 882,newy * 132), (newx * 882,newy * 85), 4)#rnew1
                            emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 882,newy * 85), (newx * 780,newy * 85), 4)#rnew1
                            emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 790,newy * 85), (newx * 790,newy * 300), 4)#rnew1
                            pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt5, newy * self.newr5), 5, 0)
                            if self.newt5 == 985 and self.newr5 > 132 and self.newr4 <= 155:
                                self.newr5 = self.newr5 - 0.3
                                # self.newt5 = self.newt5 - 0.2
                            elif (self.newr5 < 132 and self.newt5 <= 985 and self.newt5 > 882):
                                self.newt5 = self.newt5 - 0.3
                                # print ("Remon",self.newt5)
                            elif (self.newt5 == 881.8000000000156 and self.newr5 < 132 and self.newr5 > 85):
                                self.newr5 = self.newr5 - 0.3
                            elif (self.newr5 < 85 and self.newt5 <= 882 and self.newt5 > 790):
                                self.newt5 = self.newt5 - 0.3
                            elif (self.newt5 <= 790 and self.newr5 >= 84 and self.newr5 < 300):
                                self.newr5 = self.newr5 + 0.4
                    if EC1[1].ex == 798 and EC1[1].ey == 71:
                        reroutee2=1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 790,newy * 71), (newx * 790,newy * 300), 4)#rnew1
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt6, newy * self.newr6), 5, 0)
                        if (self.newt6 <= 790 and self.newr6 >= 71 and self.newr6 < 300):
                                self.newr6 = self.newr6 + 0.4
                    if EC1[1].ex == 985 and EC1[1].ey == 225:
                            reroutee2=1
                            emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 985,newy * 225), (newx * 985,newy * 125), 4)#rnew1
                            emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 985,newy * 132), (newx * 882,newy * 132), 4)#rnew1
                            emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 882,newy * 132), (newx * 882,newy * 85), 4)#rnew1
                            emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 882,newy * 85), (newx * 780,newy * 85), 4)#rnew1
                            emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 790,newy * 85), (newx * 790,newy * 300), 4)#rnew1
                            pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt5, newy * self.newr5), 5, 0)
                            if self.newt5 == 985 and self.newr5 > 132 and self.newr4 <= 155:
                                self.newr5 = self.newr5 - 0.3
                                # self.newt5 = self.newt5 - 0.2
                            elif (self.newr5 < 132 and self.newt5 <= 985 and self.newt5 > 882):
                                self.newt5 = self.newt5 - 0.3
                                # print ("Remon",self.newt5)
                            elif (self.newt5 == 881.8000000000156 and self.newr5 < 132 and self.newr5 > 85):
                                self.newr5 = self.newr5 - 0.3
                            elif (self.newr5 < 85 and self.newt5 <= 882 and self.newt5 > 790):
                                self.newt5 = self.newt5 - 0.3
                            elif (self.newt5 <= 790 and self.newr5 >= 84 and self.newr5 < 300):
                                self.newr5 = self.newr5 + 0.4
                    if EC1[1].ex == 798 and EC1[1].ey == 71:
                        reroutee2=1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 790,newy * 71), (newx * 790,newy * 300), 4)#rnew1
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt6, newy * self.newr6), 5, 0)
                        if (self.newt6 <= 790 and self.newr6 >= 71 and self.newr6 < 300):
                                self.newr6 = self.newr6 + 0.4
                    if EC1[1].ex == 903 and EC1[1].ey == 124:
                        reroutee2=1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 905,newy * 124), (newx * 1145,newy * 124), 4)#rnew1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 1145,newy * 124), (newx * 1145,newy * 310), 4)#rnew1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 1145,newy * 310), (newx * 897,newy * 310), 4)#rnew1
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt221, newy * self.newr221), 5, 0)
                        if (self.newt221 <= 1145 and self.newr221 <= 310 ):
                                self.newt221 = self.newt221 + 0.4
                        if (self.newt221 > 1145 and self.newr221 <=310 ):
                                self.newr221 = self.newr221 + 0.4
                        if (self.newr221 > 310 and self.newt221 >=900 ):
                                self.newt221 = self.newt221 - 0.4
                    if EC1[1].ex == 795 and EC1[1].ey == 170:
                        reroutee2=1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 790,newy * 165), (newx * 790,newy * 290), 4)#rnew1
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt222, newy * self.newr222), 5, 0)
                        if (self.newr222 <= 282 ):
                                self.newr222 = self.newr222 + 0.4
                    if EC1[1].ex == 1265 and EC1[1].ey == 87:
                        reroutee2=1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 1265,newy * 87), (newx * 1185,newy * 87), 4)#rnew1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 1185,newy * 87), (newx * 1185,newy * 306), 4)#rnew1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 1185,newy * 306), (newx * 900,newy * 306), 4)#rnew1
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt2222, newy * self.newr2222), 5, 0)
                        if (self.newt2222 >= 1185 ):
                                self.newt2222 = self.newt2222 - 0.4
                        if (self.newt2222 < 1185 and self.newr2222 <= 306 ):
                                self.newr2222 = self.newr2222 + 0.4
                        if (self.newt2222 >= 904 and self.newt2222 < 1185 and self.newr2222 > 306):
                                self.newt2222 = self.newt2222 - 0.4

                if(teast[i].x>745 and teast[i].y <400 and teast[i].y > 320):
                    if (self.c==255 and self.d==255):
                        print("D",self.r,self.h)
                        self.c1 = -5
                        self.d1 = -5
                        print('Done')

                    elif (self.c==0 and self.d==0):
                        print("D",self.r,self.h)
                        self.c1 = 5
                        self.d1 = 5
                    self.c = self.c + self.c1
                    self.d = self.d + self.d1
                    Graph.shortpath(graph, 'W', 'E3')
                    Graph.shortpath(graph, 'W', 'E3')
                    # route1
                    if (Graph.shortpath(graph, 'W', 'E3') == ['W', 'F', 'E3'] and counter3 == 1):
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 1255, newy * 525), (newx * 1070, newy * 525), 4)  # 185
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 1070, newy * 525), (newx * 1070, newy * 376), 4)  # 149
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.T3, newy * self.R3), 5, 0)
                        if (self.T3 >= 1073 and self.T3 <= 1255):
                            self.T3 = self.T3 - 1
                        if (self.T3 == 1072 and self.R3 >= 386 and self.R3 <= 525):
                            self.R3 = self.R3 - 1
                            # route2
                    if (Graph.shortpath(graph, 'W', 'E3') == ['W', 'F1', 'E3'] or counter3 == 3):
                        emergency.draw_line_dashed(screen,(0, 102, 102), (newx * 1255, newy *525), (newx * 1005, newy * 525), 4)  # 250
                        emergency.draw_line_dashed(screen, (0, 102, 102), (newx * 1005, newy*525), (newx * 1005, newy * 376), 4)  # 149
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.T33, newy * self.R33), 5, 0)
                        if (self.T33 >= 1005 and self.T33 <= 1255):
                            self.T33 = self.T33 - 1
                        if (self.T33 == 1004 and self.R33 >= 386 and self.R33 <= 525):
                            self.R33 = self.R33 - 1
                        # route3
                    if (Graph.shortpath(graph, 'W', 'E3') == ['W', 'F2', 'E3'] or counter3 == 2):
                        emergency.draw_line_dashed(screen, (255, 128, 0), (newx * 1255, newy * 525), (newx * 1170, newy * 525), 4)  # 85
                        emergency.draw_line_dashed(screen, (255, 128, 0), (newx * 1180, newy * 525), (newx * 1180, newy * 400), 4)  # 125
                        emergency.draw_line_dashed(screen, (255, 128, 0), (newx * 1180, newy * 405), (newx * 1075, newy * 405), 4)  # 105
                        emergency.draw_line_dashed(screen, (255, 128, 0), (newx * 1075, newy * 420), (newx * 1075, newy * 372), 4)  # 48
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.T333, newy * self.R333), 5, 0)
                        if (self.T333 >= 1181 and self.T333 <= 1255):
                            self.T333 = self.T333 - 0.5
                        if (self.T333 == 1180.5 and self.R333 >= 405 and self.R333 <= 525):
                            self.R333 = self.R333 - 0.5
                        if (self.T333 >= 1076 and self.T333 <= 1180.5 and self.R333 == 405):
                            self.T333 = self.T333 - 0.5
                        if (self.T333 <= 1076 and self.R333 >= 380 and self.R333 <= 420):
                            self.R333 = self.R333 - 0.5
                    if EC1[2].ex == 1230 and EC1[2].ey == 510:
                        reroutee3=0
                    if EC1[2].ex == 1030 and EC1[2].ey == 585:
                        reroutee3=1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 1070,newy * 585), (newx * 1070,newy * 370), 4)#rnew1
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt7, newy * self.newr7), 5, 0)
                        if (self.newt7 <= 1070 and self.newr7 > 380 and self.newr7 <= 585):
                                self.newr7 = self.newr7 - 0.3
                    if EC1[2].ex == 880 and EC1[2].ey == 460:
                        reroutee3=1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 900,newy * 460), (newx * 940,newy * 460), 4)#rnew1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 940,newy * 460), (newx * 940,newy * 410), 4)#rnew1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 940,newy * 410), (newx * 1000,newy * 410), 4)#rnew1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 1000,newy * 410), (newx * 1000,newy * 360), 4)#rnew1
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt8, newy * self.newr8), 5, 0)
                        if (self.newr8 <= 460 and self.newt8 >= 900 and self.newt8 < 941):
                                self.newt8 = self.newt8 + 0.3

                        if (self.newt8 == 941.0999999999938 and self.newr8 > 411 and self.newr8 <= 460):
                                self.newr8 = self.newr8 - 0.3
                        if (self.newr8 <= 411 and self.newt8 >= 941.0999999999938 and self.newt8 < 1000):
                                self.newt8 = self.newt8 + 0.3
                                print('REMON', self.newt8)

                        if (self.newt8 == 1000.1999999999848 and self.newr8 >= 360 and self.newr8 < 411):
                                self.newr8 = self.newr8 - 0.3
                    if EC1[2].ex == 1304 and EC1[2].ey == 437:
                        reroutee3=1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 1295,newy * 437), (newx * 1295,newy * 513), 4)#rnew1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 1295,newy * 513), (newx * 1070,newy * 513), 4)#rnew1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 1070,newy * 513), (newx * 1070,newy * 379), 4)#rnew1
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt88, newy * self.newr88), 5, 0)
                        if (self.newr88 <= 513 and self.newt88 == 1297 ):
                                self.newr88 = self.newr88 + 0.3

                        if (self.newt88 <= 1297 and self.newr88 > 513 and self.newt88 >=1070):
                                self.newt88 = self.newt88 - 0.3
                                print('REMON', self.newt88)
                        if (self.newr88 >= 378 and self.newt88 < 1070 and self.newr88 < 514  ):
                                self.newr88 = self.newr88 - 0.3
                                print('WEMON', self.newt88)
                    if EC1[2].ex == 1199 and EC1[2].ey == 595:
                        reroutee3=1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 1195,newy * 595), (newx * 1195,newy * 536), 4)#rnew1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 1195,newy * 536), (newx * 1074,newy * 536), 4)#rnew1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 1074,newy * 536), (newx * 1074,newy * 379), 4)#rnew1
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt888, newy * self.newr888), 5, 0)
                        if (self.newr888 >= 536 and self.newt888 == 1197 ):
                                self.newr888 = self.newr888 - 0.3

                        if (self.newt888 <= 1197 and self.newr888 < 536 and self.newt888 >=1074):
                                self.newt888 = self.newt888 - 0.3
                                print('Karim', self.newt888)
                        if (self.newr888 >= 378 and self.newt888 < 1074 and self.newr888 < 537  ):
                                self.newr888 = self.newr888 - 0.3
                                print('Karmala', self.newt888)
                    if EC1[2].ex == 951 and EC1[2].ey == 503:
                        reroutee3=1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 1000,newy * 503), (newx * 1000,newy * 375), 4)#rnew1
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt8888, newy * self.newr8888), 5, 0)
                        if (self.newr8888 >= 375 and self.newt8888 == 1000 ):
                                self.newr8888 = self.newr8888 - 0.3
                    if EC1[2].ex == 1086 and EC1[2].ey == 511:
                        reroutee3=1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 1080,newy * 511), (newx * 1080,newy * 380), 4)#rnew1
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt88888, newy * self.newr88888), 5, 0)
                        if (self.newr88888 >= 380 and self.newt88888 == 1080 ):
                                self.newr88888 = self.newr88888 - 0.3
                    if EC1[2].ex == 892 and EC1[2].ey == 593:
                        reroutee3=1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 890,newy * 593), (newx * 890,newy * 537), 4)#rnew1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 890,newy * 537), (newx * 1002,newy * 537), 4)#rnew1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 1002,newy * 537), (newx * 1002,newy * 378), 4)#rnew1
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt888888, newy * self.newr888888), 5, 0)
                        if (self.newr888888 >= 537 and self.newt888888 == 890 ):
                                self.newr888888 = self.newr888888 - 0.3

                        if (self.newt888888 <= 1002 and self.newr888888 < 537 and self.newt888888 >=890):
                                self.newt888888 = self.newt888888 + 0.3
                                print('Remon', self.newt888888)
                        if (self.newr888888 >= 378 and self.newt888888 == 1002.199999999983 and self.newr888888 < 538  ):
                                self.newr888888 = self.newr888888 - 0.3
                                print('Remo', self.newt888888)
                if(teast[i].x<=745 and teast[i].x > 30 and teast[i].y <400 and teast[i].y > 320):
                    if (self.e==255 and self.f==255):
                        print("D2",self.r,self.h)
                        self.e1 = -5
                        self.f1 = -5
                        print('Done')

                    elif (self.e==0 and self.f==0):
                        print("D",self.r,self.h)
                        self.e1 = 5
                        self.f1 = 5
                    self.e = self.e + self.e1
                    self.f = self.f + self.f1
                    Graph.shortpath(graph, 'M', 'E4')
                    # route1
                    if (Graph.shortpath(graph, 'M', 'E4') == ['M', 'K', 'E4'] and counter4 == 1):
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 350, newy * 545), (newx * 420, newy * 545), 3)
                        pygame.draw.line(screen, (204, 0, 102), (newx * 423, newy * 541), (newx * 423, newy * 525), 3)
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 420, newy * 525), (newx * 665, newy * 525), 3)
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 660,newy * 525), (newx * 660,newy * 460), 3)
                        pygame.draw.arc(screen, (204, 0, 102), [newx * 652, newy * 450, 17, 17], 0, 3.14 / 2, 3)
                        pygame.draw.arc(screen, (204, 0, 102), [newx * 652, newy * 450, 17, 17], 3 * 3.14 / 2, 2 * 3.14, 3)
                        pygame.draw.line(screen, (204, 0, 102), (newx * 655, newy * 450), (newx * 637, newy * 450), 3)
                        pygame.draw.line(screen, (204, 0, 102), (newx * 633, newy * 450), (newx * 625, newy * 435), 3)
                        pygame.draw.line(screen, (204, 0, 102), (newx * 625, newy * 388), (newx * 625, newy * 378), 3)
                        pygame.draw.line(screen, (204, 0, 102), (newx * 625, newy * 396), (newx * 625, newy * 407), 3)
                        pygame.draw.line(screen, (204, 0, 102), (newx * 625, newy * 417), (newx * 625, newy * 430), 3)
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.T4, newy * self.R4), 5, 0)
                        if (self.T4 >=  340 and self.T4 <=  423):
                            self.T4 = self.T4 + 0.5
                        if (self.T4 >=  423 and self.R4 >=  525):
                            self.R4 = self.R4 - 0.5
                        if (self.T4 >=  423 and self.T4 <=  660 and self.R4 ==  524.5):
                            self.T4 = self.T4 + 0.5
                        if (self.T4 >=  660 and self.R4 >=  450):
                            self.R4 = self.R4 - 0.5
                        if (self.T4 >= 633 and self.T4 <= 660 and self.R4 == 449.5):
                            self.T4 = self.T4 - 0.5
                        if (self.T4 >=  625 and self.T4 <= 633 and self.R4 <=  450):
                            self.T4 = self.T4 - 0.06
                            self.R4 = self.R4 - 0.5
                    # route2
                    if (Graph.shortpath(graph, 'M', 'E4') == ['M', 'K1', 'E4'] or counter4 == 2):
                        emergency.draw_line_dashed(screen, (255, 128, 0), (newx * 350, newy * 545), (newx * 420, newy * 545), 3)
                        pygame.draw.line(screen, (255, 128, 0), (newx * 423, newy * 541), (newx * 423, newy * 525), 3)
                        emergency.draw_line_dashed(screen, (255, 128, 0), (newx * 420, newy * 525), (newx * 489, newy * 525), 3)
                        emergency.draw_line_dashed(screen, (255, 128, 0), (newx * 480, newy * 525), (newx * 480, newy * 350), 3)
                        emergency.draw_line_dashed(screen, (255, 128, 0), (newx * 480, newy * 350), (newx * 530, newy * 350), 3)
                        pygame.draw.line(screen, (255, 128, 0), (newx * 535, newy * 358), (newx * 535, newy * 350), 3)
                        emergency.draw_line_dashed(screen, (255, 128, 0), (newx * 535,newy * 350), (newx * 535, newy * 380), 3)
                        emergency.draw_line_dashed(screen, (255, 128, 0), (newx * 530,newy * 380), (newx * 630, newy * 380), 3)
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.T44, newy * self.R44), 5, 0)
                        if (self.T44 >= 340 and self.T44 <= 423):
                            self.T44 = self.T44 + 0.5
                        if (self.T44 >= 423 and self.R44 >= 525):
                            self.R44 = self.R44 - 0.5
                        if (self.T44 >= 423 and self.T44 <= 480 and self.R44 == 524.5):
                            self.T44 = self.T44 + 0.5
                        if (self.T44 >= 480 and self.R44 >= 350):
                            self.R44 = self.R44 - 0.5
                        if (self.T44 >= 480 and self.T44 <= 535 and self.R44 == 349.5):
                            self.T44 = self.T44 + 0.5
                        if (self.T44 >= 535.5 and self.R44 >= 349.5 and self.R44 <= 380):
                            self.R44 = self.R44 + 1
                        if (self.T44 >= 535 and self.T44 <= 623 and self.R44 == 381):
                            self.T44 = self.T44 + 1
                    # route3
                    if (Graph.shortpath(graph, 'M', 'E4') == ['M', 'K2', 'E4'] or counter4 == 3):
                        emergency.draw_line_dashed(screen, (0, 102, 102), (newx * 350, newy * 545), (newx * 420, newy * 545), 3)
                        pygame.draw.line(screen, (0, 102, 102), (newx * 423, newy * 541), (newx * 423,newy * 525), 3)
                        emergency.draw_line_dashed(screen, (0, 102, 102), (newx * 420, newy * 525), (newx * 780, newy * 525 ), 3)
                        pygame.draw.line(screen, (0, 102, 102), (newx * 774, newy * 525), (newx * 776, newy * 520), 3)
                        pygame.draw.line(screen, (0, 102, 102), (newx * 779, newy * 515), (newx * 784, newy * 500), 3)
                        pygame.draw.line(screen, (0, 102, 102), (newx * 784, newy * 497), (newx * 780, newy * 485), 3)
                        pygame.draw.line(screen, (0, 102, 102), (newx * 775, newy * 483), (newx * 765, newy * 480), 3)
                        pygame.draw.line(screen, (0, 102, 102), (newx * 775, newy * 483), (newx * 765, newy * 480), 3)
                        pygame.draw.line(screen, (0, 102, 102), (newx * 761, newy * 478), (newx * 761, newy * 470), 3)
                        pygame.draw.line(screen, (0, 102, 102), (newx * 755, newy * 465), (newx * 740, newy * 458), 3)
                        emergency.draw_line_dashed(screen, (0, 102, 102), (newx * 740, newy * 458), (newx * 740, newy * 380 ), 3)
                        emergency.draw_line_dashed(screen, (0, 102, 102), (newx * 750, newy * 378), (newx * 680, newy * 378 ), 3)
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.T444, newy * self.R444), 5, 0)
                        if (self.T444 >= 340 and self.T444 <= 423):
                            self.T444 = self.T444 + 0.5
                        if (self.T444 >= 423 and self.R444 >= 525):
                            self.R444 = self.R444 - 0.5
                        if (self.T444 >= 423 and self.T444 <= 774 and self.R444 == 524.5):
                            self.T444 = self.T444 + 2
                        if (self.T444 >= 774 and self.T444 <= 784 and self.R444 >= 507):
                            self.T444 = self.T444 + 0.2
                            self.R444 = self.R444 - 0.4
                        if ( self.R444 < 508 and self.T444 >= 767 and self.T444 <= 784 ):
                            self.T444 = self.T444 - 0.2
                            self.R444 = self.R444 - 0.4
                        if ( self.R444 <= 479.3 and self.R444 >= 469 and self.T444 == 768):
                            self.R444 = self.R444 - 0.5
                        if ( self.T444 < 767 and self.T444 >= 741 and self.R444 < 507):
                            self.T444 = self.T444 - 0.3
                            self.R444 = self.R444 - 0.2
                        if ( self.R444 < 456 and self.R444 >= 380 ):
                            self.R444 = self.R444 - 0.5
                        if ( self.T444 < 741 and self.T444 >= 680 and self.R444 < 382):
                            self.T444 = self.T444 - 0.5
                    if EC1[3].ex == 350 and EC1[3].ey == 610:
                        reroutee4=0
                    if EC1[3].ex==350 and EC1[3].ey==480:
                        reroutee4=1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 410, newy * 525), (newx * 410, newy * 400), 3)
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 400, newy * 525), (newx * 489, newy * 525), 3)
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 480, newy * 525), (newx * 480, newy * 350), 3)
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 480, newy * 350), (newx * 530, newy * 350), 3)
                        pygame.draw.line(screen, (204, 0, 102), (newx * 535, newy * 358), (newx * 535, newy * 350), 3)
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 535,newy * 350), (newx * 535, newy * 380), 3)
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 530,newy * 380), (newx * 630, newy * 380), 3)
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt14, newy * self.newr14), 5, 0)

                        if (self.newt14 >= 410 and self.newt14 <= 480 and self.newr14 <= 525):
                            self.newr14 = self.newr14 + 0.5
                        elif (self.newt14 >= 410 and self.newt14 <= 480 and self.newr14 >= 525):
                            self.newt14 = self.newt14 + 0.5
                        elif (self.newt14 >= 480 and self.newt14 < 535 and self.newr14 >= 350):
                            self.newr14 = self.newr14 - 0.5
                        elif (self.newt14 >= 480 and self.newt14 <= 535 and self.newr14 == 349.5):
                            self.newt14 = self.newt14 + 0.5
                        elif (self.newt14 >= 535 and self.newr14 >= 349.5 and self.newr14 <= 380):
                            self.newr14 = self.newr14 + 1
                        elif (self.newt14 >= 535 and self.newt14 <= 630 and self.newr14 >= 380):
                            self.newt14 = self.newt14 + 1
                    if EC1[3].ex==510 and EC1[3].ey==500:
                        reroutee4=1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 480, newy * 525), (newx * 480, newy * 350), 3)
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 480, newy * 350), (newx * 530, newy * 350), 3)
                        pygame.draw.line(screen, (204, 0, 102), (newx * 535, newy * 358), (newx * 535, newy * 350), 3)
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 535,newy * 350), (newx * 535, newy * 380), 3)
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 530,newy * 380), (newx * 630, newy * 380), 3)
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt44, newy * self.newr44), 5, 0)

                        if (self.newt44 >= 480 and self.newt44 < 535 and self.newr44 >= 350):
                            self.newr44 = self.newr44 - 0.5
                        elif (self.newt44 >= 480 and self.newt44 <= 535 and self.newr44 == 349.5):
                            self.newt44 = self.newt44 + 0.5
                        elif (self.newt44 >= 535 and self.newr44 >= 349.5 and self.newr44 <= 380):
                            self.newr44 = self.newr44 + 1
                        elif (self.newt44 >= 535 and self.newt44 <= 630 and self.newr44 >= 380):
                            self.newt44 = self.newt44 + 1
                    if EC1[3].ex==760 and EC1[3].ey==580:
                        reroutee4=1
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 760, newy * 550), (newx * 830, newy * 550), 3)
                        pygame.draw.line(screen, (204, 0, 102), (newx * 830, newy * 550), (newx * 830, newy * 528), 3)
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 830, newy * 528), (newx * 480, newy * 528), 3)
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 480, newy * 528), (newx * 480, newy * 350), 3)
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 480, newy * 350), (newx * 530, newy * 350), 3)
                        pygame.draw.line(screen, (204, 0, 102), (newx * 535, newy * 358), (newx * 535, newy * 350), 3)
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 535,newy * 350), (newx * 535, newy * 380), 3)
                        emergency.draw_line_dashed(screen, (204, 0, 102), (newx * 530,newy * 380), (newx * 630, newy * 380), 3)
                        pygame.draw.circle(screen, (0, 0, 0), (newx * self.newt34, newy * self.newr34), 5, 0)
                        if(self.newt34 >= 760 and self.newt34 < 830 and self.newr34 >= 550):
                            self.newt34=self.newt34+0.5
                        elif(self.newt34 >= 830 and self.newr34 <= 550 and self.newr34 >= 528 ):
                            self.newr34=self.newr34-0.5
                        elif(self.newt34 <= 830 and self.newt34 > 480 and self.newr34 <= 528 and self.newr34 > 381):
                            self.newt34=self.newt34-0.5
                        elif (self.newt34 >= 480 and self.newt34 < 535 and self.newr34 >= 350):
                            self.newr34 = self.newr34 - 0.5
                        elif (self.newt34 >= 480 and self.newt34 <= 535 and self.newr34 == 349.5):
                            self.newt34 = self.newt34 + 0.5
                        elif (self.newt34 >= 535 and self.newr34 >= 349.5 and self.newr34 <= 380):
                            self.newr34 = self.newr34 + 1
                        elif (self.newt34 >= 535 and self.newt34 <= 630 and self.newr34 >= 380):
                            self.newt34 = self.newt34 + 1
        if (self.help == 1 and soscounter % 2 == 0):
            sound.play()
            if (self.r == 255 and self.h == 255):
                self.r1 = -5
                self.h1 = -5
            elif (self.r == 0 and self.h == 0):
                self.r1 = 5
                self.h1 = 5
            self.r = self.r + self.r1
            self.h = self.h + self.h1
            if (self.a == 255 and self.b == 255):
                self.a1 = -5
                self.b1 = -5
            elif (self.a == 0 and self.b == 0):
                self.a1 = 5
                self.b1 = 5
            self.a = self.a + self.a1
            self.b = self.b + self.b1
            if (self.c == 255 and self.d == 255):
                self.c1 = -5
                self.d1 = -5
            elif (self.c == 0 and self.d == 0):
                self.c1 = 5
                self.d1 = 5
            self.c = self.c + self.c1
            self.d = self.d + self.d1
            if (self.e == 255 and self.f == 255):
                self.e1 = -5
                self.f1 = -5
            elif (self.e == 0 and self.f == 0):
                self.e1 = 5
                self.f1 = 5
            self.e = self.e + self.e1
            self.f = self.f + self.f1
            if (self.XR == 255):
                self.XR1 = -5
            elif (self.XR == 0):
                self.XR1 = 5
            self.XR = self.XR + self.XR1

            if (self.px == 255):
                self.px1 = -5
            elif (self.px == 0):
                self.px1 = 5
            self.px = self.px + self.px1


    def emergency(self):
        trainindex=ui.comboBox.currentIndex()
        choice = str(ui.comboBox.currentText())
        first_char = re.findall("\d",choice)

        if(first_char[0]=='5' and first_char[2]=='6'):
            twest[0].flagE = 1
            twest[0].Ex1 = twest[0].x
            twest[0].Ey1 = twest[0].y
            sound.play()
        if(first_char[0]=='5' and first_char[2]=='7'):
            twest[1].flagE = 1
            twest[1].Ex1 = twest[1].x
            twest[1].Ey1 = twest[1].y
            sound.play()
        if(first_char[0]=='5' and first_char[2]=='8'):
            twest[2].flagE = 1
            twest[2].Ex1 = twest[2].x
            twest[2].Ey1 = twest[2].y
            sound.play()
        if(first_char[0]=='5' and first_char[2]=='9'):
            twest[3].flagE = 1
            twest[3].Ex1 = twest[3].x
            twest[3].Ey1 = twest[3].y
            sound.play()
        if(first_char[0]=='5' and first_char[2]=='0'):
            twest[4].flagE = 1
            twest[4].Ex1 = twest[4].x
            twest[4].Ey1 = twest[4].y
            sound.play()
        if(first_char[0]=='5' and first_char[2]=='1'):
            twest[5].flagE = 1
            twest[5].Ex1 = twest[5].x
            twest[5].Ey1 = twest[5].y
            sound.play()
        if(first_char[0]=='8' and first_char[2]=='6'):
            teast[0].flagE = 1
            teast[0].Ex1 = teast[0].x
            teast[0].Ey1 = teast[0].y
            sound.play()
        if(first_char[0]=='8' and first_char[2]=='7'):
            teast[1].flagE = 1
            teast[1].Ex1 = teast[1].x
            teast[1].Ey1 = teast[1].y
            sound.play()
        if(first_char[0]=='8' and first_char[2]=='8'):
            teast[2].flagE = 1
            teast[2].Ex1 = teast[2].x
            teast[2].Ey1 = teast[2].y
            sound.play()
        if(first_char[0]=='8' and first_char[2]=='9'):
            teast[3].flagE = 1
            teast[3].Ex1 = teast[3].x
            teast[3].Ey1 = teast[3].y
            sound.play()
        if(first_char[0]=='8' and first_char[2]=='0'):
            teast[4].flagE = 1
            teast[4].Ex1 = teast[4].x
            teast[4].Ey1 = teast[4].y
            sound.play()
        if(first_char[0]=='8' and first_char[2]=='1'):
            teast[5].flagE = 1
            teast[5].Ex1 = teast[5].x
            teast[5].Ey1 = teast[5].y
            sound.play()
        for i in range(len(twest)):
            if twest[i].flagE == 1:
                realtime.db.child("emergency").update({"isEmergency":"1"})

        for i in range(len(teast)):
            if teast[i].flagE == 1:
                realtime.db.child("emergency").update({"isEmergency":"1"})


start_time = time.time()
end_time=0
font = pygame.font.Font('freesansbold.ttf', 14)
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
running =1
no_trains=3
twest=[]
teast=[]
t=[]
twestid=516
teastid=816
c=emergency(1)
reroutee=0
reroutee2=0
reroutee3=0
reroutee4=0
counter = 1
counter2 = 1
counter3 = 1
counter4 = 1
soscounter = 1
XR = 255
XR1 = 0
px = 255
px1 = 0
s="0"
for i in range(no_trains):
    twest.append(train(twestid,screen,newx,newy,15,205,start_time ))
    twestid=twestid+1
for i in range(no_trains):
    teast.append(train(teastid,screen,newx,newy,1473,220,start_time ))
    teastid=teastid+1
pw=["el mosher tantawy","el mosher tantawy","el mosher tantawy"]
pe=["Dusit","Dusit","Dusit"]
def Start():
    twest[0].flagmov =1
    teast[0].flagmov =1
    for i in range(len(twest)):
        twest[i].xflage='start'
        twest[i].endprocess=0
        twest[i].backward=0
    for i in range(len(teast)):
        teast[i].xflage='start'
        teast[i].endprocess=0
        teast[i].backward=0
        teast[i].f=0

def stop():
    for i in range(len(twest)):
        twest[i].xflage='stop'
    for i in range(len(teast)):
        teast[i].xflage='stop'
def endprocess():
    for i in range(len(twest)):
        if i > 0:
            twest[i].fl=0
        twest[i].endprocess=1
    for i in range(len(teast)):
        if i > 0:
            teast[i].fl=0
        teast[i].endprocess=1
def report():
    import socket
    host = socket.gethostbyname(socket.gethostname())
    webbrowser.open(f'http://{host}:5000/')
def REROUTING():
    emindex = ui.comboBox_2.currentIndex()
    global reroutee
    global reroutee2
    global reroutee3
    global reroutee4
    global counter
    global counter2
    global counter3
    global counter4
    print(reroutee2)
    if reroutee == 0:
        if (emindex == 0):
            if (counter == 3):
                counter = counter - 3
            if (counter <= 3):
                counter = counter + 1
    if reroutee2 == 0:
        if (emindex == 1):
            if (counter2 == 2):
                counter2 = counter2 - 2
            if (counter2 <= 2):
                counter2 = counter2 + 1
    if reroutee3 == 0:
        if (emindex == 2):
            if (counter3 == 3):
                counter3 = counter3 - 3
            if (counter3 <= 3):
                counter3 = counter3 + 1
    if reroutee4 == 0:
        if (emindex == 3):
            if (counter4 == 3):
                counter4 = counter4 - 3
            if (counter4 <= 3):
                counter4 = counter4 + 1

def S_O_S():
    global soscounter
    if (soscounter % 2 == 1):
        c.help = 0
    sound.stop()
    soscounter = soscounter + 1
    c.px = 255
    c.XR1 = 0
    c.px1 = 0
    c.XR = 255
    c.r = 255
    c.r1 = 0
    c.h = 255
    c.h1 = 0
    c.a = 255
    c.a1 = 0
    c.b = 255
    c.b1 = 0
    c.f = 255
    c.f1 = 0
    c.r = 255
    c.r1 = 0
    c.d = 255
    c.d1 = 0
    c.e = 255
    c.e1 = 0
    c.c = 255
    c.c1 = 0
    if (soscounter % 2 == 0):
        c.help = 1
def is_over(rect, pos):
    # function takes a tuple of (x, y) coords and a pygame.Rect object
    # returns True if the given rect overlaps the given coords
    # else it returns False
    return True if rect.collidepoint(pos[0], pos[1]) else False
def screenrep(x,y,id):
    pygame.draw.rect(screen, (51, 137, 210), (newx * x,newy * y, 85, 70), 0, 3)
    text = font.render("    ID: %d "%id, True, white)
    text1 = font.render("  speed: 80 ", True, white)
    text2 = font.render("   pos: %d "%x, True, white)
    screen.blit(text, (newx * x, newy * y + 10))
    screen.blit(text1, (newx * x,newy * y + 25))
    screen.blit(text2, (newx * x,newy * y + 40))
def emergencyrep(x,y,n):
    pygame.draw.rect(screen, (243 , 156 , 18), (newx * x, newy * y, newx * 120 , newy * 220), 0, 3)
    text1 = font.render("  Emergency  ", True, white)
    text = font.render("  station %d "%n, True, white)
    text2 = font.render(" 1 Ambulances", True, white)
    text3 = font.render(" 1 PoliceCars", True, white)
    text4 = font.render(" 2 doctors", True, white)
    text5 = font.render(" 4 nurses", True, white)
    text6 = font.render(" 2 inspector", True, white)
    text7 = font.render(" 1 fire engine", True, white)
    text8 = font.render(" stations from", True, white)
    if n == 1:
        text9 = font.render(" 1-3 W & 1-5 E", True, white)
    elif n == 2:
        text9 = font.render("       4-5 W", True, white)
    elif n == 3:
        text9 = font.render("6-10 W & 10-8 E", True, white)
    elif n == 4:
        text9 = font.render("7-6 E", True, white)
    screen.blit(text, (newx * x + 10, newy * y + 30))
    screen.blit(text1,(newx * x + 10 , newy * y + 10))
    screen.blit(text2,(newx * x + 10, newy * y + 50))
    screen.blit(text3,(newx * x + 10, newy * y + 70))
    screen.blit(text4,(newx * x + 10, newy * y + 90))
    screen.blit(text5, (newx * x + 10, newy * y + 110))
    screen.blit(text6, (newx * x + 10, newy * y + 130))
    screen.blit(text7, (newx * x + 10, newy * y + 150))
    screen.blit(text8, (newx * x + 10, newy * y + 170))
    screen.blit(text9, (newx * x + 10, newy * y + 190))
def emergencyacc(x,y):
    pygame.draw.rect(screen, (243 , 156 , 18), (newx * x, newy * y, newx * 93 , newy * 50), 0, 3)
    text1 = font.render("   Help is on ", True, white)
    text = font.render("  the way ", True, white)
    screen.blit(text, (newx * x + 10, newy * y + 25))
    screen.blit(text1, (newx * x, newy *y + 10))
def hospitalrep(x,y,n):
    pygame.draw.rect(screen, (231, 76, 60), (newx * x,newy * y, 87, 50), 0, 3)
    text = font.render("  hospital %d "%n, True, white)
    screen.blit(text, (newx * x, newy * y + 18))
def policerep(x,y,n):
    pygame.draw.rect(screen, (65,105,225), (newx * x,newy * y, 120, 50), 0, 3)
    text = font.render("  police station %d "%n, True, white)
    screen.blit(text, (newx * x, newy * y + 18))
def keyrep(x,y):
    pygame.draw.rect(screen, (255,255,255), (newx * x,newy * y, 120, 220), 0, 3)
    text = font.render("Police", True, (0,0,0))
    text1 = font.render("Emergency", True, (0,0,0))
    text2 = font.render("Hospital", True, (0,0,0))
    text3 = font.render("EastTrain", True, (0,0,0))
    text4 = font.render("WestTrain", True, (0,0,0))
    text5 = font.render("EastStation", True, (0,0,0))
    text6 = font.render("WestStation", True, (0,0,0))
    text7 = font.render("E-line", True, (0,0,0))
    text8 = font.render("Report", True, (0,0,0))
    text9 = font.render("END/START", True, (0,0,0))
    image1 = pygame.image.load("em.png")
    image1 = pygame.transform.scale(image1 ,(20,20) )
    image2 = pygame.image.load("po.png")
    image2 = pygame.transform.scale(image2 ,(20,20) )
    image3 = pygame.image.load("ho.png")
    image3 = pygame.transform.scale(image3 ,(20,20) )
    image4 = pygame.image.load("east train.png")
    image4 = pygame.transform.scale(image4 ,(20,20) )
    image5 = pygame.image.load("west train.png")
    image5 = pygame.transform.scale(image5 ,(20,20) )
    image6 = pygame.image.load("east station.png")
    image6 = pygame.transform.scale(image6 ,(20,20) )
    image7 = pygame.image.load("west station.png")
    image7 = pygame.transform.scale(image7 ,(20,20) )
    image8 = pygame.image.load("emline.png")
    image8 = pygame.transform.scale(image8 ,(20,15) )
    image10 = pygame.image.load("report.png")
    image10 = pygame.transform.scale(image10 ,(15,20) )
    image9 = pygame.image.load("ESstation.png")
    image9 = pygame.transform.scale(image9 ,(20,20) )
    screen.blit(text, (newx * x + 5, newy * y + 38))
    screen.blit(text1, (newx * x + 5, newy *y + 18))
    screen.blit(text2, (newx * x + 5 , newy *y + 58 ))
    screen.blit(text3, (newx * x + 5 , newy *y + 78 ))
    screen.blit(text4, (newx * x + 5 , newy *y + 98 ))
    screen.blit(text5, (newx * x + 5 , newy *y + 118 ))
    screen.blit(text6, (newx * x + 5 , newy *y + 138 ))
    screen.blit(text7, (newx * x + 5 , newy *y + 158 ))
    screen.blit(text8, (newx * x + 5 , newy *y + 178 ))
    screen.blit(text9, (newx * x + 5 , newy *y + 198 ))
    screen.blit(image1, (newx * x + 90 , newy *y + 18))
    screen.blit(image2, (newx * x + 90 , newy *y + 38))
    screen.blit(image3, (newx * x + 90 , newy *y + 58))
    screen.blit(image4, (newx * x + 90 , newy *y + 78))
    screen.blit(image5, (newx * x + 90 , newy *y + 98))
    screen.blit(image6, (newx * x + 90 , newy *y + 118))
    screen.blit(image7, (newx * x + 90 , newy *y + 138))
    screen.blit(image8, (newx * x + 90 , newy *y + 158))
    screen.blit(image10, (newx * x + 90 , newy *y + 178))
    screen.blit(image9, (newx * x + 90 , newy *y + 198))
rectangle = pygame.rect.Rect(176, 134, 17, 17)
rectangle_draging = False
clock = pygame.time.Clock()
def station(x,y,n):
    pygame.draw.rect(screen, (231, 76, 60), (newx * x, newy * y, 150, 40), 0, 3)
    text1 = font.render("%s" % n, True, white)
    screen.blit(text1, (newx * x + 10, newy * y + 12))

rectangle = pygame.rect.Rect(176, 134, 17, 17)
rectangle_draging = False
clock = pygame.time.Clock()
# TILESIZE = 32
# BOARD_POS = (540, 100)
# def create_board_surf():
#         global TILESIZE
#         board_surf = pygame.Surface((TILESIZE*4, TILESIZE*4))
#         dark = False
#         for sy in range(4):
#             for sx in range(4):
#                 rect = pygame.Rect(sx*TILESIZE, sy*TILESIZE, TILESIZE, TILESIZE)
#                 pygame.draw.rect(board_surf, pygame.Color('#C6A7A7' if dark else '#1C274B'), rect)
#                 dark = not dark
#             dark = not dark
#         return board_surf

# def create_board():
#         board = []
#         for sy in range(4):
#             board.append([])
#             for sx in range(4):
#                  board[sy].append(None)
#         return board

# def get_square_under_mouse(board):
#     mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) - BOARD_POS
#     sx, sy = [int(v // TILESIZE) for v in mouse_pos]
#     try:
#         if sx >= 0 and sy >= 0: return (board[sy][sx], sx, sy)
#     except IndexError: pass
#     return None, None, None
j=1
g=3
counter8=0
counter7=0
zg1=0
zg2=0
def addtrainwest():
    global twestid
    global EC_list
    global counter8
    global j
    global g
    global trainpos
    global pw
    ntwestid=0
    if j<=3:
        twest.append(train(twestid,screen,newx,newy,15,205,start_time))
        twest[j+2].speed=0.02
        j=j+1
        twestid=twestid+1
        EC_list.append(str(twestid-1))
        EC_list.sort(key=int)
        ui.comboBox.clear()
        ui.comboBox.addItems(EC_list)
        for i in range(len(twest)):
            twest[i].xflage='start'

        newtwestid = [twestid-1]
        cursor = conn.cursor()
        csql = "INSERT IGNORE INTO trains VALUES (%s,'Available','00:00:00','00:00:00','0', 'Al moshir tantawy' ,'west')"
        val = (newtwestid)
        cursor.execute(csql,val)
        conn.commit()
        pw.append("el mosher tantawy")

    elif j > 3:
        print("in j")
        if "516" not in EC_list:
            ntwestid="516"
            print("ana hna")
        elif "517" not in EC_list:
            ntwestid="517"
        elif "518" not in EC_list:
            ntwestid="518"
        elif "519" not in EC_list:
            ntwestid="519"
        elif "520" not in EC_list:
            ntwestid="520"
        elif "521" not in EC_list:
            ntwestid="521"
        else:
            ntwestid="0"
        if ntwestid != "0":
            print("appended", ntwestid)
            twest.append(train(ntwestid,screen,newx,newy,1473,220,start_time))
            counter8=0
            EC_list.append(str(ntwestid))
            EC_list.sort(key=int)
            ui.comboBox.clear()
            ui.comboBox.addItems(EC_list)
            for i in range(len(twest)):
                twest[i].xflage='start'
            newtwestid = [ntwestid]
            cursor = conn.cursor()
            csql = "UPDATE trains SET status = 'Available' WHERE ID = %s"
            val = (newtwestid)
            cursor.execute(csql,val)
            conn.commit()
            pw.append("el mosher tantawy")

k=1
mmcs=0
def addtraineast():
    global teastid
    global EC_list
    global k
    global counter7
    global pe
    nteastid=0
    if k<=3:
        teast.append(train(teastid,screen,newx,newy,1473,220,start_time))
        teast[k+2].speed=0.02
        k=k+1
        teastid=teastid+1
        EC_list.append(str(teastid-1))
        EC_list.sort(key=int)
        ui.comboBox.clear()
        ui.comboBox.addItems(EC_list)
        for i in range(len(teast)):
            teast[i].xflage='start'

        newteastid = [teastid-1]
        cursor = conn.cursor()
        csql = "INSERT IGNORE INTO trains VALUES (%s,'Available','00:00:00','00:00:00','0', 'Dusit' ,'east')"
        val = (newteastid)
        cursor.execute(csql,val)
        conn.commit()
        pe.append("Dusit")
    elif k == 4:
        if "816" not in EC_list:
            nteastid="816"
        elif "817" not in EC_list:
            nteastid="817"
        elif "818" not in EC_list:
            nteastid="818"
        elif "819" not in EC_list:
            nteastid="819"
        elif "820" not in EC_list:
            nteastid="820"
        elif "821" not in EC_list:
            nteastid="821"
        else:
            nteastid="0"
        if nteastid != "0":
            teast.append(train(nteastid,screen,newx,newy,1473,220,start_time))
            EC_list.append(str(nteastid))
            counter7=0
            EC_list.sort(key=int)
            ui.comboBox.clear()
            ui.comboBox.addItems(EC_list)
            for i in range(len(teast)):
                teast[i].xflage='start'

            newteastid = [nteastid]
            cursor = conn.cursor()
            csql = "UPDATE trains SET status = 'Available' WHERE ID = %s"
            val = (newteastid)
            cursor.execute(csql,val)
            conn.commit()
            pe.append("Dusit")
ce1=0
ce2=0
ce3=0
ce4=0

def removetrain():
    trainindex=ui.comboBox.currentIndex()
    choice = str(ui.comboBox.currentText())
    first_char = re.findall("\d",choice)
    global counter8
    global counter7
    global EC_list
    removechoice = [choice]
    cursor = conn.cursor()

    csql = "UPDATE trains SET status = 'maintenance' WHERE ID = %s"
    val = (removechoice)
    cursor.execute(csql,val)
    conn.commit()

    #insert main
    sss=""
    if choice == '516':
        sss= '519'
    elif choice == '517':
        sss= '520'
    elif choice == '518':
        sss= '521'
    sss1=[sss]
    now = datetime.now()
    end = int(now.day)
    end1=now.replace(day = (end + 3))
    now1=[now]
    end2=[end1]
    csql = "INSERT IGNORE INTO maintenance (TR_ID,maintenance_start_date,maintenance_end_date,new_TR_ID	) VALUES (%s,%s,%s,%s)"
    val = (removechoice[0],now1[0],end2[0],sss1[0])
    cursor.execute(csql,val)
    conn.commit()  
    if(first_char[0]=='5' and first_char[2]=='6' and counter8==0):
        twest.pop(0)
        counter8=1
        EC_list.pop(trainindex)
        pw.pop(0)
        ui.comboBox.clear()
        ui.comboBox.addItems(EC_list)

    elif(first_char[0]=='5' and first_char[2]=='7'):
        if(counter8==1):
            twest.pop(0)
            pw.pop(0)
            counter8=2
            EC_list.pop(trainindex)
            ui.comboBox.clear()
            ui.comboBox.addItems(EC_list)
        else:
            twest.pop(1)
            pw.pop(1)
            counter8=3
            EC_list.pop(trainindex)
            ui.comboBox.clear()
            ui.comboBox.addItems(EC_list)

    elif(first_char[0]=='5' and first_char[2]=='8'):
        if(counter8==2):
            twest.pop(0)
            pw.pop(0)
            counter8=4
            EC_list.pop(trainindex)
            ui.comboBox.clear()
            ui.comboBox.addItems(EC_list)
        elif(counter8==3):
            twest.pop(1)
            pw.pop(1)
            counter8=5
            EC_list.pop(trainindex)
            ui.comboBox.clear()
            ui.comboBox.addItems(EC_list)
        else:
            twest.pop(2)
            pw.pop(2)
            counter8=6
            EC_list.pop(trainindex)
            ui.comboBox.clear()
            ui.comboBox.addItems(EC_list)

    elif(first_char[0]=='5' and first_char[2]=='9'):
        if(counter8==4):
            twest.pop(0)
            pw.pop(0)
            counter8=7
            EC_list.pop(trainindex)
            ui.comboBox.clear()
            ui.comboBox.addItems(EC_list)
        elif(counter8==5):
            twest.pop(1)
            pw.pop(1)
            counter8=8
            EC_list.pop(trainindex)
            ui.comboBox.clear()
            ui.comboBox.addItems(EC_list)
        elif(counter8==6):
            twest.pop(2)
            pw.pop(2)
            counter8=9
            EC_list.pop(trainindex)
            ui.comboBox.clear()
            ui.comboBox.addItems(EC_list)
        else:
            twest.pop(3)
            pw.pop(3)
            counter8=10
            EC_list.pop(trainindex)
            ui.comboBox.clear()
            ui.comboBox.addItems(EC_list)

    elif(first_char[0]=='5' and first_char[2]=='0'):
        if(counter8==7):
            twest.pop(0)
            pw.pop(0)
            counter8=11
            EC_list.pop(trainindex)
            ui.comboBox.clear()
            ui.comboBox.addItems(EC_list)
        elif(counter8==8):
            twest.pop(1)
            pw.pop(1)
            counter8=12
            EC_list.pop(trainindex)
            ui.comboBox.clear()
            ui.comboBox.addItems(EC_list)
        elif(counter8==9):
            twest.pop(2)
            pw.pop(2)
            counter8=13
            EC_list.pop(trainindex)
            ui.comboBox.clear()
            ui.comboBox.addItems(EC_list)
        elif(counter8==10):
            twest.pop(3)
            pw.pop(3)
            counter8=14
            EC_list.pop(trainindex)
            ui.comboBox.clear()
            ui.comboBox.addItems(EC_list)
        else:
            twest.pop(4)
            pw.pop(4)
            counter8=15
            EC_list.pop(trainindex)
            ui.comboBox.clear()
            ui.comboBox.addItems(EC_list)

    elif(first_char[0]=='5' and first_char[2]=='1'):
        if(counter8==11):
            twest.pop(0)
            pw.pop(0)
            EC_list.pop(trainindex)
            ui.comboBox.clear()
            ui.comboBox.addItems(EC_list)
        elif(counter8==12):
            twest.pop(1)
            pw.pop(1)
            EC_list.pop(trainindex)
            ui.comboBox.clear()
            ui.comboBox.addItems(EC_list)
        elif(counter8==13):
            twest.pop(2)
            pw.pop(2)
            EC_list.pop(trainindex)
            ui.comboBox.clear()
            ui.comboBox.addItems(EC_list)
        elif(counter8==14):
            twest.pop(3)
            pw.pop(3)
            EC_list.pop(trainindex)
            ui.comboBox.clear()
            ui.comboBox.addItems(EC_list)
        elif(counter8==15):
            twest.pop(4)
            pw.pop(4)
            EC_list.pop(trainindex)
            ui.comboBox.clear()
            ui.comboBox.addItems(EC_list)
        else:
            twest.pop(5)
            pw.pop(5)
            EC_list.pop(trainindex)
            ui.comboBox.clear()
            ui.comboBox.addItems(EC_list)

    if(first_char[0]=='8' and first_char[2]=='6' and counter7==0):
        teast.pop(0)
        pe.pop(0)
        counter7=1
        EC_list.pop(trainindex)
        ui.comboBox.clear()
        ui.comboBox.addItems(EC_list)

    if(first_char[0]=='8' and first_char[2]=='7'):
        if(counter7==1):
            teast.pop(0)
            pe.pop(0)
            counter7=2
            EC_list.pop(trainindex)
            ui.comboBox.clear()
            ui.comboBox.addItems(EC_list)
        else:
            teast.pop(1)
            pe.pop(1)
            counter7=3
            EC_list.pop(trainindex)
            ui.comboBox.clear()
            ui.comboBox.addItems(EC_list)

    if(first_char[0]=='8' and first_char[2]=='8'):
        if(counter7==2):
            teast.pop(0)
            pe.pop(0)
            EC_list.pop(trainindex)
            ui.comboBox.clear()
            ui.comboBox.addItems(EC_list)
        elif(counter7==3):
            teast.pop(1)
            pe.pop(1)
            EC_list.pop(trainindex)
            ui.comboBox.clear()
            ui.comboBox.addItems(EC_list)
        else:
            teast.pop(2)
            pe.pop(2)
            EC_list.pop(trainindex)
            ui.comboBox.clear()
            ui.comboBox.addItems(EC_list)

    elif(first_char[0]=='8' and first_char[2]=='9'):
        if(counter7==4):
            teast.pop(0)
            pe.pop(0)
            counter7=7
            EC_list.pop(trainindex)
            ui.comboBox.clear()
            ui.comboBox.addItems(EC_list)
        elif(counter7==5):
            teast.pop(1)
            pe.pop(1)
            counter7=8
            EC_list.pop(trainindex)
            ui.comboBox.clear()
            ui.comboBox.addItems(EC_list)
        elif(counter7==6):
            teast.pop(2)
            pe.pop(2)
            counter7=9
            EC_list.pop(trainindex)
            ui.comboBox.clear()
            ui.comboBox.addItems(EC_list)
        else:
            teast.pop(3)
            pe.pop(3)
            counter7=10
            EC_list.pop(trainindex)
            ui.comboBox.clear()
            ui.comboBox.addItems(EC_list)

    elif(first_char[0]=='8' and first_char[2]=='0'):
        if(counter7==7):
            teast.pop(0)
            pe.pop(0)
            counter7=11
            EC_list.pop(trainindex)
            ui.comboBox.clear()
            ui.comboBox.addItems(EC_list)
        elif(counter7==8):
            teast.pop(1)
            pe.pop(1)
            counter7=12
            EC_list.pop(trainindex)
            ui.comboBox.clear()
            ui.comboBox.addItems(EC_list)
        elif(counter7==9):
            teast.pop(2)
            pe.pop(2)
            counter7=13
            EC_list.pop(trainindex)
            ui.comboBox.clear()
            ui.comboBox.addItems(EC_list)
        elif(counter7==10):
            teast.pop(3)
            pe.pop(3)
            counter7=14
            EC_list.pop(trainindex)
            ui.comboBox.clear()
            ui.comboBox.addItems(EC_list)
        else:
            teast.pop(4)
            pe.pop(4)
            counter7=15
            EC_list.pop(trainindex)
            ui.comboBox.clear()
            ui.comboBox.addItems(EC_list)

    elif(first_char[0]=='8' and first_char[2]=='1'):
        if(counter7==11):
            teast.pop(0)
            pe.pop(0)
            EC_list.pop(trainindex)
            ui.comboBox.clear()
            ui.comboBox.addItems(EC_list)
        elif(counter7==12):
            teast.pop(1)
            pe.pop(1)
            EC_list.pop(trainindex)
            ui.comboBox.clear()
            ui.comboBox.addItems(EC_list)
        elif(counter7==13):
            teast.pop(2)
            pe.pop(2)
            EC_list.pop(trainindex)
            ui.comboBox.clear()
            ui.comboBox.addItems(EC_list)
        elif(counter7==14):
            teast.pop(3)
            pe.pop(3)
            EC_list.pop(trainindex)
            ui.comboBox.clear()
            ui.comboBox.addItems(EC_list)
        elif(counter7==15):
            teast.pop(4)
            pe.pop(4)
            EC_list.pop(trainindex)
            ui.comboBox.clear()
            ui.comboBox.addItems(EC_list)
        else:
            teast.pop(5)
            pe.pop(5)
            EC_list.pop(trainindex)
            ui.comboBox.clear()
            ui.comboBox.addItems(EC_list)

ui.pushButton_7.clicked.connect(Start)
ui.pushButton_3.clicked.connect(stop)
ui.pushButton_9.clicked.connect(emergency.emergency)
ui.pushButton_12.clicked.connect(report)
ui.pushButton_8.clicked.connect(REROUTING)
ui.pushButton_6.clicked.connect(S_O_S)
ui.pushButton_15.clicked.connect(addtrainwest)
ui.pushButton_16.clicked.connect(addtraineast)
ui.pushButton_23.clicked.connect(removetrain)
ui.pushButton_20.clicked.connect(endprocess)

conn = mysql.connector.connect(host='localhost',
                               database='monorail',
                               user='root',
)

cursor = conn.cursor()
csql = "UPDATE trains SET status = 'Available'"
cursor.execute(csql)
conn.commit()

EC1=[]
EC1.append(ec(screen, c.r, c.h,newx,newy,580,185,595,155,610,185,165,595))
EC1.append(ec(screen,c.a, c.b,newx,newy,1120, 110,1135, 80,1150, 110,90,1135))
EC1.append(ec(screen,c.c, c.d,newx,newy,1230, 510,1245, 480,1260, 510,490,1245))
EC1.append(ec(screen, c.e, c.f,newx,newy,350, 610, 365, 580,380, 610,590,365))
flag=None

ui.checkBox.click()
ui.horizontalSlider.setValue(15)

def changespeedValue(value):
    trainindex=ui.comboBox.currentIndex()
    choice = str(ui.comboBox.currentText())
    first_char = re.findall("\d",choice)
    global speed
    c=len(twest)
    check = ui.checkBox.checkState()
    if check == 2 :
        for i in range(len(twest)):
            if value==0:
                stop()
            elif value>0 and value<=19:
                twest[i].speed=0.02
            elif value>19 and value<=33:
                twest[i].speed=0.04
            elif value>33 and value<=46:
                twest[i].speed=0.08
            elif value>46 and value<=59:
                twest[i].speed=0.12
            elif value>59 and value<=73:
                twest[i].speed=0.16
            elif value>73 and value<=82:
                twest[i].speed=0.18
            elif value>82 and value<=92:
                twest[i].speed=0.22
            elif value>92:
                twest[i].speed=0.26

        for i in range(len(teast)):
            cursor = conn.cursor()
            if value==0:
                stop()
                csql = "UPDATE trains SET average_speed = '0'"
            elif value>0 and value<=19:
                teast[i].speed=0.02
                csql = "UPDATE trains SET average_speed = '10'"
            elif value>19 and value<=33:
                teast[i].speed=0.04
                csql = "UPDATE trains SET average_speed = '20'"
            elif value>33 and value<=46:
                teast[i].speed=0.08
                csql = "UPDATE trains SET average_speed = '30'"
            elif value>46 and value<=59:
                teast[i].speed=0.12
                csql = "UPDATE trains SET average_speed = '40'"
            elif value>59 and value<=73:
                teast[i].speed=0.16
                csql = "UPDATE trains SET average_speed = '50'"
            elif value>73 and value<=82:
                teast[i].speed=0.18
                csql = "UPDATE trains SET average_speed = '60'"
            elif value>82 and value<=92:
                teast[i].speed=0.22
                csql = "UPDATE trains SET average_speed = '70'"
            elif value>92:
                teast[i].speed=0.26
                csql = "UPDATE trains SET average_speed = '80'"
            cursor.execute(csql)
            conn.commit()      
                
    if first_char[0]=='5':
        cursor = conn.cursor()
        speedchoice = [int(choice)]
        val = (speedchoice)
        if value==0 and twest[trainindex].flagspeed == 1:
            twest[trainindex].speed=0
            csql2 = "UPDATE trains SET average_speed = '0' where id = %s "
            cursor.execute(csql2, val)
            conn.commit()
        elif value>0 and value<=19 and twest[trainindex].flagspeed == 1:
            #Start()
            twest[trainindex].speed=0.02
            csql2 = "UPDATE trains SET average_speed = '10' where id = %s "
            cursor.execute(csql2, val)
            conn.commit()
        elif value>19 and value<=33 and twest[trainindex].flagspeed == 1:
            twest[trainindex].speed=0.04
            csql2 = "UPDATE trains SET average_speed = '20' where id = %s "
            cursor.execute(csql2, val)
            conn.commit()
        elif value>33 and value<=46 and twest[trainindex].flagspeed == 1:
            twest[trainindex].speed=0.08
            csql2 = "UPDATE trains SET average_speed = '30' where id = %s "
            cursor.execute(csql2, val)
            conn.commit()
        elif value>46 and value<=59 and twest[trainindex].flagspeed == 1:
            twest[trainindex].speed=0.12
            csql2 = "UPDATE trains SET average_speed = '40' where id = %s "
            cursor.execute(csql2, val)
            conn.commit()
        elif value>59 and value<=73 and twest[trainindex].flagspeed == 1:
            twest[trainindex].speed=0.16
            csql2 = "UPDATE trains SET average_speed = '50' where id = %s "
            cursor.execute(csql2, val)
            conn.commit()
        elif value>73 and value<=82 and twest[trainindex].flagspeed == 1:
            twest[trainindex].speed=0.18
            csql2 = "UPDATE trains SET average_speed = '60' where id = %s "
            cursor.execute(csql2, val)
            conn.commit()
        elif value>82 and value<=92 and twest[trainindex].flagspeed == 1:
            twest[trainindex].speed=0.22
            csql2 = "UPDATE trains SET average_speed = '70' where id = %s "
            cursor.execute(csql2, val)
            conn.commit()
        elif value>92 and twest[trainindex].flagspeed == 1:
            twest[trainindex].speed=0.25       
            csql2 = "UPDATE trains SET average_speed = '80' where id = %s "
            cursor.execute(csql2, val)
            conn.commit()
        
    if first_char[0]=='8':
        cursor = conn.cursor()
        speedchoice = [int(choice)]
        val = (speedchoice)
        if value==0 and teast[trainindex-c].flagspeed == 1:
            teast[trainindex-c].speed=0
            csql2 = "UPDATE trains SET average_speed = '0' where id = %s "
            cursor.execute(csql2, val)
            conn.commit()
        elif value>0 and value<=19 and teast[trainindex-c].flagspeed == 1:
            #Start()
            teast[trainindex-c].speed=0.02
            csql2 = "UPDATE trains SET average_speed = '10' where id = %s "
            cursor.execute(csql2, val)
            conn.commit()
        elif value>19 and value<=33 and teast[trainindex-c].flagspeed == 1:
            teast[trainindex-c].speed=0.04
            csql2 = "UPDATE trains SET average_speed = '20' where id = %s "
            cursor.execute(csql2, val)
            conn.commit()
        elif value>33 and value<=46 and teast[trainindex-c].flagspeed == 1:
            teast[trainindex-c].speed=0.08
            csql2 = "UPDATE trains SET average_speed = '30' where id = %s "
            cursor.execute(csql2, val)
            conn.commit()
        elif value>46 and value<=59 and teast[trainindex-c].flagspeed == 1:
            teast[trainindex-c].speed=0.12
            csql2 = "UPDATE trains SET average_speed = '40' where id = %s "
            cursor.execute(csql2, val)
            conn.commit()
        elif value>59 and value<=73 and teast[trainindex-c].flagspeed == 1:
            teast[trainindex-c].speed=0.16
            csql2 = "UPDATE trains SET average_speed = '50' where id = %s "
            cursor.execute(csql2, val)
            conn.commit()
        elif value>73 and value<=82 and teast[trainindex-c].flagspeed == 1:
            teast[trainindex-c].speed=0.18
            csql2 = "UPDATE trains SET average_speed = '60' where id = %s "
            cursor.execute(csql2, val)
            conn.commit()
        elif value>82 and value<=92 and teast[trainindex-c].flagspeed == 1:
            teast[trainindex-c].speed=0.22
            csql2 = "UPDATE trains SET average_speed = '70' where id = %s "
            cursor.execute(csql2, val)
            conn.commit()
        elif value>92 and teast[trainindex-c].flagspeed == 1:
            teast[trainindex-c].speed=0.25       
            csql2 = "UPDATE trains SET average_speed = '80' where id = %s "
            cursor.execute(csql2, val)
            conn.commit()
                
while running:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit(app.exec_())
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if EC1[0].impEC().collidepoint(event.pos):
                    rectangle_draging = True
                    mouse_x, mouse_y = event.pos
                    offset_x = EC1[0].ex - mouse_x
                    offset_y = EC1[0].ey - mouse_y
                    offset_x1 = EC1[0].ex1 - mouse_x
                    offset_y1 = EC1[0].ey1 - mouse_y
                    offset_x2 = EC1[0].ex2 - mouse_x
                    offset_y2 = EC1[0].ey2 - mouse_y
                    offset_ys = EC1[0].ys - mouse_x
                    offset_yl = EC1[0].yl - mouse_y
                    flag=0
                if EC1[1].impEC().collidepoint(event.pos):
                    rectangle_draging = True
                    mouse_x, mouse_y = event.pos
                    offset_x = EC1[1].ex - mouse_x
                    offset_y = EC1[1].ey - mouse_y
                    offset_x1 = EC1[1].ex1 - mouse_x
                    offset_y1 = EC1[1].ey1 - mouse_y
                    offset_x2 = EC1[1].ex2 - mouse_x
                    offset_y2 = EC1[1].ey2 - mouse_y
                    offset_ys = EC1[1].ys - mouse_x
                    offset_yl = EC1[1].yl - mouse_y
                    flag=1
                if EC1[2].impEC().collidepoint(event.pos):
                    rectangle_draging = True
                    mouse_x, mouse_y = event.pos
                    offset_x = EC1[2].ex - mouse_x
                    offset_y = EC1[2].ey - mouse_y
                    offset_x1 = EC1[2].ex1 - mouse_x
                    offset_y1 = EC1[2].ey1 - mouse_y
                    offset_x2 = EC1[2].ex2 - mouse_x
                    offset_y2 = EC1[2].ey2 - mouse_y
                    offset_ys = EC1[2].ys - mouse_x
                    offset_yl = EC1[2].yl - mouse_y
                    flag=2

                if EC1[3].impEC().collidepoint(event.pos):
                    rectangle_draging = True
                    mouse_x, mouse_y = event.pos
                    offset_x = EC1[3].ex - mouse_x
                    offset_y = EC1[3].ey - mouse_y
                    offset_x1 = EC1[3].ex1 - mouse_x
                    offset_y1 = EC1[3].ey1 - mouse_y
                    offset_x2 = EC1[3].ex2 - mouse_x
                    offset_y2 = EC1[3].ey2 - mouse_y
                    offset_ys = EC1[3].ys - mouse_x
                    offset_yl = EC1[3].yl - mouse_y
                    flag=3
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                rectangle_draging = False
                if flag==0 :
                    print(EC1[0].ex)
                    print(EC1[0].ey)
                    if EC1[0].ex<=630 and EC1[0].ex>500 and EC1[0].ey<=228:
                        EC1[0].ex=580
                        EC1[0].ey=185
                        EC1[0].ex1=595
                        EC1[0].ey1=155
                        EC1[0].ex2=610
                        EC1[0].ey2=185
                        EC1[0].yl=165
                        EC1[0].ys=595
                        counter=1
                        print('ceX1')
                    elif EC1[0].ex<=496 and EC1[0].ex>=360 and EC1[0].ey<=160:
                        EC1[0].ex = 430
                        EC1[0].ey = 119
                        EC1[0].ex1 = 460
                        EC1[0].ey1 = 119
                        EC1[0].ex2 = 445
                        EC1[0].ey2 = 89
                        EC1[0].yl = 96
                        EC1[0].ys = 445
                        counter=0
                        print('ceX2')
                    elif EC1[0].ex<=360 and EC1[0].ex>=316 and EC1[0].ey<=160:
                        EC1[0].ex = 355
                        EC1[0].ey = 119
                        EC1[0].ex1 = 385
                        EC1[0].ey1 = 119
                        EC1[0].ex2 = 370
                        EC1[0].ey2 = 89
                        EC1[0].yl = 96
                        EC1[0].ys = 370
                        counter=0
                        print('ceX22')
                    elif EC1[0].ex<=316 and EC1[0].ey<=160:
                        EC1[0].ex = 275
                        EC1[0].ey = 55
                        EC1[0].ex1 = 305
                        EC1[0].ey1 = 55
                        EC1[0].ex2 = 290
                        EC1[0].ey2 = 25
                        EC1[0].yl = 32
                        EC1[0].ys = 290
                        counter=0
                        print('ceX222')
                    elif EC1[0].ex>-14 and EC1[0].ex<=345 and EC1[0].ey>=166 and EC1[0].ey<299:
                        EC1[0].ex = 313
                        EC1[0].ey = 195
                        EC1[0].ex1 = 343
                        EC1[0].ey1 = 195
                        EC1[0].ex2 = 328
                        EC1[0].ey2 = 161
                        EC1[0].yl=170
                        EC1[0].ys = 328
                        counter=0
                        print('ceX33')
                    elif EC1[0].ex>345 and EC1[0].ex<=463 and EC1[0].ey>=166 and EC1[0].ey<299:
                        EC1[0].ex = 378
                        EC1[0].ey = 208
                        EC1[0].ex1 = 408
                        EC1[0].ey1 = 208
                        EC1[0].ex2 = 393
                        EC1[0].ey2 = 174
                        EC1[0].yl=183
                        EC1[0].ys = 393
                        counter=0
                        print('ceX3')
                    elif EC1[0].ex>631 and  EC1[0].ex<790 and EC1[0].ey<=208:
                        EC1[0].ex = 675
                        EC1[0].ey = 156
                        EC1[0].ex1 = 705
                        EC1[0].ey1 = 156
                        EC1[0].ex2 = 690
                        EC1[0].ey2 = 126
                        EC1[0].yl=136
                        EC1[0].ys = 690
                        counter=0
                        print('ceX4')
                    elif  EC1[0].ey>213 and EC1[0].ex<=760 and EC1[0].ex>=465:
                        EC1[0].ex = 602
                        EC1[0].ey = 310
                        EC1[0].ex1 = 632
                        EC1[0].ey1 = 310
                        EC1[0].ex2 = 617
                        EC1[0].ey2 = 280
                        EC1[0].yl=287
                        EC1[0].ys = 617
                        counter=0
                        print('ceX5')
                if flag==1 :
                    print(EC1[1].ex)
                    print(EC1[1].ey)
                    if  EC1[1].ex<=1170 and EC1[1].ex>1050 and EC1[1].ey<=120:
                        EC1[1].ex=1126
                        EC1[1].ey=117
                        EC1[1].ex1=1156
                        EC1[1].ey1=117
                        EC1[1].ex2=1141
                        EC1[1].ey2=87
                        EC1[1].yl=94
                        EC1[1].ys=1141
                        counter2=1
                        print('ceX11')
                    elif EC1[1].ex>860 and EC1[1].ex<=1050  and EC1[1].ey<=150:
                        EC1[1].ex = 903
                        EC1[1].ey = 124
                        EC1[1].ex1 = 933
                        EC1[1].ey1 = 124
                        EC1[1].ex2 = 918
                        EC1[1].ey2 = 94
                        EC1[1].yl = 101
                        EC1[1].ys = 918
                        counter2=0
                        print('ceX221')
                    elif EC1[1].ex>880 and EC1[1].ex<=1145 and EC1[1].ey<=320 and EC1[1].ey>150:
                        EC1[1].ex = 985
                        EC1[1].ey = 225
                        EC1[1].ex1 = 1015
                        EC1[1].ey1 = 225
                        EC1[1].ex2 = 1000
                        EC1[1].ey2 = 195
                        EC1[1].yl = 202
                        EC1[1].ys = 1000
                        counter2=0
                        print('ceX222')
                    elif EC1[1].ex>1180 and EC1[1].ex<=1500 and EC1[1].ey<=320 and EC1[1].ey>10:
                        EC1[1].ex = 1265
                        EC1[1].ey = 87
                        EC1[1].ex1 = 1295
                        EC1[1].ey1 = 87
                        EC1[1].ex2 = 1280
                        EC1[1].ey2 = 57
                        EC1[1].yl = 64
                        EC1[1].ys = 1280
                        counter2=0
                        print('ceX223')
                    elif EC1[1].ex>=650 and EC1[1].ex<=880 and EC1[1].ey>=10 and EC1[1].ey<150:
                        EC1[1].ex = 798
                        EC1[1].ey = 71
                        EC1[1].ex1 = 828
                        EC1[1].ey1 = 71
                        EC1[1].ex2 = 813
                        EC1[1].ey2 = 41
                        EC1[1].yl=48
                        EC1[1].ys =813
                        counter2=0
                        print('ceX33')
                    elif EC1[1].ex>=650 and EC1[1].ex<=880 and EC1[1].ey>=150 and EC1[1].ey<260:
                        EC1[1].ex = 795
                        EC1[1].ey = 170
                        EC1[1].ex1 = 825
                        EC1[1].ey1 = 170
                        EC1[1].ex2 = 810
                        EC1[1].ey2 = 140
                        EC1[1].yl=147
                        EC1[1].ys =810
                        counter2=0
                        print('ceX332')
                if flag==2:
                    print(EC1[2].ex)
                    print(EC1[2].ey)
                    if EC1[2].ex>=1170 and EC1[2].ex<1285 and EC1[2].ey>350 and EC1[2].ey<=540:
                        EC1[2].ex=1230
                        EC1[2].ey=510
                        EC1[2].ex1=1245
                        EC1[2].ey1=480
                        EC1[2].ex2=1260
                        EC1[2].ey2=510
                        EC1[2].yl=490
                        EC1[2].ys=1245
                        counter3=1
                        print('ceX1')
                    elif EC1[2].ex<1165 and EC1[2].ex>975 and EC1[2].ey>535:
                        EC1[2].ex=1030
                        EC1[2].ey=585
                        EC1[2].ex1=1045
                        EC1[2].ey1=555
                        EC1[2].ex2=1060
                        EC1[2].ey2=585
                        EC1[2].yl=565
                        EC1[2].ys=1045
                        counter3=0
                        print('ceX12')
                    elif EC1[2].ex<1476 and EC1[2].ex>=1172 and EC1[2].ey>=545 and EC1[2].ey<700:
                        EC1[2].ex=1199
                        EC1[2].ey=595
                        EC1[2].ex1=1214
                        EC1[2].ey1=565
                        EC1[2].ex2=1229
                        EC1[2].ey2=595
                        EC1[2].yl=575
                        EC1[2].ys=1214
                        counter3=0
                        print('ceX1222')
                    elif EC1[2].ex<1473 and EC1[2].ex>=1293 and EC1[2].ey>=265 and EC1[2].ey<620:
                        EC1[2].ex=1304
                        EC1[2].ey=437
                        EC1[2].ex1=1319
                        EC1[2].ey1=407
                        EC1[2].ex2=1334
                        EC1[2].ey2=437
                        EC1[2].yl=417
                        EC1[2].ys=1319
                        counter3=0
                        print('ceX12222')
                    elif EC1[2].ex<=1162 and EC1[2].ex>=1070 and EC1[2].ey>=343 and EC1[2].ey<529:
                        EC1[2].ex=1086
                        EC1[2].ey=511
                        EC1[2].ex1=1101
                        EC1[2].ey1=481
                        EC1[2].ex2=1116
                        EC1[2].ey2=511
                        EC1[2].yl=491
                        EC1[2].ys=1101
                        counter3=0
                        print('ceX122222')
                    elif EC1[2].ex<906 and EC1[2].ex>670 and EC1[2].ey>350 and EC1[2].ey<=535:
                        EC1[2].ex=880
                        EC1[2].ey=460
                        EC1[2].ex1=895
                        EC1[2].ey1=430
                        EC1[2].ex2=910
                        EC1[2].ey2=460
                        EC1[2].yl=440
                        EC1[2].ys=895
                        counter3=0
                        print('ceX1')
                    elif EC1[2].ex>905 and EC1[2].ex<1070 and EC1[2].ey>345 and EC1[2].ey<=535:
                        EC1[2].ex=951
                        EC1[2].ey=503
                        EC1[2].ex1=966
                        EC1[2].ey1=473
                        EC1[2].ex2=981
                        EC1[2].ey2=503
                        EC1[2].yl=483
                        EC1[2].ys=966
                        counter3=0
                        print('ceX11111111111111111111111111')
                    elif EC1[2].ex>800 and EC1[2].ex<970 and EC1[2].ey>530 and EC1[2].ey<=700:
                        EC1[2].ex=892
                        EC1[2].ey=593
                        EC1[2].ex1=907
                        EC1[2].ey1=563
                        EC1[2].ex2=922
                        EC1[2].ey2=593
                        EC1[2].yl=573
                        EC1[2].ys=907
                        counter3=0
                        print('ceX11111111111111111111111111')
                if flag==3:
                    if EC1[3].ex<=460 and EC1[3].ex>0 and EC1[3].ey>515:
                        EC1[3].ex=350
                        EC1[3].ey=610
                        EC1[3].ex1=365
                        EC1[3].ey1=580
                        EC1[3].ex2=380
                        EC1[3].ey2=610
                        EC1[3].yl=590
                        EC1[3].ys=365
                        counter4=1
                        print('ceX1')
                    elif EC1[3].ex<=400 and EC1[3].ex>0 and EC1[3].ey<515:
                        EC1[3].ex=350
                        EC1[3].ey=480
                        EC1[3].ex1=365
                        EC1[3].ey1=450
                        EC1[3].ex2=380
                        EC1[3].ey2=480
                        EC1[3].yl=460
                        EC1[3].ys=365
                        counter4=0
                        print('ceX2')
                    elif EC1[3].ex<=630 and EC1[3].ex>400 and EC1[3].ey<700:
                        EC1[3].ex=510
                        EC1[3].ey=500
                        EC1[3].ex1=525
                        EC1[3].ey1=470
                        EC1[3].ex2=540
                        EC1[3].ey2=500
                        EC1[3].yl=480
                        EC1[3].ys=525
                        counter4=0
                        print('ceX3')
                    elif EC1[3].ex>=630 and EC1[3].ex<860 and EC1[3].ey<700:
                        EC1[3].ex=760
                        EC1[3].ey=580
                        EC1[3].ex1=775
                        EC1[3].ey1=550
                        EC1[3].ex2=790
                        EC1[3].ey2=580
                        EC1[3].yl=560
                        EC1[3].ys=775
                        counter4=0
                        print('ceX4')

        elif event.type == pygame.MOUSEMOTION:
            if rectangle_draging:
                mouse_x, mouse_y = event.pos
                EC1[flag].ex = mouse_x + offset_x
                EC1[flag].ey = mouse_y + offset_y
                EC1[flag].ex1 = mouse_x + offset_x1
                EC1[flag].ey1 = mouse_y + offset_y1
                EC1[flag].ex2 = mouse_x + offset_x2
                EC1[flag].ey2 = mouse_y + offset_y2
                EC1[flag].ys = mouse_x + offset_ys
                EC1[flag].yl = mouse_y + offset_yl

        if event.type == VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            bg = pygame.image.load("map3.jpg")
            bg = pygame.transform.scale(bg, (event.w, event.h))
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit(app.exec_())

    pygame.display.update()
    screen_info = pygame.display.Info()  # Required to set a good resolution for the game screen

    for i in range(len(twest)):
        if twest[i].positionflg==0:
            if (twest[i].x > 15 and twest[i].x < 55) and (twest[i].y > 205 and twest[i].y < 215):
                pw[i]="600 m to Ard El Maared"
            elif (twest[i].x > 65 and twest[i].x < 95) and (twest[i].y > 205 and twest[i].y < 215):
                pw[i]="300 m to Ard El Maared"
            elif (twest[i].x > 110 and twest[i].x < 180) and (twest[i].y > 254 and twest[i].y < 260):#5od balak
                pw[i]="600 m to Cairo Festival City"
            elif (twest[i].x > 180 and twest[i].x < 250) and (twest[i].y > 290 and twest[i].y < 300):#5od balak
                pw[i]="300 m to Cairo Festival City"
            elif (twest[i].x > 250 and twest[i].x < 350) and (twest[i].y > 310 and twest[i].y <= 318):
                pw[i]="600 m to DownTown"
            elif (twest[i].x > 350 and twest[i].x < 450) and (twest[i].y > 310 and twest[i].y <= 318):
                pw[i]="300 m to DownTown"
            elif (twest[i].x > 450 and twest[i].x < 550) and (twest[i].y > 316 and twest[i].y <= 319):
                pw[i]="600 m to el Ghaz 1"
            elif (twest[i].x > 550 and twest[i].x < 650) and (twest[i].y > 316 and twest[i].y <= 319):
                pw[i]="300 m to el Ghaz 1"
            elif (twest[i].x > 650 and twest[i].x < 750) and (twest[i].y > 316 and twest[i].y <= 319):
                pw[i]="600 m to Mogmaa El Bonok"
            elif (twest[i].x > 750 and twest[i].x < 850) and (twest[i].y > 316 and twest[i].y <= 319):
                pw[i]="300 m to Mogmaa El Bonok"
            elif (twest[i].x > 850 and twest[i].x < 950) and (twest[i].y > 316 and twest[i].y <= 319):
                pw[i]="600 m to Mostashfa El Gawy"
            elif (twest[i].x > 950 and twest[i].x < 1050) and (twest[i].y > 316 and twest[i].y <= 319):
                pw[i]="300 m to Mostashfa El Gawy"
            elif (twest[i].x > 1050 and twest[i].x < 1150) and (twest[i].y > 316 and twest[i].y <= 319):
                pw[i]="600 m to Ghaz 2"
            elif (twest[i].x > 1150 and twest[i].x < 1270) and (twest[i].y > 316 and twest[i].y <= 319):
                pw[i]="300 m to Ghaz 2"
            elif (twest[i].x > 1270 and twest[i].x < 1320) and (twest[i].y > 260 and twest[i].y <= 300):
                pw[i]="600 m to Ghandor Auto"
            elif (twest[i].x > 1320 and twest[i].x < 1370) and (twest[i].y > 260 and twest[i].y <= 300):
                pw[i]="300 m to Ghandor Auto"
            elif (twest[i].x > 1370 and twest[i].x < 1420) and (twest[i].y > 202 and twest[i].y <= 260):
                pw[i]="600 m to Dusit"
            elif (twest[i].x > 1420 and twest[i].x < 1470) and (twest[i].y > 202 and twest[i].y <= 260):
                pw[i]="300 m to Dusit"
            if (twest[i].x > 1469 and twest[i].x < 1471):
                twest[i].positionflg=1
        #coming back
        if twest[i].positionflg==1:
            if (twest[i].x > 1420 and twest[i].x < 1470) and (twest[i].y > 202 and twest[i].y <= 280):
                pw[i]="600 m to Ghandor Auto"
            elif (twest[i].x > 1376 and twest[i].x < 1420) and (twest[i].y > 202 and twest[i].y < 280):
                pw[i]="300 m to Ghandor Auto"
            elif (twest[i].x > 1330 and twest[i].x < 1360) and (twest[i].y > 280 and twest[i].y < 330):#5od balak
                pw[i]="600 m to EL Ghaz 2"
            elif (twest[i].x > 1280 and twest[i].x < 1310) and (twest[i].y > 280 and twest[i].y < 330):#5od balak
                pw[i]="300 m to EL Ghaz 2"
            elif (twest[i].x > 1150 and twest[i].x < 1276) and (twest[i].y > 338 and twest[i].y <= 343):
                pw[i]="600 m to Mostashfa El Gawy"
            elif (twest[i].x > 1050 and twest[i].x < 1150) and (twest[i].y > 338 and twest[i].y <= 343):
                pw[i]="300 m to Mostashfa El Gawy"
            elif (twest[i].x > 950 and twest[i].x < 1050) and (twest[i].y > 338 and twest[i].y <= 343):
                pw[i]="600 m to Mogmaa El Bonok"
            elif (twest[i].x > 850 and twest[i].x < 950) and (twest[i].y > 338 and twest[i].y <= 343):
                pw[i]="300 m to Mogmaa El Bonok"
            elif (twest[i].x > 750 and twest[i].x < 850) and (twest[i].y > 338 and twest[i].y <= 343):
                pw[i]="600 m to El Ghaz 1"
            elif (twest[i].x > 650 and twest[i].x < 750) and (twest[i].y > 338 and twest[i].y <= 343):
                pw[i]="300 m to El Ghaz 1"
            elif (twest[i].x > 550 and twest[i].x < 650) and (twest[i].y > 338 and twest[i].y <= 343):
                pw[i]="600 m to DownTown"
            elif (twest[i].x > 450 and twest[i].x < 550) and (twest[i].y > 338 and twest[i].y <= 343):
                pw[i]="300 m to DownTown"
            elif (twest[i].x > 350 and twest[i].x < 450) and (twest[i].y > 338 and twest[i].y <= 343):
                pw[i]="600 m to Cairo Festival City"
            elif (twest[i].x > 250 and twest[i].x < 350) and (twest[i].y > 338 and twest[i].y <= 343):
                pw[i]="300 m to Cairo Festival City"
            elif (twest[i].x > 170 and twest[i].x < 250) and (twest[i].y > 290 and twest[i].y <= 300):
                pw[i]="600 m to Ard El Maared"
            elif (twest[i].x > 110 and twest[i].x < 170) and (twest[i].y > 260 and twest[i].y <= 270):
                pw[i]="300 m to Ard El Maared"
            elif (twest[i].x > 65 and twest[i].x < 110) and (twest[i].y > 230 and twest[i].y <= 238):
                pw[i]="600 m to El Moshir Tantawy"
            elif (twest[i].x > 15 and twest[i].x < 65) and (twest[i].y > 230 and twest[i].y <= 238):
                pw[i]="300 m to El Moshir Tantawy"
            if (twest[i].x > 14 and twest[i].x < 16):
                twest[i].positionflg=0

    for i in range(len(teast)):
        if teast[i].positionflg==0:
            if (teast[i].x > 15 and teast[i].x < 55) and (teast[i].y > 205 and teast[i].y < 215):
                pe[i]="600 m to Ard El Maared"
            elif (teast[i].x > 65 and teast[i].x < 95) and (teast[i].y > 205 and teast[i].y < 215):
                pe[i]="300 m to Ard El Maared"
            elif (teast[i].x > 110 and teast[i].x < 180) and (teast[i].y > 214 and teast[i].y < 310):#5od balak
                pe[i]="600 m to Cairo Festival City"
            elif (teast[i].x > 180 and teast[i].x < 250) and (teast[i].y > 214 and teast[i].y < 310):#5od balak
                pe[i]="300 m to Cairo Festival City"
            elif (teast[i].x > 250 and teast[i].x < 350) and (teast[i].y > 310 and teast[i].y <= 318):
                pe[i]="600 m to DownTown"
            elif (teast[i].x > 350 and teast[i].x < 450) and (teast[i].y > 310 and teast[i].y <= 318):
                pe[i]="300 m to DownTown"
            elif (teast[i].x > 450 and teast[i].x < 550) and (teast[i].y > 310 and teast[i].y <= 318):
                pe[i]="600 m to El Ghaz 1"
            elif (teast[i].x > 550 and teast[i].x < 650) and (teast[i].y > 310 and teast[i].y <= 318):
                pe[i]="300 m to El Ghaz 1"
            elif (teast[i].x > 650 and teast[i].x < 750) and (teast[i].y > 310 and teast[i].y <= 318):
                pe[i]="600 m to Mogmaa El Bonok"
            elif (teast[i].x > 750 and teast[i].x < 850) and (teast[i].y > 310 and teast[i].y <= 318):
                pe[i]="300 m to Mogmaa El Bonok"
            elif (teast[i].x > 850 and teast[i].x < 950) and (teast[i].y > 310 and teast[i].y <= 318):
                pe[i]="600 m to Mostashfa El Gawy"
            elif (teast[i].x > 950 and teast[i].x < 1050) and (teast[i].y > 310 and teast[i].y <= 318):
                pe[i]="300 m to Mostashfa El Gawy"
            elif (teast[i].x > 1050 and teast[i].x < 1150) and (teast[i].y > 310 and teast[i].y <= 318):
                pe[i]="600 m to Ghaz 2"
            elif (teast[i].x > 1150 and teast[i].x < 1270) and (teast[i].y > 310 and teast[i].y <= 318):
                pe[i]="300 m to Ghaz 2"
            elif (teast[i].x > 1270 and teast[i].x < 1320) and (teast[i].y > 260 and teast[i].y <= 270):
                pe[i]="600 m to Ghandor Auto"
            elif (teast[i].x > 1320 and teast[i].x < 1370) and (teast[i].y > 260 and teast[i].y <= 270):
                pe[i]="300 m to Ghandor Auto"
            elif (teast[i].x > 1370 and teast[i].x < 1420) and (teast[i].y > 260 and teast[i].y <= 270):
                pe[i]="600 m to Dusit"
            elif (teast[i].x > 1420 and teast[i].x < 1470) and (teast[i].y > 270 and teast[i].y <= 186):
                pe[i]="300 m to Dusit"
            if (teast[i].x > 1469 and teast[i].x < 1471):
                teast[i].positionflg=1
        #coming back
        if teast[i].positionflg==1:
            if (teast[i].x > 1400 and teast[i].x < 1470) and (teast[i].y > 230 and teast[i].y <= 241):
                pe[i]="600 m to Ghandor Auto"
            elif (teast[i].x > 1376 and teast[i].x < 1400) and (teast[i].y > 251 and teast[i].y < 270):
                pe[i]="300 m to Ghandor Auto"
            elif (teast[i].x > 1310 and teast[i].x < 1376) and (teast[i].y > 291 and teast[i].y < 300):#5od balak
                pe[i]="600 m to El Ghaz 2"
            elif (teast[i].x > 1276 and teast[i].x < 1310) and (teast[i].y > 310 and teast[i].y < 320):#5od balak
                pe[i]="300 m to El Ghaz 2"
            elif (teast[i].x > 1150 and teast[i].x < 1276) and (teast[i].y > 338 and teast[i].y <= 340):
                pe[i]="600 m to Mostashfa El Gawy"
            elif (teast[i].x > 1050 and teast[i].x < 1150) and (teast[i].y > 338 and teast[i].y <= 340):
                pe[i]="300 m to Mostashfa El Gawy"
            elif (teast[i].x > 950 and teast[i].x < 1050) and (teast[i].y > 338 and teast[i].y <= 340):
                pe[i]="600 m to Mogmaa El Bonok"
            elif (teast[i].x > 850 and teast[i].x < 950) and (teast[i].y > 338 and teast[i].y <= 340):
                pe[i]="300 m to Mogmaa El Bonok"
            elif (teast[i].x > 750 and teast[i].x < 850) and (teast[i].y > 338 and teast[i].y <= 340):
                pe[i]="600 m to El Ghaz 1"
            elif (teast[i].x > 650 and teast[i].x < 750) and (teast[i].y > 338 and teast[i].y <= 340):
                pe[i]="300 m to El Ghaz 1"
            elif (teast[i].x > 550 and teast[i].x < 650) and (teast[i].y > 338 and teast[i].y <= 340):
                pe[i]="600 m to DownTown"
            elif (teast[i].x > 450 and teast[i].x < 550) and (teast[i].y > 338 and teast[i].y <= 340):
                pe[i]="300 m to DownTown"
            elif (teast[i].x > 350 and teast[i].x < 450) and (teast[i].y > 338 and teast[i].y <= 340):
                pe[i]="600 m to Cairo Festival City"
            elif (teast[i].x > 250 and teast[i].x < 350) and (teast[i].y > 338 and teast[i].y <= 340):
                pe[i]="300 m to Cairo Festival City"
            elif (teast[i].x > 170 and teast[i].x < 280) and (teast[i].y > 290 and teast[i].y <= 300):
                pe[i]="600 m to Ard El Maared"
            elif (teast[i].x > 110 and teast[i].x < 170) and (teast[i].y > 260 and teast[i].y <= 270):
                pe[i]="300 m to Ard El Maared"
            elif (teast[i].x > 65 and teast[i].x < 110) and (teast[i].y > 230 and teast[i].y <= 238):
                pe[i]="600 m to El Moshir Tantawy"
            elif (teast[i].x > 15 and teast[i].x < 65) and (teast[i].y > 230 and teast[i].y <= 238):
                pe[i]="300 m to El Moshir Tantawy"
            if (teast[i].x > 14 and teast[i].x < 16):
                teast[i].positionflg=0
    trainpos=pw+pe
    d = [516,517,518,816,817,818]
    i = 0
    cursor = conn.cursor()
    while i < len(trainpos):
       csql = "UPDATE trains SET Position = %s WHERE ID = %s"
       val = (trainpos[i],EC_list[i])
       i=i+1
       cursor.execute(csql, val)
       conn.commit()

    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        running = 0
        sys.exit(app.exec_())
    screen.blit(bg, (0, 0))

    newx = (screen_info.current_w / 1500)
    newy = (screen_info.current_h / 700)
    # board = create_board()
    # board_surf = create_board_surf()
    # piece, sx, sy = get_square_under_mouse(board)
    # screen.blit(board_surf, BOARD_POS)
    # if sx != None:
    #         rect = (BOARD_POS[0] + sx * TILESIZE, BOARD_POS[1] + sy * TILESIZE, TILESIZE, TILESIZE)
    #         pygame.draw.rect(screen, (255, 0, 0, 50), rect, 2)
    
    for i in range(len(twest)):
        if(twest[i].x == 15):
            cursor = conn.cursor()
            now = datetime.now()
            now1=[now]
            twestidr=[twest[i].id]
            csql = "UPDATE trains SET departure_time = %s WHERE id = %s"
            val = (now1[0],twestidr[0])
            cursor.execute(csql,val)
            conn.commit()       
    
    for i in range(len(twest)):
        if(twest[i].x >1470 and twest[i].x <1472 ):
            cursor = conn.cursor()
            now = datetime.now()
            now1=[now]
            twestidr=[twest[i].id]
            csql = "UPDATE trains SET expected_at = %s WHERE id = %s"
            val = (now1[0],twestidr[0])
            cursor.execute(csql,val)
            conn.commit()          
            
    for i in range(len(teast)):
        if(teast[i].x == 1473):
            cursor = conn.cursor()
            nowe = datetime.now()
            now2=[nowe]
            teastidr=[teast[i].id]
            csql = "UPDATE trains SET departure_time = %s WHERE id = %s"
            val = (now2[0],teastidr[0])
            cursor.execute(csql,val)
            conn.commit()
    
    for i in range(len(teast)):
        if(teast[i].x > 13 and teast[i].x < 15):
            cursor = conn.cursor()
            nowe = datetime.now()
            now2=[nowe]
            teastidr=[teast[i].id]
            csql = "UPDATE trains SET expected_at = %s WHERE id = %s"
            val = (now2[0],teastidr[0])
            cursor.execute(csql,val)
            conn.commit()
    # =======================================================================
    # Left To Right Direction
    # =======================================================================
    pos = pygame.mouse.get_pos()
    pygame.draw.line(screen, (0, 153, 0), (newx * 15, newy * 205), (newx * 110, newy * 214), 2)  # line 1
    pygame.draw.line(screen, (0, 153, 0), (newx * 110, newy * 214), (newx * 250, newy * 310), 2)  # line 2
    pygame.draw.line(screen, (0, 153, 0), (newx * 250, newy * 310), (newx * 450, newy * 318), 2)  # line 3
    pygame.draw.line(screen, (0, 153, 0), (newx * 450, newy * 318), (newx * 650, newy * 318), 2)  # line 4
    pygame.draw.line(screen, (0, 153, 0), (newx * 650, newy * 318), (newx * 850, newy * 317), 2)  # line 5
    pygame.draw.line(screen, (0, 153, 0), (newx * 850, newy * 317), (newx * 1270, newy * 318), 2)  # line 6,7
    pygame.draw.line(screen, (0, 153, 0), (newx * 1270, newy * 318), (newx * 1370, newy * 260), 2)  # line 8
    pygame.draw.line(screen, (0, 153, 0), (newx * 1370, newy * 260), (newx * 1470, newy * 200), 2)  # line 9
	#pygame.draw.circle(screen, (128, 128, 128), (newx * 15, newy * 205), 7, 0)  # start station East Bound

    sw2 = pygame.draw.circle(screen, (0, 153, 0), (newx * 110, newy * 214), 6, 0)  # station 2 East Bound
    if is_over(sw2, pos):
        station(118, 222, "Ard El Maared")
    sw3 = pygame.draw.circle(screen, (0, 153, 0), (newx * 250, newy * 310), 6, 0)  # station 3 East Bound
    if is_over(sw3, pos):
        station(258, 318, "Cairo Festival City")
    sw4 = pygame.draw.circle(screen, (0, 153, 0), (newx * 450, newy * 318), 6, 0)  # station 4 East Bound
    if is_over(sw4, pos):
        station(458, 326, "DownTown")
    sw5 = pygame.draw.circle(screen, (0, 153, 0), (newx * 650, newy * 318), 6, 0)  # station 5 East Bound
    if is_over(sw5, pos):
        station(658, 326, "El Ghaz 1")
    sw6 = pygame.draw.circle(screen, (0, 153, 0), (newx * 850, newy * 317), 6, 0)  # station 6 East Bound
    if is_over(sw6, pos):
        station(858, 325, "Mogmaa El Bonok")
    sw7 = pygame.draw.circle(screen, (0, 153, 0), (newx * 1050, newy * 317), 6, 0)  # station 7 East Bound
    if is_over(sw7, pos):
        station(1058, 325, "Mostashfa El Gawy")
    sw8 = pygame.draw.circle(screen, (0, 153, 0), (newx * 1270, newy * 318), 6, 0)  # station 8 East Bound
    if is_over(sw8, pos):
        station(1278, 326, "Ghaz 2")
    sw9 = pygame.draw.circle(screen, (0, 153, 0), (newx * 1370, newy * 260), 6, 0)  # station 9 East Bound
    if is_over(sw9, pos):
        station(1370, 268, "Ghandor Auto")
    # pygame.draw.circle(screen, (128, 128, 128), (newx * 1470, newy * 200), 7, 0)  # end station East

    # emergency route 1 L1(Left to Right)
    pygame.draw.line(screen, linecolor1, (newx * 385, newy * 317), (newx * 400, newy * 280), 2)
    pygame.draw.line(screen, linecolor1, (newx * 400, newy * 280), (newx * 490, newy * 280), 2)
    pygame.draw.line(screen, linecolor1, (newx * 490, newy * 280), (newx * 505, newy * 317), 2)
    # emergency route 2 L1(Left to Right)
    pygame.draw.line(screen, linecolor1, (newx * 785, newy * 316), (newx * 800, newy * 280), 2)
    pygame.draw.line(screen, linecolor1, (newx * 800, newy * 280), (newx * 890, newy * 280), 2)
    pygame.draw.line(screen, linecolor1, (newx * 890, newy * 280), (newx * 905, newy * 316), 2)
    # ==============================================
    # Right To Left Direction
    # ===============================================

    pygame.draw.line(screen, linecolor, (newx * 1473, newy * 220), (newx * 1376, newy * 281), 2)  # line 1
    pygame.draw.line(screen, linecolor, (newx * 1376, newy * 281), (newx * 1275, newy * 338), 2)  # line 2
    pygame.draw.line(screen, linecolor, (newx * 1275, newy * 338), (newx * 1050, newy * 340), 2)  # line 3
    pygame.draw.line(screen, linecolor, (newx * 1050, newy * 340), (newx * 850, newy * 340), 2)  # line 4
    pygame.draw.line(screen, linecolor, (newx * 850, newy * 340), (newx * 650, newy * 340), 2)  # line 5
    pygame.draw.line(screen, linecolor, (newx * 650, newy * 340), (newx * 450, newy * 340), 2)  # line 6
    pygame.draw.line(screen, linecolor, (newx * 450, newy * 340), (newx * 250, newy * 337), 2)  # line 7
    pygame.draw.line(screen, linecolor, (newx * 250, newy * 337), (newx * 110, newy * 238), 2)  # line 8
    pygame.draw.line(screen, linecolor, (newx * 110, newy * 238), (newx * 15, newy * 230), 2)  # line 9
    # pygame.draw.circle(screen, (128, 128, 128), (newx * 1473, newy * 220), 7, 0)  # start station West Bound

    se2 = pygame.draw.circle(screen, linecolor, (newx * 1376, newy * 281), 6, 0)  # station 2 West Bound
    if is_over(se2, pos):
        station(1370, 289, "Ghandor Auto")
    se3 = pygame.draw.circle(screen, linecolor, (newx * 1275, newy * 338), 6, 0)  # station 3 West Bound
    if is_over(se3, pos):
        station(1283, 346, "Ghaz 2")
    se4 = pygame.draw.circle(screen, linecolor, (newx * 1050, newy * 340), 6, 0)  # station 4 East Bound
    if is_over(se4, pos):
        station(1058, 348, "Mostashfa El Gawy")
    se5 = pygame.draw.circle(screen, linecolor, (newx * 850, newy * 340), 6, 0)  # station 5 East Bound
    if is_over(se5, pos):
        station(858, 348, "Mogmaa El Bonok")
    se6 = pygame.draw.circle(screen, linecolor, (newx * 650, newy * 340), 6, 0)  # station 6 East Bound
    if is_over(se6, pos):
        station(658, 348, "El Ghaz 1")
    se7 = pygame.draw.circle(screen, linecolor, (newx * 450, newy * 340), 6, 0)  # station 7 East Bound
    if is_over(se7, pos):
        station(458, 348, "DownTown")
    se8 = pygame.draw.circle(screen, linecolor, (newx * 250, newy * 337), 6, 0)  # station 8 East Bound
    if is_over(se8, pos):
        station(258, 345, "Cairo Festival City")
    se9 = pygame.draw.circle(screen, linecolor, (newx * 110, newy * 238), 6, 0)  # station 9 East Bound
    if is_over(se9, pos):
        station(118, 246, "Ard El Maared")
    # pygame.draw.circle(screen, (128, 128, 128), (newx * 15, newy * 230), 7, 0)  # End Station West

    # ============================================
    # Line Switching
    # ===========================================
    # gets the current mouse coords
    pygame.draw.line(screen, linecolor, (newx * 17, newy * 230), (newx * 103, newy * 214),
                     2)  # line  Switching  In West Terminal
    pygame.draw.line(screen, (0, 153, 0), (newx * 1475, newy * 200), (newx * 1375, newy * 280),
                     2)  # line  Switching In  East Terminal
    sw1 = pygame.draw.rect(screen, (178, 34, 34), pygame.Rect(newx * 5, newy * 190, newx * 12, newy * 60), 0,
                           4)  # start terminal
    if is_over(sw1, pos):
        station(23, 213, "El Moshir Tantawy")
    sw10 = pygame.draw.rect(screen, (178, 34, 34), pygame.Rect(newx * 1470, newy * 186, newx * 12, newy * 55), 0,
                            5)  # END station East Bound
    if is_over(sw10, pos):
        station(1400, 218, "Dusit")

    # emergency route 1 L2(Right to Left)
    pygame.draw.line(screen, linecolor1, (newx * 590, newy * 342), (newx * 605, newy * 378), 2)
    pygame.draw.line(screen, linecolor1, (newx * 605, newy * 378), (newx * 695, newy * 378), 2)
    pygame.draw.line(screen, linecolor1, (newx * 695, newy * 378), (newx * 710, newy * 342), 2)
    # emergency route 2 L2(Right to Left)
    pygame.draw.line(screen, linecolor1, (newx * 990, newy * 342), (newx * 1005, newy * 378), 2)
    pygame.draw.line(screen, linecolor1, (newx * 1005, newy * 378), (newx * 1095, newy * 378), 2)
    pygame.draw.line(screen, linecolor1, (newx * 1095, newy * 378), (newx * 1110, newy * 341), 2)
    # hospital1
    H1 = pygame.draw.circle(screen, (c.XR,0, 0), [newx * 1020, newy * 170], 18, 2)
    pygame.draw.line(screen, (c.XR, 0, 0), (newx * 1010, newy * 170), (newx * 1030, newy * 170), 3)
    pygame.draw.line(screen, (c.XR, 0, 0), (newx * 1020, newy * 160), (newx * 1020, newy * 180), 3)
    if is_over(H1, pos):
        hospitalrep(1028, 178, 1)
    # hospital 2
    H2 = pygame.draw.circle(screen, (c.XR, 0, 0), [newx * 580, newy * 417], 18, 2)
    pygame.draw.line(screen, (c.XR, 0, 0), (newx * 570, newy * 417), (newx * 590, newy * 417), 3)
    pygame.draw.line(screen, (c.XR, 0, 0), (newx * 580, newy * 407), (newx * 580, newy * 427), 3)
    if is_over(H2, pos):
        hospitalrep(588, 418, 2)
    # hospital3
    H3 = pygame.draw.circle(screen, (c.XR, 0, 0), [newx * 350, newy * 60], 18, 2)
    pygame.draw.line(screen, (c.XR, 0, 0), (newx * 340, newy * 60), (newx * 360, newy * 60), 3)
    pygame.draw.line(screen, (c.XR, 0, 0), (newx * 350, newy * 50), (newx * 350, newy * 70), 3)
    if is_over(H3, pos):
        hospitalrep(358, 68, 3)
    #police station1
    POL1 = pygame.draw.circle(screen, (0,0,c.px), [newx * 725.8, newy * 112], 18 )
    policefont = pygame.font.SysFont(None, 35)
    text = policefont.render("P", True, white)
    screen.blit(text, (newx * 718, newy * 102))

    if is_over(POL1, pos):
        policerep(730, 126, 1)
    #police station2
    POL2 = pygame.draw.circle(screen, (0, 0 , c.px), [newx *1120, newy *432], 18)

    policefont = pygame.font.SysFont(None, 35)
    text = policefont.render("P", True, white)
    screen.blit(text, (newx * 1113, newy * 423))
    if is_over(POL2, pos):
        policerep(1128, 420, 2)
    # Police station3
    POL3 = pygame.draw.circle(screen, (0,0,c.px), [newx *450.6, newy *637], 18)
    policefont = pygame.font.SysFont(None, 35)
    text = policefont.render("P", True, white)
    screen.blit(text, (newx * 443.6, newy * 628))
    if is_over(POL3, pos):
        policerep(458, 647, 3)
    # key
    key = pygame.draw.rect(screen, [34, 139, 34], [newx * 1337, newy * 623, 80, 30], 2)
    keyfont = pygame.font.SysFont(None, 25)
    text = keyfont.render("KeyMap", True, (34, 139, 34))
    screen.blit(text, (newx * 1345, newy * 630))
    if is_over(key, pos):
        keyrep(1350, 470)
    # Emergency center 1
    EC1[0].impEC()
    EC1[0].r=c.r
    EC1[0].h=c.h
    if is_over(EC1[0].impEC(), pos): # pass in the pygame.Rect and the mouse coords
            emergencyrep(EC1[0].ex2,EC1[0].ey2,1)
    # Emergency center 2
    EC1[1].impEC()
    EC1[1].r=c.a
    EC1[1].h=c.b
    if is_over(EC1[1].impEC(), pos): # pass in the pygame.Rect and the mouse coords
            emergencyrep(EC1[1].ex2,EC1[1].ey2,2)
    # Emergency center 3
    EC1[2].impEC()
    EC1[2].r=c.c
    EC1[2].h=c.d
    if is_over(EC1[2].impEC(), pos): # pass in the pygame.Rect and the mouse coords
            emergencyrep(EC1[2].ex2,(EC1[2].ey2)-50,3)
    # Emergency center 4
    EC1[3].impEC()
    EC1[3].r=c.e
    EC1[3].h=c.f
    if is_over(EC1[3].impEC(), pos): # pass in the pygame.Rect and the mouse coords
            emergencyrep((EC1[3].ex2),(EC1[3].ey2)-130,4)
    # clock=pygame.time.Clock()
    # clock.tick(30)

    for i in range(len(twest)):
        twest[i].west_implement()
        twest[i].newx=(screen_info.current_w / 1500)
        twest[i].newy=(screen_info.current_h / 700)
        if ((twest[i].x > 1469 and twest[i].x < 1471) or (twest[i].x > 20 and twest[i].x < 22)) and twest[i].history == 0 :
            cursor = conn.cursor()
            csql = "SELECT status FROM trains WHERE ID = %s"
            val = [twest[i].id]
            i=i+1
            cursor.execute(csql, val)
            myresult = cursor.fetchone()
            twest[i-1].trips=twest[i-1].trips+1

            #insert
            now = datetime.now()
            myres1=[myresult[0]]
            now1=[now]
            westid = [twest[i-1].id]
            westtrips = [twest[i-1].trips]
            csql2 = "INSERT IGNORE INTO train_history(TR_ID,TR_Status,Trip_Time,Number_of_Trip) VALUES (%s,%s,%s,%s)"
            val2 = (westid[0],myres1[0],now1[0],westtrips[0])
            cursor.execute(csql2,val2)
            conn.commit()
            twest[i-1].history = 1

        elif ((twest[i].x > 330 and twest[i].x < 340) or (twest[i].x > 1400 and twest[i].x < 1410)) and twest[i].history == 1:
            twest[i-1].history = 0

    for i in range(len(teast)):
        teast[i].east_implement()
        teast[i].newx=(screen_info.current_w / 1500)
        teast[i].newy=(screen_info.current_h / 700)
        if ((teast[i].x > 1465 and teast[i].x < 1467 ) or (teast[i].x > 14 and teast[i].x < 16 )) and teast[i].history == 0 :
            cursor = conn.cursor()
            csql = "SELECT status FROM trains WHERE ID = %s"
            val = [teast[i].id]
            i=i+1
            cursor.execute(csql, val)
            myresult = cursor.fetchone()
            teast[i-1].trips=teast[i-1].trips+1

            #insert
            now = datetime.now()
            myres1=[myresult[0]]
            now1=[now]
            eastid = [teast[i-1].id]
            easttrips = [teast[i-1].trips]
            csql2 = "INSERT IGNORE INTO train_history(TR_ID,TR_Status,Trip_Time,Number_of_Trip) VALUES (%s,%s,%s,%s)"
            val2 = (eastid[0],myres1[0],now1[0],easttrips[0])
            cursor.execute(csql2,val2)
            conn.commit()
            teast[i-1].history = 1

        elif ((teast[i].x > 330 and teast[i].x < 340) or (teast[i].x > 1400 and teast[i].x < 1410)) and teast[i].history == 1:
            teast[i-1].history = 0
    EC1[0].newx=(screen_info.current_w / 1500)
    EC1[1].newx=(screen_info.current_w / 1500)
    EC1[2].newx=(screen_info.current_w / 1500)
    EC1[3].newx=(screen_info.current_w / 1500)

    EC1[0].newy=(screen_info.current_h / 700)
    EC1[1].newy=(screen_info.current_h / 700)
    EC1[2].newy=(screen_info.current_h / 700)
    EC1[3].newy=(screen_info.current_h / 700)
    
    for i in range(len(twest)):  # control movement of west trains
        if (twest[i].x >= 451 or twest[i].flagcx == 1) and i < (len(twest) - 1):
            twest[i + 1].flagmov = 1
        if is_over(twest[i].west_implement(), pos):  # pass in the pygame.Rect and the mouse coords
            screenrep(twest[i].x, twest[i].y, twest[i].id)
        end_time = time.time()
        if twest[i].flagE == 1:
            if realtime.v == "0-A":
                if (((end_time - start_time) < 3) or (twest[i].k == 1)):
                    if (twest[i].x <= 852 and twest[i].x > 30 and twest[i].y < 400 and twest[i].y > 320):
                        if twest[i].k2 != 0:
                            emergencyacc(EC1[3].ex2, EC1[3].ey2)
                    elif (twest[i].x > 950 and twest[i].y < 400 ):
                        if twest[i].k2 != 0:
                            emergencyacc(EC1[2].ex2, EC1[2].ey2)
                    elif (twest[i].x >= 500 and twest[i].x < 950 and twest[i].y < 320):
                        if twest[i].k2 != 0:
                            emergencyacc(EC1[1].ex2, EC1[1].ey2)
                    elif (twest[i].x < 500 and twest[i].y < 320):
                        if twest[i].k2 != 0:
                            emergencyacc(EC1[0].ex2, EC1[0].ey2)

                    s = "z"
                if s == "z" and twest[i].k != 0:
                    start_time = time.time()
                    if twest[i].flagE == 1:
                        twest[i].k = 0
                        
                if (twest[i].flagStop == 1) and ((end_time - start_time) > 3):       
                    twest[i].k2=0
                    
        for m in range(i + 1, len(twest)):
            x_distance = twest[i].x - twest[m].x
            y_distance = twest[i].y - twest[m].y
            distance = math.hypot(x_distance, y_distance)
            if (abs(x_distance) <= 50 and abs(y_distance) <= 5 and twest[m].flagmov == 1 and (twest[m].flag1 == twest[i].flag1 )) :
                if (twest[m].end_time - twest[m].start_time >= 2) and twest[i].endprocess == 0:
                    twest[m].start_time = time.time()
                    twest[m].speed = twest[i].speed
                    sound.play()
                    
            if (distance<= 35):
                twest[m].flagspeed = 0
            elif distance>35:
                twest[m].flagspeed = 1 
          
        for xxx in range(len(twest)-1,-1,-1):
            for zzz in range(len(teast)):
                x_distancem1 = teast[zzz].x - twest[xxx].x
                y_distancem1 = teast[zzz].y - twest[xxx].y
                distancem = math.hypot(x_distancem1, y_distancem1)
                if(abs(x_distancem1)<=50 and abs(y_distancem1)<=5):
                    if(teast[zzz].end_time - teast[zzz].start_time >= 2) and teast[zzz].endprocess == 0:
                        teast[zzz].start_time = time.time()
                        teast[zzz].speed = 0.02
                        twest[xxx].flagspeed= 0
                        sound.play()


    for i in range(len(teast)):  # control movement of east trains
        if (teast[i].x <= 1050 or teast[i].flagcx == 1) and i < (len(teast) - 1):
            teast[i + 1].flagmov = 1
        if is_over(teast[i].east_implement(), pos):  # pass in the pygame.Rect and the mouse coords
            screenrep(teast[i].x-60, teast[i].y, teast[i].id)

        end_time = time.time()
        if teast[i].flagE == 1:
            if realtime.v == "0-A":
                if (((end_time - start_time) < 3) or (teast[i].k == 1)):
                    if (teast[i].x <= 852 and teast[i].x > 30 and teast[i].y < 400 and teast[i].y > 320):
                        if teast[i].k2 != 0:
                            emergencyacc(EC1[3].ex2, EC1[3].ey2)
                    if (teast[i].x > 950 and teast[i].y < 400 ):
                        if teast[i].k2 != 0:
                            emergencyacc(EC1[2].ex2, EC1[2].ey2)
                    if (teast[i].x >= 500 and teast[i].x < 950 and teast[i].y < 320):
                        if teast[i].k2 != 0:
                            emergencyacc(EC1[1].ex2, EC1[1].ey2)
                    if (teast[i].x < 500 and teast[i].y < 320):
                        if teast[i].k2 != 0:
                            emergencyacc(EC1[0].ex2, EC1[0].ey2)

                    s = "z"
                if s == "z" and teast[i].k != 0:
                    start_time = time.time()
                    if teast[i].flagE == 1:
                        teast[i].k = 0
                if (teast[i].flagStop == 1) and ((end_time - start_time) > 3):       
                    teast[i].k2=0

        for m in range(i + 1, len(teast)):
            x_distance = teast[m].x - teast[i].x
            y_distance = teast[m].y - teast[i].y
            distance = math.hypot(x_distance, y_distance)
            if(abs(x_distance)<=50 and abs(y_distance)<=5 and teast[m].flagmov == 1 and (teast[m].flag1 == teast[i].flag1 )) and teast[i].endprocess == 0:
                if(teast[m].end_time - teast[m].start_time >= 2):
                    teast[m].start_time = time.time()
                    teast[m].speed = teast[i].speed
                    sound.play()
                    print(i,m,x_distance,y_distance)
            if (distance<= 35):
                teast[m].flagspeed = 0
            elif distance>35:
                teast[m].flagspeed = 1

        for xxx in range(len(teast)-1,-1,-1):
            for zzz in range(len(twest)):
                x_distancem = teast[xxx].x - twest[zzz].x
                y_distancem = teast[xxx].y - twest[zzz].y
                distancem = math.hypot(x_distancem, y_distancem)
                if(abs(x_distancem)<=50 and abs(y_distancem)<=5):
                    if(twest[zzz].end_time - twest[zzz].start_time >= 2) and twest[zzz].endprocess == 0:
                            twest[zzz].start_time = time.time()
                            twest[zzz].speed = 0.02
                            sound.play()                    


    c.route()

    value = ui.horizontalSlider.value()
    changespeedValue(value)
pygame.display.update()

conn.close()