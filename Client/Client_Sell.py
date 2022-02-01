# -*- encoding=utf-8 -*-
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime

info = [
    ['1001', '李华', '男', '2014-01-25', '广东', '计算5班', ],
    ['1002', '小米', '男', '2015-11-08', '深圳', '计算5班', ],
    ['1003', '刘亮', '男', '2015-09-12', '福建', '计算5班', ],
    ['1004', '白鸽', '女', '2016-04-01', '湖南', '计算5班', ]]


class Sell(object):
    def __init__(self, info_):

        self.public_info = tk.Tk()  # 创建获取往来单位和日期信息的窗口
        tt = datetime.now().strftime('%Y-%m-%d')
        yy = tt[0:4]
        mm = tt[5:7]
        dd = tt[8:10]
        self.var_yy = tk.StringVar(value=yy)
        self.var_mm = tk.StringVar(value=mm)
        self.var_dd = tk.StringVar(value=dd)
        self.target = tk.StringVar(value='')

        self.quantity = tk.StringVar(value=100)  # 出库商品数量
        self.value = tk.StringVar(value=100)  # 出库商品单价

        self.sell = True
        self.is_selected = True
        self.public_info_get()

        if self.sell:
            # 完成了基本信息的录入
            self.info_ = info_
            self.win = tk.Tk()  # 窗口
            self.is_quare = True
            self.selected = ''
            self.item_list = ''
            self.root_init()

            if self.selected:
                self.info_list = []  # 在第三集窗口中储存信息的列表
                self.value_info = tk.Tk()  # 创建获取往来单位和日期信息的窗口
                self.value_info_get()

    def root_init(self):
        self.win.title('库存查询')  # 标题
        screenwidth = self.win.winfo_screenwidth()  # 屏幕宽度
        screenheight = self.win.winfo_screenheight()  # 屏幕高度
        width = 640
        height = 480
        x = int((screenwidth - width) / 2)
        y = int((screenheight - height) / 2)
        self.win.geometry('{}x{}+{}+{}'.format(width, height, x, y))  # 大小以及位置

        tabel_frame = tk.Frame(self.win)
        tabel_frame.pack()

        xscroll = Scrollbar(tabel_frame, orient=HORIZONTAL)
        yscroll = Scrollbar(tabel_frame, orient=VERTICAL)

        columns = ['序号', '入库时间', '往来单位', '一级分类',
                   '二级分类', '商品名称', '规格型号', '单位',
                   '数量', '单价', '金额', '备注/序列号']
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

        for index, data in enumerate(self.info_):
            table.insert('', END, values=data)  # 添加数据到末尾

        table.bind('<<TreeviewSelect>>', self.selectTree)
        table.pack(fill=BOTH, expand=True)
        self.table = table

        btn_sell = Button(self.win, text="下一步", command=self.Sell)
        btn_sell.place(x=50, y=400)

        btn_back = Button(self.win, text="退出", command=self.Back)
        btn_back.place(x=150, y=400)

        self.win.mainloop()

    def public_info_get(self):
        # 获取往来单位和出库日期
        self.public_info.title('公共信息录入')
        screenwidth = self.public_info.winfo_screenwidth()  # 屏幕宽度
        screenheight = self.public_info.winfo_screenheight()  # 屏幕高度
        width = 300
        height = 180
        x = int((screenwidth - width) / 2)
        y = int((screenheight - height) / 2)
        self.public_info.geometry('{}x{}+{}+{}'.format(width, height, x, y))  # 大小以及位置

        self.public_info.configure(bg='#DDEBF7')
        title = tk.Label(self.public_info,
                         bg='#DDEBF7',
                         font=('Arial', 16),
                         text='商品出库')
        title.place(x=110, y=20)

        lb_yy = tk.Label(self.public_info,
                         bg='#DDEBF7',
                         font=('Arial', 12),
                         text='年')
        lb_yy.place(x=150, y=60)

        lb_mm = tk.Label(self.public_info,
                         bg='#DDEBF7',
                         font=('Arial', 12),
                         text='月')
        lb_mm.place(x=195, y=60)

        lb_dd = tk.Label(self.public_info,
                         bg='#DDEBF7',
                         font=('Arial', 12),
                         text='日')
        lb_dd.place(x=240, y=60)

        En_yy = tk.Entry(self.public_info, textvariable=self.var_yy, bd=2, justify='center', width=6, bg='#DDEBF7',
                         relief="flat")
        En_yy.place(x=105, y=60)
        En_mm = tk.Entry(self.public_info, textvariable=self.var_mm, bd=2, justify='center', width=3, bg='#DDEBF7',
                         relief="flat")
        En_mm.place(x=170, y=60)
        En_dd = tk.Entry(self.public_info, textvariable=self.var_dd, bd=2, justify='center', width=3, bg='#DDEBF7',
                         relief="flat")
        En_dd.place(x=215, y=60)

        lb1 = tk.Label(self.public_info,
                       bg='#DDEBF7',
                       font=('Arial', 12),
                       text='往来单位:')
        lb1.place(x=15, y=90)

        En1 = tk.Entry(self.public_info, textvariable=self.target, bd=2)
        En1.place(x=110, y=90)

        btn_finsh = tk.Button(self.public_info, text="确认", command=self.check_input)
        btn_finsh.place(x=100, y=130)

        btn_back = tk.Button(self.public_info, text="返回", command=self.info_back)
        btn_back.place(x=200, y=130)

        self.public_info.mainloop()

    def check_input(self):
        self.public_info.destroy()

    def info_back(self):
        self.public_info.destroy()
        self.sell = False

    def value_info_get(self):

        def plot_tree(lists):
            i = 0
            for i, data in enumerate(lists):
                tree.insert('', i, values=(data[0], data[1], data[2]))
                i += 1
            tree.pack(expand=True, fill=BOTH)

        screenwidth = self.value_info.winfo_screenwidth()  # 屏幕宽度
        screenheight = self.value_info.winfo_screenheight()  # 屏幕高度
        width = 600
        height = 130 + len(self.item_list) * 50
        print(height)
        x = int((screenwidth - width) / 2)
        y = int((screenheight - height) / 2)
        self.value_info.geometry('{}x{}+{}+{}'.format(width, height, x, y))  # 大小以及位置

        columns = ("name", "quantity", "value")
        tree = ttk.Treeview(self.value_info, show="headings", columns=columns, selectmode=BROWSE)
        tree.column("name", anchor=CENTER)
        tree.column("quantity", anchor=CENTER)
        tree.column("value", anchor=CENTER)

        # # 设置表格文字居中
        # tree.column("name")
        # tree.column("gender")
        # tree.column("age")

        # 设置表格头部标题
        tree.heading("name", text="商品名称")
        tree.heading("quantity", text="数量")
        tree.heading("value", text="金额")

        select_lists = []
        for rows in self.info_:
            if rows[0] in self.item_list:
                select_lists.append(rows[4])

        self.info_list = [[i, 0, 0] for i in select_lists]

        # print(select_lists)
        plot_tree(self.info_list)
        tree.bind('<ButtonRelease-1>', self.treeviewClick)
        self.tree = tree
        self.value_info.mainloop()

    def treeviewClick(self, event):  # 单击
        # for item in self.tree.selection():
        #     item_text = self.tree.item(item, "values")
        #     print(item_text)

        item = self.tree.selection()
        self.item_text = self.tree.item(item, "values")

        one_info = tk.Tk()

        winWidth = 300
        winHeight = 150
        # 获取屏幕分辨率
        screenWidth = one_info.winfo_screenwidth()
        screenHeight = one_info.winfo_screenheight()

        x = int((screenWidth - winWidth) / 2)
        y = int((screenHeight - winHeight) / 2)

        # 设置主窗口标题
        one_info.title("商品信息录入")
        # 设置窗口初始位置在屏幕居中
        one_info.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y))



        lb_quantity = tk.Label(one_info, bg='#DDEBF7', font=('Arial', 12), text='数量')
        lb_value = tk.Label(one_info, bg='#DDEBF7', font=('Arial', 12), text='金额')
        lb_quantity.place(x=10, y=20)
        lb_value.place(x=140, y=20)

        En_quantity = tk.Entry(one_info, textvariable=self.quantity, bd=2, justify='center', width=10, bg='#DDEBF7')
        En_value = tk.Entry(one_info, textvariable=self.value, bd=2, justify='center', width=10, bg='#DDEBF7')

        En_quantity.place(x=60, y=20)
        En_value.place(x=180, y=20)

        def cancle():
            one_info.destroy()

        def confirm():
            self.confirm_self(one_info, En_quantity.get(), En_value.get())

        btn_cancle = tk.Button(one_info, text="取消", command=cancle)
        btn_confirm = tk.Button(one_info, text="确认", command=confirm)

        btn_cancle.place(x=60, y=120)
        btn_confirm.place(x=180, y=120)

        one_info.mainloop()

    def confirm_self(self, master, quantity, value):
        master.destroy()
        for i, data in enumerate(self.info_list):
            if data[0] == self.item_text[0]:
                self.info_list[i][1] = quantity
                self.info_list[i][2] = value

        x = self.tree.get_children()
        for item in x:
            self.tree.delete(item)

        i = 0
        for i, data in enumerate(self.info_list):
            self.tree.insert('', i, values=(data[0], data[1], data[2]))
            i += 1
        self.tree.pack(expand=True, fill=BOTH)


    def Sell(self):
        a = messagebox.askokcancel('出库确认', '您是否要要将编号为 %s 的商品出库出库？' % self.selected)  # 弹出对话框
        if a:
            print(self.selected)
            self.win.destroy()
            self.is_selected = True
        else:
            self.is_selected = False

    def Back(self):
        self.is_quare = False
        self.win.destroy()
        self.is_selected = False

    def selectTree(self, event):
        item_list = []
        for item in self.table.selection():
            item_id = self.table.item(item, "values")[0]
            # print(item_text)
            item_list.append(item_id)
        selected = ', '.join(item_list)
        # print(selected)
        self.selected = selected
        self.item_list = item_list


def Quare(info_):
    quare = Sell(info_)
    selected = quare.selected
    return selected


if __name__ == '__main__':
    Quare(info)
