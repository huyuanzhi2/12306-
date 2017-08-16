import sys
from PyQt5 import QtCore, QtGui, QtWidgets 
from gui import *
from query import *

class MyWindow(QtWidgets.QMainWindow,Ui_Form):  
    def __init__(self):  
        super(MyWindow,self).__init__()  
        self.setupUi(self)  
        self.pushButton.clicked.connect(self.Search)
    def Search(self):
        search_time = self.dateEdit.dateTime().toString().split(' ')
        year = search_time[4]
        month = '%02d' % int(search_time[1][0])
        day = '%02d' % int(search_time[2])
        _time = year+'-'+month+'-'+day
        _from_station_name = str(self.lineEdit.text())
        _to_station_name = str(self.lineEdit_2.text())
        msg_content = [_time,_from_station_name,_to_station_name]
        self.plainTextEdit.setPlainText('')
        #print(msg_content)
        infos = query_train_info(get_query_url(msg_content))
        if infos != 'error':
            for info in infos:
                self.plainTextEdit.appendPlainText(info)
                self.plainTextEdit.appendPlainText('='*90)
        else:
            self.plainTextEdit.setPlainText('Error!!!')
 
if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)  
    myshow = MyWindow()  
    myshow.show()
    sys.exit(app.exec_())