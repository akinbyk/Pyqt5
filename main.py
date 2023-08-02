import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt,QTimer
from time import sleep
import threading
from loginekran import *
from PyQt5.QtWidgets import QMessageBox
from anamenu import *
import timeit
import requests
import hashlib
import sqlite3 as sql

from PyQt5.QtCore import pyqtSignal, QObject

class VeritabaniSinyali(QObject):
    veritabani_degisiklik = pyqtSignal()

uygulama=QApplication(sys.argv)
pencere=QMainWindow()
pencere1=QMainWindow()
ui1=Ui_MainWindow1()
ui=LoginEkran()

def loginmain():
    
    ui.setupUi(pencere)
    pencere.setWindowFlag(Qt.FramelessWindowHint)
    pencere.show()
    vt=sql.connect('keskinlab.db')
    imlec=vt.cursor()

    def barcodeGiris():
        barcode = ui.lineEdit.text()
        company = barcode[:2]
        user_id = barcode[3:5]
        password = barcode[6:]
        vt=sql.connect('keskinlab.db')
        imlec=vt.cursor()
        hashed_password = hashlib.md5(str(password).encode()).hexdigest()     
        komut= "SELECT * FROM users WHERE company = ? AND id = ? AND password = ?"
        imlec.execute(komut,(company,user_id,hashed_password))
        user = imlec.fetchone()
        if user:
            ui1.setupUi(pencere)
            pencere.setWindowFlag(Qt.FramelessWindowHint)
            vt.close()
            main()
        else:
            ui.lineEdit.clear()
            vt.close()
  
    def girisKontrol1():
        username=ui.usernameText.text()
        password=ui.passwordText.text()
        
        vt=sql.connect('keskinlab.db')
        imlec=vt.cursor()
        hashed_password = hashlib.md5(str(password).encode()).hexdigest()
        
        komut= "SELECT * FROM users WHERE password = ? AND username= ?"
        imlec.execute(komut,(hashed_password,username))
        user = imlec.fetchone()
        if user:
            ui1.setupUi(pencere)
            pencere.setWindowFlag(Qt.FramelessWindowHint)
            vt.close()
            main()
        else:
            QMessageBox.warning(None, "Hatalı Giriş", "Kullanıcı adı veya şifre hatalı!", QMessageBox.Ok)
            ui.usernameText.clear()
            ui.passwordText.clear()
            vt.close()
        

    def cikisyap():
            loginmain()
            pencere1.hide()
            
            
    def cikis():
            sys.exit()   
            
            
    def main():
      
        def listele():
                
            ui1.listWidget.clear()
            komut="select No from keskinlab where status=0 and cam=1"
                
            for row in imlec.execute(komut):
                ui1.listWidget.addItems(row)


        def veritabani_kontrol():
            listele()  
            
        def labelGetir():
            ui1.selectedLabel.setText(ui1.listWidget.currentItem().text())
                

        def okeyButton():
            try:
                kosul=ui1.selectedLabel.text()
                imlec.execute("Update keskinlab set status=1 where No=?",[kosul])
                vt.commit()
                listele()
                ui1.selectedLabel.setText(ui1.listWidget.item(0).text())
                listesorgula()    
                vt.commit()

            except Exception as error:
                print(error)
                        
        def listesorgula():
            if ui1.listWidget.count() > 0:
                ui1.selectedLabel.setText(ui1.listWidget.item(0).text())
            else:
                ui1.selectedLabel.setText("Liste boş.")

        def notokeyButton():
            try:
                kosul=ui1.selectedLabel.text()
                imlec.execute("Update keskinlab set status=2 where No=?",[kosul])
                listele()
                vt.commit()
                listesorgula()
            except Exception as error:
                print(error)

        timer = QTimer()
        timer.timeout.connect(veritabani_kontrol)
        timer.start(2000) 

        
        listele()
        listesorgula()
        ui1.listWidget.clicked.connect(labelGetir)
        ui1.okButton.clicked.connect(okeyButton)
        ui1.notButton.clicked.connect(notokeyButton)
        ui1.logoutButton.clicked.connect(cikisyap)
        
     
    ui.lineEdit.setFocus()
    ui.lineEdit.returnPressed.connect(barcodeGiris)
    ui.girisButton.clicked.connect(girisKontrol1)
    ui.cikisButton.clicked.connect(cikis)

loginmain()

sys.exit(uygulama.exec_())