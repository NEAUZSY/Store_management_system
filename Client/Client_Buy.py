import tkinter as tk
from tkinter import messagebox
from SQL import MyDb

FORM = {}


def init_purchase(root):
    root_P = root
    root_P.title('进项管理')

    screenwidth = root_P.winfo_screenwidth()  # 屏幕宽度
    screenheight = root_P.winfo_screenheight()  # 屏幕高度
    width = 360
    height = 520
    x = int((screenwidth - width) / 2)
    y = int((screenheight - height) / 2)
    root_P.geometry('{}x{}+{}+{}'.format(width, height, x, y))  # 大小以及位置

    root_P.configure(bg='#DDEBF7')
    title = tk.Label(root_P,
                     bg='#DDEBF7',
                     font=('Arial', 16),
                     text='商品购入')
    title.place(x=110, y=20)


def init_form(root):
    lb1 = tk.Label(root,
                   bg='#DDEBF7',
                   font=('Arial', 12),
                   text='往来单位：')
    lb1.place(x=5, y=80)

    lb2 = tk.Label(root,
                   bg='#DDEBF7',
                   font=('Arial', 12),
                   text='一级分类：')
    lb2.place(x=5, y=120)

    lb3 = tk.Label(root,
                   bg='#DDEBF7',
                   font=('Arial', 12),
                   text='二级分类')
    lb3.place(x=5, y=160)

    lb4 = tk.Label(root,
                   bg='#DDEBF7',
                   font=('Arial', 12),
                   text='商品名称')
    lb4.place(x=5, y=200)

    lb5 = tk.Label(root,
                   bg='#DDEBF7',
                   font=('Arial', 12),
                   text='规格型号')
    lb5.place(x=5, y=240)

    lb6 = tk.Label(root,
                   bg='#DDEBF7',
                   font=('Arial', 12),
                   text='单        位：')
    lb6.place(x=5, y=280)

    lb7 = tk.Label(root,
                   bg='#DDEBF7',
                   font=('Arial', 12),
                   text='数        量：')
    lb7.place(x=5, y=320)

    lb8 = tk.Label(root,
                   bg='#DDEBF7',
                   font=('Arial', 12),
                   text='含税进价：')
    lb8.place(x=5, y=360)

    lb9 = tk.Label(root,
                   bg='#DDEBF7',
                   font=('Arial', 12),
                   text='未税进价')
    lb9.place(x=5, y=400)

    En1 = tk.Entry(root, bd=2)
    En1.place(x=100, y=80)
    En2 = tk.Entry(root, bd=2)
    En2.place(x=100, y=120)
    En3 = tk.Entry(root, bd=2)
    En3.place(x=100, y=160)
    En4 = tk.Entry(root, bd=2)
    En4.place(x=100, y=200)
    En5 = tk.Entry(root, bd=2)
    En5.place(x=100, y=240)
    En6 = tk.Entry(root, bd=2)
    En6.place(x=100, y=280)
    En7 = tk.Entry(root, bd=2)
    En7.place(x=100, y=320)
    En8 = tk.Entry(root, bd=2)
    En8.place(x=100, y=360)
    En9 = tk.Entry(root, bd=2)
    En9.place(x=100, y=400)

    # is_with_tax = tk.IntVar()
    # with_tax = tk.Radiobutton(root, text='含税', variable=is_with_tax, value=1, )
    # with_tax.place(x=250, y=430)
    # without_tax = tk.Radiobutton(root, text='未税', variable=is_with_tax, value=0, )
    # without_tax.place(x=300, y=430)

    forms = En1, En2, En3, En4, En5, En6, En7, En8, En9, root  # , is_with_tax

    btn_finsh = tk.Button(root, text="确认", command=lambda _forms=forms: add_purchase(_forms))
    btn_finsh.place(x=100, y=460)


def add_purchase(forms):
    global FORM, max_id
    goods_id = max_id + 1
    # En1, En2, En3, En4, En5, En6, En7, En8, root, is_with_tax = forms
    En1, En2, En3, En4, En5, En6, En7, En8, En9, root = forms
    form = {'商品编号': goods_id,
            '往来单位': En1.get(),
            '一级分类': En2.get(),
            '二级分类': En3.get(),
            '商品名称': En4.get(),
            '规格型号': En5.get(),
            '单位': En6.get(),
            '数量': En7.get()}

    if En8.get() and En9.get():
        messagebox.askokcancel('输入有误', '您只能输入一个价格')
        return
    elif En9.get():
        without_tax = float(En9.get())
        form['未税进价'] = without_tax
        form['含税进价'] = without_tax * 1.13
    elif En8.get():
        with_tax = float(En8.get())
        form['含税进价'] = with_tax
        form['未税进价'] = with_tax / 1.13
    else:
        messagebox.askokcancel('输入有误', '您还没有输入价格')
        return
    root.destroy()
    print(form)
    FORM = form


def main():
    global max_id
    db = MyDb()
    print('当前库存为')
    data = db.query()
    if data:
        max_id = data[0][0]
        for row in data:
            if row[0] >= max_id:
                max_id = row[0]
    else:
        max_id = 0

    print('进入了采购页面')
    root = tk.Tk()
    init_purchase(root)
    init_form(root)
    root.mainloop()
    return FORM


if __name__ == '__main__':
    main()
