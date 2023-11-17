import io
import sys
import time

from PyQt5 import QtCore
from PyQt5.QtCore import QProcess
from PyQt5 import uic
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtWidgets import QMainWindow
from time import sleep

ui = '''<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>800</width>
    <height>600</height>
   </rect>
  </property>
  <property name="minimumSize">
   <size>
    <width>640</width>
    <height>480</height>
   </size>
  </property>
  <property name="maximumSize">
   <size>
    <width>1920</width>
    <height>1080</height>
   </size>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <layout class="QGridLayout" name="gridLayout">
    <item row="2" column="6">
     <widget class="QPushButton" name="send_2">
      <property name="text">
       <string>^</string>
      </property>
     </widget>
    </item>
    <item row="3" column="0" colspan="4">
     <widget class="QTextEdit" name="textEdit"/>
    </item>
    <item row="0" column="1">
     <widget class="QPushButton" name="uslovie">
      <property name="text">
       <string>Условие</string>
      </property>
     </widget>
    </item>
    <item row="3" column="4" colspan="3">
     <widget class="QTextBrowser" name="console"/>
    </item>
    <item row="2" column="3">
     <spacer name="horizontalSpacer_2">
      <property name="orientation">
       <enum>Qt::Horizontal</enum>
      </property>
      <property name="sizeHint" stdset="0">
       <size>
        <width>385</width>
        <height>28</height>
       </size>
      </property>
     </spacer>
    </item>
    <item row="0" column="0">
     <widget class="QPushButton" name="pushButton">
      <property name="text">
       <string>&lt;</string>
      </property>
     </widget>
    </item>
    <item row="1" column="0" rowspan="2" colspan="4">
     <widget class="QLabel" name="label">
      <property name="text">
       <string>Не решено</string>
      </property>
     </widget>
    </item>
    <item row="0" column="2" colspan="5">
     <spacer name="horizontalSpacer">
      <property name="orientation">
       <enum>Qt::Horizontal</enum>
      </property>
      <property name="sizeHint" stdset="0">
       <size>
        <width>617</width>
        <height>38</height>
       </size>
      </property>
     </spacer>
    </item>
    <item row="2" column="5">
     <widget class="QPushButton" name="sendButton">
      <property name="text">
       <string>Отправить решение</string>
      </property>
     </widget>
    </item>
   </layout>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>800</width>
     <height>21</height>
    </rect>
   </property>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>
'''


class Lms(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(io.StringIO(ui), self)
        self.setWindowTitle('Lms-absolute?')
        self.sleep = False
        self.sendButton.clicked.connect(self.code_send)
        self.send_2.clicked.connect(self.code_send)
        self.timer = QtCore.QTime()
        self.uslovie.clicked.connect(self.usl)
        self.yes = False

    def usl(self):
        check = '''
условие задачи
'''
        QMessageBox.information(self, 'Uslovie', check)

    def code_send(self):
        if self.yes:
            qm = QMessageBox()
            ret = qm.question(self, 'answer already na meste', 'у вас уже есть ответ на это задание.'
                                                               'точно отправить новое решение?', qm.Yes | qm.No)
            if ret == qm.Yes:
                with open('testing_code.py', 'w') as clear_file:
                    pass
                with open('testing_code.py', 'w') as r_code:
                    if self.textEdit.toPlainText():
                        r_code.write(self.textEdit.toPlainText())
                        self.checking_pep()
                    else:
                        QMessageBox().information(self, 'no code written', 'Напиши код а то проверять нечего')
            else:
                pass
        else:
            with open('testing_code.py', 'w') as clear_file:
                pass
            with open('testing_code.py', 'w') as r_code:
                if self.textEdit.toPlainText():
                    r_code.write(self.textEdit.toPlainText())
                    self.checking_pep()
                else:
                    QMessageBox().information(self, 'no code written', 'Напиши код а то проверять нечего')

    # checking code for pep8 warnings
    def checking_pep(self):
        self.console.clear()
        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.pep_stdout)
        self.process.finished.connect(self.finished_pep)
        self.process.start("pycodestyle testing_code.py")

    def finished_pep(self):
        with open('pep8_errors.txt', 'r') as errors:
            f = errors.read()
            if f:
                self.console.append(f"Код не соответствует пяти столпам ислама.\n"
                                    f"Все подробности в файле pep8_error.txt")
                self.yes = False
                self.ocenka()
                print('f: ' + f)
            else:
                self.console.append('Проверка на пеп восьмой пройдена')
                sleep(1)
                self.run()

    def pep_stdout(self):
        data = self.process.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        open('pep8_errors.txt', 'w').close()

        with open('pep8_errors.txt', 'w') as out:
            if stdout:
                print('pep: ' + stdout)
                if 'end of file' in stdout and len(stdout.split(' ')) == 8:
                    print('по пепу только новая строка и кек')
                else:
                    out.write(stdout)
            else:
                print('no pep')

    # running code and get result
    def handle_stderr(self):
        data = self.process.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        self.console.append(stderr)

    def handle_stdout(self):
        data = self.process.readAllStandardOutput()
        print(data)
        stdout = bytes(data).decode("utf8")
        self.console.append(stdout)
        print(stdout.split('\n'))
        need = ['5\r', '4\r', '3\r', '2\r', '1\r', '0\r', 'pusk\r', '']
        if stdout.split('\n') == need:
            self.yes = True

    def run(self):
        fname = 'testing_code.py'
        self.console.show()
        self.console.clear()

        self.console.append(f"[Running your code]\n")
        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)
        self.process.started.connect(self.timer.start)
        self.process.finished.connect(self.finished_code)
        try:
            self.process.start("python", [f"{fname}"])
        except Exception as e:
            QMessageBox().information(self, 'Error', f"{e}")

    def stop_code(self):
        try:
            self.process.kill()
        except Exception as e:
            QMessageBox().information(self, 'Error', f"{e}")

    def finished_code(self):
        process_time = self.timer.elapsed()
        self.console.append(f"[Finished in {process_time / 1000}s]")
        self.process = None
        self.ocenka()

    def ocenka(self):
        if self.yes:
            self.label.setStyleSheet('background-color: #00FF00')
            self.label.setFont(QFont('Arial', 14))
            self.label.setText('                                        Зачтено 2384623864/2384623864 баллов')
        else:
            self.label.setStyleSheet('background-color: #FF0000')
            self.label.setFont(QFont('Arial', 14))
            self.label.setText('                                        На доработку')


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Lms()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
