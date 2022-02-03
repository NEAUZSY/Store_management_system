from tkinter import *
import Client_Buy as Cb
import Client_Login as Cl
import Client_Check_Buy as Ccb
import Client_Check_Sell as Ccs
import Client_Sell as Cs
from SQL import MyDb


class Windows(object):
    def __init__(self):
        # 初始化界面
        self.is_running = True
        self.is_Log_In = True
        self.root = Tk()
        self.root.title('进销存系统')

        screenwidth = self.root.winfo_screenwidth()  # 屏幕宽度
        screenheight = self.root.winfo_screenheight()  # 屏幕高度
        width = 190
        height = 350
        x = int((screenwidth - width) / 2)
        y = int((screenheight - height) / 2)
        self.root.geometry('{}x{}+{}+{}'.format(width, height, x, y))  # 大小以及位置

        self.whichwindows = 0
        # 连接数据库
        lb1 = Label(self.root, text='正在连接数据库……')
        lb1.grid(column=0, row=0)
        self.db = MyDb()
        lb1.configure(text='请选择要使用的功能', font=('Arial', 15), )
        btn_pur = Button(self.root, text="入库登记", command=self.Click_btn_pur)
        btn_quera_buy = Button(self.root, text="入库记录查询", command=self.Click_btn_quera_buy)
        btn_stock = Button(self.root, text="库存查询", command=self.Click_btn_stock)
        btn_sell = Button(self.root, text="出库登记", command=self.Click_btn_sell)
        btn_quera_sell = Button(self.root, text="出库记录查询", command=self.Click_btn_quera_sell)
        btn_logout = Button(self.root, text="注销", command=self.Click_btn_logout)
        btn_exit = Button(self.root, text="退出", command=self.Click_btn_exit)

        # 这里需要插入一个费用录入按钮 fee 按钮
        btn_pur.place(x=60, y=50)
        btn_quera_buy.place(x=60, y=100)
        btn_stock.place(x=60, y=150)
        btn_sell.place(x=60, y=200)
        btn_quera_sell.place(x=60, y=250)

        btn_logout.place(x=30, y=300)
        btn_exit.place(x=110, y=300)
        self.root.mainloop()

    def Click_btn_pur(self):
        # 入库按钮回调函数
        self.whichwindows = 1
        self.root.destroy()
        buy = Cb.Buy()
        form = buy.filling()
        if form:
            self.db.upload('tb_buy', form)

    def Click_btn_quera_buy(self):
        # 入库记录查询按钮回调
        is_check = True
        while is_check:
            temp = self.db.query('tb_buy')
            Store = Ccb.Store(temp)
            is_check = Store.is_check

    def Click_btn_stock(self):
        # 查询库存按钮回调函数
        self.whichwindows = 3
        self.root.destroy()
        is_check = True
        while is_check:
            temp = self.db.query('tb_store')
            Store = Ccb.Store(temp)
            is_check = Store.is_check

    def Click_btn_sell(self):
        # 出库按钮回调函数
        self.whichwindows = 2
        self.root.destroy()
        is_quare = True
        while is_quare:
            temp = self.db.query('tb_store')
            Sell = Cs.Sell(temp)
            select = Sell.is_selected
            # 获取选择状态，是否在库存商品页面进行了选取
            if select:
                pass
                self.db.delete(select)
                self.db.refresh_store('delete')
            dics = Sell.sell_dic_list
            self.db.add_sell_info(dics)
            is_quare = Sell.is_quare

    def Click_btn_quera_sell(self):
        # 入库记录查询按钮回调
        is_check = True
        while is_check:
            temp = self.db.query('tb_sell')
            Sell = Ccs.Sell(temp)
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


def main():
    is_running = True
    while is_running:
        # 整个程序的循环，方便注销后依然能够进入系统
        is_Log_In, is_running = Cl.Log_In_main()
        while is_Log_In:
            root = Windows()
            is_Log_In = root.is_Log_In
            is_running = root.is_running


if __name__ == '__main__':
    main()
