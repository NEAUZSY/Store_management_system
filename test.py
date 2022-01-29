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


class Store(object):
    def __init__(self, info_):
        self.selected = ''
        self.win = tkinter.Tk()  # 窗口
        self.win.title('库存查询')  # 标题
        screenwidth = self.win.winfo_screenwidth()  # 屏幕宽度
        screenheight = self.win.winfo_screenheight()  # 屏幕高度
        width = 640
        height = 480
        x = int((screenwidth - width) / 2)
        y = int((screenheight - height) / 2)
        self.win.geometry('{}x{}+{}+{}'.format(width, height, x, y))  # 大小以及位置

        tabel_frame = tkinter.Frame(self.win)
        tabel_frame.pack()

        xscroll = Scrollbar(tabel_frame, orient=HORIZONTAL)
        yscroll = Scrollbar(tabel_frame, orient=VERTICAL)

        columns = ['采购单号', '采购单位', '采购日期', '规格', '型号', '数量']
        table = ttk.Treeview(
            master=tabel_frame,  # 父容器
            height=15,  # 表格显示的行数,height行
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
            table.column(column=column, width=100, minwidth=100, anchor=CENTER, )  # 定义列
        xscroll.config(command=table.xview)
        xscroll.pack(side=BOTTOM, fill=X)
        yscroll.config(command=table.yview)
        yscroll.pack(side=RIGHT, fill=Y)

        for index, data in enumerate(info_):
            table.insert('', END, values=data)  # 添加数据到末尾

        table.bind('<<TreeviewSelect>>', self.selectTree)
        table.pack(fill=BOTH, expand=True)
        self.table = table

        btn_sell = Button(self.win, text="出库", command=self.Sell)
        btn_sell.place(x=50, y=400)

        self.win.mainloop()

    def Sell(self):
        a = messagebox.askokcancel('出库确认', '您是否要要将编号为 %s 的商品出库出库？' % self.selected)  # 弹出对话框
        if a:
            print(self.selected)

    def selectTree(self, event):
        item_list = []
        for item in self.table.selection():
            item_id = self.table.item(item, "values")[0]
            # print(item_text)
            item_list.append(item_id)
        selected = ', '.join(item_list)
        # print(selected)
        self.selected = selected


def display(info_):
    quare = Store(info_)


if __name__ == '__main__':
    display(info)
