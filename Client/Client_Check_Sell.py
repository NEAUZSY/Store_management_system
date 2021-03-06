# -*- encoding=utf-8 -*-
import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

info = [
    ['1001', '李华', '男', '2014-01-25', '广东', '计算5班', ],
    ['1002', '小米', '男', '2015-11-08', '深圳', '计算5班', ],
    ['1003', '刘亮', '男', '2015-09-12', '福建', '计算5班', ],
    ['1004', '白鸽', '女', '2016-04-01', '湖南', '计算5班', ]]


class Sell(object):
    def __init__(self, info_):
        self.is_check = True
        self.win = tkinter.Tk()  # 窗口
        self.win.title('出库信息查询查询')  # 标题
        screenwidth = self.win.winfo_screenwidth()  # 屏幕宽度
        screenheight = self.win.winfo_screenheight()  # 屏幕高度
        width = 1400
        height = 600
        x = int((screenwidth - width) / 2)
        y = int((screenheight - height) / 2)
        self.win.geometry('{}x{}+{}+{}'.format(width, height, x, y))  # 大小以及位置

        tabel_frame = tkinter.Frame(self.win)
        tabel_frame.pack()

        xscroll = Scrollbar(tabel_frame, orient=HORIZONTAL)
        yscroll = Scrollbar(tabel_frame, orient=VERTICAL)

        columns = ['序号', '入库时间', '往来单位', '一级分类',
                   '二级分类', '商品名称', '规格型号', '单位',
                   '数量', '单价（含税）', '单价（未税）', '金额（含税）',
                   '金额（未税）', '备注/序列号', '生成出库单次数']
        table = ttk.Treeview(
            master=tabel_frame,  # 父容器
            height=25,  # 表格显示的行数,height行
            columns=columns,  # 显示的列
            show='headings',  # 隐藏首列
            selectmode="extended",  # 选择模式为可多选
            xscrollcommand=xscroll.set,  # x轴滚动条
            yscrollcommand=yscroll.set,  # y轴滚动条
        )
        for column in columns:
            table.heading(column=column, text=column, anchor=CENTER,
                          command=lambda name=column:
                          messagebox.showinfo('', '{}描述信息~~~'.format(name)))  # 定义表头
            table.column(column=column, width=110, minwidth=110, anchor=CENTER, )  # 定义列
        xscroll.config(command=table.xview)
        xscroll.pack(side=BOTTOM, fill=X)
        yscroll.config(command=table.yview)
        yscroll.pack(side=RIGHT, fill=Y)
        print(info_)
        for index, data in enumerate(info_):
            table.insert('', END, values=tuple(list(data[:-2]) + [data[-1]]))  # 添加数据到末尾

        table.pack(fill=BOTH, expand=True)
        self.table = table
        btn_back = Button(self.win, text="返回", command=self.Back)
        btn_back.place(x=150, y=height-50)

        self.win.mainloop()

    def Back(self):
        self.is_check = False
        self.win.destroy()


def display(info_):
    quare = Sell(info_)


if __name__ == '__main__':
    display(info)
