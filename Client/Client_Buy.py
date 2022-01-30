import tkinter as tk

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
                   text='商品编号：')
    lb1.place(x=5, y=80)

    lb2 = tk.Label(root,
                   bg='#DDEBF7',
                   font=('Arial', 12),
                   text='类        别：')
    lb2.place(x=5, y=130)

    lb3 = tk.Label(root,
                   bg='#DDEBF7',
                   font=('Arial', 12),
                   text='商品名称')
    lb3.place(x=5, y=180)

    lb4 = tk.Label(root,
                   bg='#DDEBF7',
                   font=('Arial', 12),
                   text='规格型号')
    lb4.place(x=5, y=230)

    lb5 = tk.Label(root,
                   bg='#DDEBF7',
                   font=('Arial', 12),
                   text='商品来源')
    lb5.place(x=5, y=280)

    lb6 = tk.Label(root,
                   bg='#DDEBF7',
                   font=('Arial', 12),
                   text='单        位：')
    lb6.place(x=5, y=330)

    lb7 = tk.Label(root,
                   bg='#DDEBF7',
                   font=('Arial', 12),
                   text='数        量：')
    lb7.place(x=5, y=380)

    lb8 = tk.Label(root,
                   bg='#DDEBF7',
                   font=('Arial', 12),
                   text='价        格：')
    lb8.place(x=5, y=430)

    En1 = tk.Entry(root, bd=2)
    En1.place(x=100, y=80)
    En2 = tk.Entry(root, bd=2)
    En2.place(x=100, y=130)
    En3 = tk.Entry(root, bd=2)
    En3.place(x=100, y=180)
    En4 = tk.Entry(root, bd=2)
    En4.place(x=100, y=230)
    En5 = tk.Entry(root, bd=2)
    En5.place(x=100, y=280)
    En6 = tk.Entry(root, bd=2)
    En6.place(x=100, y=330)
    En7 = tk.Entry(root, bd=2)
    En7.place(x=100, y=380)
    En8 = tk.Entry(root, bd=2)
    En8.place(x=100, y=430)

    is_with_tax = tk.IntVar()
    with_tax = tk.Radiobutton(root, text='含税', variable=is_with_tax, value=1, )
    with_tax.place(x=250, y=430)
    without_tax = tk.Radiobutton(root, text='未税', variable=is_with_tax, value=0, )
    without_tax.place(x=300, y=430)

    forms = En1, En2, En3, En4, En5, En6, En7, En8, root, is_with_tax

    btn_finsh = tk.Button(root, text="确认", command=lambda _forms=forms: add_purchase(_forms))
    btn_finsh.place(x=100, y=460)


def add_purchase(forms):
    global FORM
    En1, En2, En3, En4, En5, En6, En7, En8, root, is_with_tax = forms
    form = {'商品编号': En1.get(),
            '类别': En2.get(),
            '商品名称': En3.get(),
            '规格型号': En4.get(),
            '商品来源': En5.get(),
            '单位': En6.get(),
            '数量': En7.get()}
    if is_with_tax:
        form['含税进价'] = float(En7.get())
        form['未税进价'] = float(En7.get()) / 1.3
    else:
        form['未税进价'] = float(En7.get())
        form['含税进价'] = float(En7.get()) * 1.3
    root.destroy()
    print(form)
    FORM = form


def main():
    print('进入了采购页面')
    root = tk.Tk()
    init_purchase(root)
    init_form(root)
    root.mainloop()
    return FORM


if __name__ == '__main__':
    main()
