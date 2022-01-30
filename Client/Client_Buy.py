from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from SQL import MyDb


class Buy(object):
    def __init__(self):
        self.db = MyDb()
        self.form = {}

        tt = datetime.now().strftime('%Y-%m-%d')
        yy = tt[0:4]
        mm = tt[5:7]
        dd = tt[8:10]

        # print('当前库存为')
        data = self.db.query()
        self.max_id = 0
        if data:
            self.max_id = data[0][0]
            for row in data:
                if row[0] >= self.max_id:
                    self.max_id = row[0]

        # print('进入了采购页面')
        self.root = tk.Tk()
        self.var_yy = tk.StringVar(value=yy)
        self.var_mm = tk.StringVar(value=mm)
        self.var_dd = tk.StringVar(value=dd)

    def filling(self):
        self.init_purchase()
        self.init_form()
        self.root.mainloop()
        return self.form

    def init_purchase(self):
        root_P = self.root
        root_P.title('进项管理')

        screenwidth = root_P.winfo_screenwidth()  # 屏幕宽度
        screenheight = root_P.winfo_screenheight()  # 屏幕高度
        width = 300
        height = 560
        x = int((screenwidth - width) / 2)
        y = int((screenheight - height) / 2)
        root_P.geometry('{}x{}+{}+{}'.format(width, height, x, y))  # 大小以及位置

        root_P.configure(bg='#DDEBF7')
        title = tk.Label(root_P,
                         bg='#DDEBF7',
                         font=('Arial', 16),
                         text='商品购入')
        title.place(x=110, y=20)

    def init_form(self):
        root = self.root

        lb_yy = tk.Label(root,
                         bg='#DDEBF7',
                         font=('Arial', 12),
                         text='年')
        lb_yy.place(x=150, y=60)

        lb_mm = tk.Label(root,
                         bg='#DDEBF7',
                         font=('Arial', 12),
                         text='月')
        lb_mm.place(x=195, y=60)

        lb_dd = tk.Label(root,
                         bg='#DDEBF7',
                         font=('Arial', 12),
                         text='日')
        lb_dd.place(x=240, y=60)

        En_yy = tk.Entry(root, textvariable=self.var_yy, bd=2, justify='center', width=6, bg='#DDEBF7', relief="flat")
        En_yy.place(x=105, y=60)
        En_mm = tk.Entry(root, textvariable=self.var_mm, bd=2, justify='center', width=3, bg='#DDEBF7', relief="flat")
        En_mm.place(x=170, y=60)
        En_dd = tk.Entry(root, textvariable=self.var_dd, bd=2, justify='center', width=3, bg='#DDEBF7', relief="flat")
        En_dd.place(x=215, y=60)

        lb1 = tk.Label(root,
                       bg='#DDEBF7',
                       font=('Arial', 12),
                       text='往来单位:')
        lb1.place(x=15, y=90)

        lb2 = tk.Label(root,
                       bg='#DDEBF7',
                       font=('Arial', 12),
                       text='一级分类:')
        lb2.place(x=15, y=130)

        lb3 = tk.Label(root,
                       bg='#DDEBF7',
                       font=('Arial', 12),
                       text='二级分类:')
        lb3.place(x=15, y=170)

        lb4 = tk.Label(root,
                       bg='#DDEBF7',
                       font=('Arial', 12),
                       text='商品名称:')
        lb4.place(x=15, y=210)

        lb5 = tk.Label(root,
                       bg='#DDEBF7',
                       font=('Arial', 12),
                       text='规格型号:')
        lb5.place(x=15, y=250)

        lb6 = tk.Label(root,
                       bg='#DDEBF7',
                       font=('Arial', 12),
                       text='单        位:')
        lb6.place(x=15, y=290)

        lb7 = tk.Label(root,
                       bg='#DDEBF7',
                       font=('Arial', 12),
                       text='数        量:')
        lb7.place(x=15, y=330)

        lb8 = tk.Label(root,
                       bg='#DDEBF7',
                       font=('Arial', 12),
                       text='含税进价:')
        lb8.place(x=15, y=370)

        lb9 = tk.Label(root,
                       bg='#DDEBF7',
                       font=('Arial', 12),
                       text='未税进价:')
        lb9.place(x=15, y=410)

        lb10 = tk.Label(root,
                        bg='#DDEBF7',
                        font=('Arial', 12),
                        text='备注/序列号:')
        lb10.place(x=15, y=450)

        En1 = tk.Entry(root, bd=2)
        En1.place(x=110, y=90)
        En2 = tk.Entry(root, bd=2)
        En2.place(x=110, y=130)
        En3 = tk.Entry(root, bd=2)
        En3.place(x=110, y=170)
        En4 = tk.Entry(root, bd=2)
        En4.place(x=110, y=210)
        En5 = tk.Entry(root, bd=2)
        En5.place(x=110, y=250)
        En6 = tk.Entry(root, bd=2)
        En6.place(x=110, y=290)
        En7 = tk.Entry(root, bd=2)
        En7.place(x=110, y=330)
        En8 = tk.Entry(root, bd=2)
        En8.place(x=110, y=370)
        En9 = tk.Entry(root, bd=2)
        En9.place(x=110, y=410)
        En10 = tk.Entry(root, bd=2)
        En10.place(x=110, y=450)

        # is_with_tax = tk.IntVar()
        # with_tax = tk.Radiobutton(root, text='含税', variable=is_with_tax, value=1, )
        # with_tax.place(x=250, y=430)
        # without_tax = tk.Radiobutton(root, text='未税', variable=is_with_tax, value=0, )
        # without_tax.place(x=300, y=430)

        self.forms = En1, En2, En3, En4, En5, En6, En7, En8, En9, En10, root  # , is_with_tax

        btn_finsh = tk.Button(root, text="继续录入", command=self.add_purchase)
        btn_finsh.place(x=80, y=500)

        btn_finsh = tk.Button(root, text="确认", command=self.add_purchase)
        btn_finsh.place(x=200, y=500)

    def add_purchase(self):
        goods_id = self.max_id + 1
        data = "{}-{}-{}".format(self.var_yy.get(), self.var_mm.get(), self.var_dd.get())
        En1, En2, En3, En4, En5, En6, En7, En8, En9, En10, root = self.forms
        form = {'商品编号': goods_id,
                '日期': data,
                '往来单位': En1.get(),
                '一级分类': En2.get(),
                '二级分类': En3.get(),
                '商品名称': En4.get(),
                '规格型号': En5.get(),
                '单位': En6.get(),
                '数量': En7.get(),
                '备注/序列号': En10.get()}

        if En8.get() and En9.get():
            messagebox.askokcancel('输入有误', '您只能输入一个价格')
            return
        elif En9.get():
            without_tax = float(En9.get())
            form['未税进价'] = without_tax
            form['含税进价'] = without_tax * 1.13
            form['实际进价'] = without_tax
        elif En8.get():
            with_tax = float(En8.get())
            form['含税进价'] = with_tax
            form['未税进价'] = with_tax / 1.13
            form['实际进价'] = with_tax
        else:
            messagebox.askokcancel('输入有误', '您还没有输入价格')
            return
        root.destroy()
        self.form = form


def main():
    buy = Buy()
    return buy.filling()


if __name__ == '__main__':
    main()
