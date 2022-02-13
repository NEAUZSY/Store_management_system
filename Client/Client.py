import base64
import os
from tkinter import *
from tkinter import messagebox

import Client_Buy as Cb
import Client_Check_Buy as Ccb
import Client_Check_Sell as CCSell
import Client_Check_Store as CCStore
import Client_Login as Cl
import Client_ODO as Co
import Client_Sell as Cs
from SQL import MyDb
from file.logo import logo


class Windows(object):
    def __init__(self, User):

        self.User = User

        # 初始化界面
        self.is_running = True
        self.is_Log_In = True
        self.root = Tk()
        self.root.title('进销存系统')

        screenwidth = self.root.winfo_screenwidth()  # 屏幕宽度
        screenheight = self.root.winfo_screenheight()  # 屏幕高度
        width = 400
        height = 250
        x = int((screenwidth - width) / 2)
        y = int((screenheight - height) / 2)
        self.root.geometry('{}x{}+{}+{}'.format(width, height, x, y))  # 大小以及位置

        # 连接数据库
        lb1 = Label(self.root, text='正在连接数据库……')
        lb1.grid(column=0, row=0)
        self.db = MyDb()
        lb1.configure(text='请选择要使用的功能', font=('Arial', 15), )
        btn_pur = Button(self.root, text="入库登记", command=self.Click_btn_pur)
        btn_sell = Button(self.root, text="出库登记", command=self.Click_btn_sell)
        btn_odo = Button(self.root, text="生成出库单", command=self.Click_btn_odo)

        btn_quera_buy = Button(self.root, text="入库记录查询", command=self.Click_btn_quera_buy)
        btn_stock = Button(self.root, text="库存查询", command=self.Click_btn_stock)
        btn_quera_sell = Button(self.root, text="出库记录查询", command=self.Click_btn_quera_sell)

        btn_logout = Button(self.root, text="注销", command=self.Click_btn_logout)
        btn_exit = Button(self.root, text="退出", command=self.Click_btn_exit)
        btn_clean = Button(self.root, text="清空数据库", command=self.Click_btn_clean)

        # -----------------操作按钮-----------------
        # 入库登记按钮
        btn_pur.place(x=100, y=50)

        # 出库登记按钮
        btn_odo.place(x=100, y=100)

        # 出库单按钮
        btn_sell.place(x=100, y=150)

        # -----------------查询按钮-----------------
        # 入库查询按钮
        btn_quera_buy.place(x=250, y=50)

        # 库存查询按钮
        btn_stock.place(x=250, y=100)

        # 出库查询按钮
        btn_quera_sell.place(x=250, y=150)

        # -----------------功能按钮-----------------
        # 注销按钮
        btn_logout.place(x=70, y=200)

        # 退出按钮
        btn_exit.place(x=170, y=200)

        # 清空数据按钮
        btn_clean.place(x=270, y=200)

        self.root.mainloop()

    def Click_btn_pur(self):
        # 入库按钮回调函数
        self.root.destroy()
        buy = Cb.Buy()
        form = buy.filling()
        if form:
            self.db.upload('tb_buy', form)

    def Click_btn_sell(self):
        # 出库按钮回调函数
        self.root.destroy()
        # 查询库存
        temp = self.db.query('tb_store')
        # 使用查询到的库存初始化出售对象，并传入数据库对象
        Sell = Cs.Sell(temp, self.db)

    def Click_btn_odo(self):
        # 生成库存单按钮回调函数
        self.root.destroy()
        # 查询库存
        temp = self.db.query('tb_sell')
        # 使用查询到的库存初始化出售对象，并传入数据库对象
        ODO = Co.ODO(temp, self.db, self.User)

    def Click_btn_quera_buy(self):
        # 入库记录查询按钮回调
        self.root.destroy()
        is_check = True
        while is_check:
            temp = self.db.query('tb_buy')
            Store = Ccb.Store(temp)
            is_check = Store.is_check

    def Click_btn_stock(self):
        # 查询库存按钮回调函数
        self.root.destroy()
        is_check = True
        while is_check:
            temp = self.db.query('tb_store')
            Store = CCStore.Store(temp)
            is_check = Store.is_check

    def Click_btn_quera_sell(self):
        # 入库记录查询按钮回调
        self.root.destroy()
        is_check = True
        while is_check:
            temp = self.db.query('tb_sell')
            Sell = CCSell.Sell(temp)
            is_check = Sell.is_check

    def Click_btn_logout(self):
        # 注销
        self.is_Log_In = False
        self.root.destroy()

    def Click_btn_exit(self):
        # 退出
        self.is_Log_In = False
        self.is_running = False
        self.root.destroy()

    def Click_btn_clean(self):

        a = messagebox.askokcancel('清空确认', '您是否要要清楚数据库数据？')
        if a:
            self.db.execute("TRUNCATE TABLE tb_buy;")
            self.db.execute("TRUNCATE TABLE tb_store;")
            self.db.execute("TRUNCATE TABLE tb_sell;")
        else:
            return


def main():
    is_running = True
    img_data = base64.b64decode(logo)
    with open('./logo.png', 'wb') as f:
        f.write(img_data)
    while is_running:
        # 整个程序的循环，方便注销后依然能够进入系统
        is_Log_In, is_running, User = Cl.Log_In_main()
        while is_Log_In:
            root = Windows(User)
            is_Log_In = root.is_Log_In
            is_running = root.is_running
    os.remove('./logo.png')


if __name__ == '__main__':
    main()
