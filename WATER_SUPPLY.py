import sys
from tkinter import messagebox

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

import MAIN
import alert
import bye


def get_rules():
    # 获取规则库 并将结论和前提分开存储
    RD = open("RD.txt", 'r')
    P = []
    Q = []
    for line in RD:
        line = line.strip('\n')  # 删除开头或是结尾的回车字符
        if line == '':  # 处理空行 跳过
            continue
        line = line.split(' ')  # 切片
        Q.append(line[line.__len__() - 1])  # 分开存储，Q存放每条推理结论
        del (line[line.__len__() - 1])
        P.append(line)  # P存放每条推理条件
    RD.close()  # 关闭文件
    return P, Q


# 判断list中所有元素是否都在集合set中
def ListInSet(li, se):
    for i in li:
        if i not in se:
            return False
    return True


# 设置退出页面
class bye_ui(QtWidgets.QMainWindow, bye.Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)  # 创建主界面对象
        bye.Ui_MainWindow.__init__(self)  # 主界面对象初始化
        self.setupUi(self)  # 配置主界面对象


# 设置提示界面
class alert_ui(QtWidgets.QMainWindow, alert.Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)  # 创建主界面对象
        alert.Ui_MainWindow.__init__(self)  # 主界面对象初始化
        self.setupUi(self)  # 配置主界面对象


# 设置主界面
class MAIN_ui(QtWidgets.QMainWindow, MAIN.Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)  # 创建主界面对象
        MAIN.Ui_MainWindow.__init__(self)  # 主界面对象初始化
        self.setupUi(self)  # 配置主界面对象
        self.pushButton.clicked.connect(self.add_rule)  # 添加规则
        self.pushButton_3.clicked.connect(self.del_rule)  # 添加规则
        self.pushButton_4.clicked.connect(self.find_rule)  # 查询规则
        self.pushButton_2.clicked.connect(self.inference)
        self.alert_window = alert_ui()
        for line in open('RD.txt'):  # 将规则库放入显示框
            self.textBrowser.append(line)

    def add_rule(self):
        # 添加新规则
        new_rule = self.lineEdit.text()
        if new_rule != " ":
            self.textBrowser.append(new_rule)
            RD = open('RD.txt', 'a')
            RD.write(new_rule)
            RD.write('\n')

    def del_rule(self):
        # 删除规则
        new_rule = self.lineEdit.text()
        if new_rule != " ":
            lines = [l for l in open("RD.txt", "r") if l.find(new_rule) != 0]
            fd = open("RD.txt", "w")
            fd.writelines(lines)
            fd.close()
        self.textBrowser.clear()
        for line in open('RD.txt'):  # 将规则库放入显示框
            self.textBrowser.append(line)

    def find_rule(self):
        # 查询规则
        new_rule = self.lineEdit.text()
        if new_rule != " ":
            for line in open('RD.txt'):
                a = line.find(new_rule)
        if a == -1:
            msg_box = QMessageBox(QMessageBox.Question, 'Results', 'Not found')
        else:
            msg_box = QMessageBox(QMessageBox.Question, 'Results', 'Found it')
        msg_box.exec_()  # 执行弹出框

    def no(self):
        self.bye_window = bye_ui()
        self.bye_window.show()
        self.alert_window.close()
        self.close()

    def inference(self):
        # 推理
        input = self.textEdit.toPlainText()  # 获取输入的事实
        input = input.split('\n')
        DB = set(input)  # 将综合数据库以集合的形式存放
        [P, Q] = get_rules()  # 获取规则库
        self.process = ''  # 用于存储推理过程
        self.animal = ''  # 存储结论
        DB_list = []
        strr = []
        for p in input:
            DB_list.append(p)
            strr.append(p)
        # 下面开始正式推理
        flag = 0

        n = 3  # 遍历两遍
        while n != 0:
            for premise in P:  # 对前提条件进行遍历
                if ListInSet(premise, DB) and Q[P.index(premise)] not in DB:
                    # 能够找到一个前提条件全部存在于数据库
                    DB.add(Q[P.index(premise)])  # 把结论放入综合数据库
                    self.animal = Q[P.index(premise)]  # 更新结论
                    self.process += "%s --> %s\n" % (premise, Q[P.index(premise)])
                    flag = 1  # 至少有一个能够推出来的结论

                    DB_list.append(Q[P.index(premise)])  # 用于数据库的显示
                    for i in DB_list:
                        self.textEdit_3.insertPlainText(i)
                        self.textEdit_3.insertPlainText(" ")
                    self.textEdit_3.insertPlainText("\n")
                    # print(DB_list)
                    # print(Q[P.index(premise)])
            n -= 1

        if flag == 0:
            # 一个结论也推不出来，询问用户是否进行补充
            self.alert_window.show()
            self.alert_window.pushButton.clicked.connect(self.alert_window.close)
            self.alert_window.pushButton_2.clicked.connect(self.no)
        else:  # flag!=0说明有结论生成
            # 显示出推理过程
            self.textEdit_2.setText(self.process)
            # 显示出结论
            self.lineEdit_2.setText(self.animal)
            strrr = "If "+ " ".join(map(str, strr))
            strrr += " Then: " + self.animal
            self.textEdit_4.setText(strrr)


app = QtWidgets.QApplication(sys.argv)  # 新建窗体
MAIN_window = MAIN_ui()  # 创建主菜单的窗口对象
MAIN_window.show()  # 显示主菜单
sys.exit(app.exec_())  # 保持显示
