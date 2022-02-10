# 该文件用于批量导入本地数据
from tkinter import filedialog
import tkinter as tk
from openpyxl import Workbook, load_workbook
from openpyxl.styles import *
from SQL import MyDb


class Import_Datas(object):
    def __init__(self):

        self.db = MyDb()

        self.root = tk.Tk()  # 创建文件选择窗口
        screenwidth = self.root.winfo_screenwidth()  # 屏幕宽度
        screenheight = self.root.winfo_screenheight()  # 屏幕高度
        width = 350
        height = 150
        x = int((screenwidth - width) / 2)
        y = int((screenheight - height) / 2)
        self.root.geometry('{}x{}+{}+{}'.format(width, height, x, y))  # 大小以及位置
        self.root.title('选择要导入的文件')
        label = tk.Label(self.root, text='文件路径：')
        label.place(x=10, y=10)
        self.path = tk.StringVar(value=r'C:\Users\NEAUZSY\Desktop\大类_唐山迈拓科技有限公司.xlsx')  # 创建文件路径变量

        enter = tk.Entry(self.root, width=30, textvariable=self.path)  # 创建显示文件路径的输入框
        enter.place(x=80, y=15)

        # 创建选择文件路径的按钮
        btn_select = tk.Button(self.root, text='...', width=3, height=1, command=self.Button_command)
        btn_select.place(x=310, y=10)

        btn_confirm = tk.Button(self.root, text='返回', width=4, height=1, command=self.Click_back)
        btn_confirm.place(x=100, y=90)

        btn_back = tk.Button(self.root, text='确认', width=4, height=1, command=self.Click_confirm)
        btn_back.place(x=200, y=90)

        self.is_return = False

        self.root.mainloop()
        if self.is_return:
            self.WorkBook_Init()
            self.Import_Data()

    def Button_command(self):
        # 获取文件路径
        Filepath = filedialog.askopenfilename()  # 获得选择好的文件
        self.path.set(Filepath)

    def Click_back(self):
        self.root.destroy()
        self.is_return = False

    def Click_confirm(self):
        self.root.destroy()
        # 获取到路径的值
        self.path = self.path.get()
        self.is_return = True

    # noinspection PyAttributeOutsideInit
    def WorkBook_Init(self):
        try:
            self.wb = load_workbook(self.path)
            self.ws = self.wb['商品购入模板（期初）']
            print('初始化工作表完成 开始导入数据---->')
        except Exception as e:
            print(e)

    def Import_Data(self):
        for i, row in enumerate(self.ws.values):
            if i >= 1:
                # print(row)
                # 格式化数据称为能直接放到SQL语句中的字符串
                data_list = [str(i) for i in list(row)]
                data_buy = '"' + '", "'.join([i for i in data_list]) + '"'
                task_buy = 'insert into tb_buy values(%s);' % data_buy
                result = self.db.execute(task_buy)
                store_list = data_list[0:9]
                if data_list[-1] == "1":
                    # 含税 库存中单价和金额存储为含税项
                    store_list.extend([data_list[9], data_list[11]])
                else:
                    store_list.extend([data_list[10], data_list[12]])
                store_list.extend(data_list[13:15])
                data_store = '"' + '", "'.join([i for i in store_list]) + '"'
                task_store = 'insert into tb_store values(%s);' % data_store

                result = self.db.execute(task_store)
                print('已经完成了 %d 行数据的导入' % i)




def main():
    myimport = Import_Datas()


if __name__ == '__main__':
    main()
