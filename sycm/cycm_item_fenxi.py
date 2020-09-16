import sys
import cycm_item_ui
 
#这里我们提供必要的引用。基本控件位于pyqt5.qtwidgets模块中。
from PyQt5.QtWidgets import QApplication, QMainWindow
 
 
if __name__ == '__main__':
    #每一pyqt5应用程序必须创建一个应用程序对象。sys.argv参数是一个列表，从命令行输入参数。
    app = QApplication(sys.argv)
    #创建一个主窗口
    mainWindow = QMainWindow()
    #调用生成的ui文件
    ui = cycm_item_ui.Ui_MainWindow()
    #设置ui
    ui.setupUi(mainWindow)
    #显示窗口、
    mainWindow.setWindowTitle('生意参谋-单品分析')
    mainWindow.show()
    #消息循环
    sys.exit(app.exec_())