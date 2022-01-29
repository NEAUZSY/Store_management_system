import tkinter as tk

FORM = {}


def init_purchase(root):
    root_P = root
    root_P.title('进项管理')

    screenwidth = root_P.winfo_screenwidth()  # 屏幕宽度
    screenheight = root_P.winfo_screenheight()  # 屏幕高度
    width = 320
    height = 480
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
                   text='采购单号：')
    lb1.place(x=5, y=100)

    lb2 = tk.Label(root,
                   bg='#DDEBF7',
                   font=('Arial', 12),
                   text='采购单位：')
    lb2.place(x=5, y=150)

    lb3 = tk.Label(root,
                   bg='#DDEBF7',
                   font=('Arial', 12),
                   text='采购日期')
    lb3.place(x=5, y=200)

    lb4 = tk.Label(root,
                   bg='#DDEBF7',
                   font=('Arial', 12),
                   text='规        格：')
    lb4.place(x=5, y=250)

    lb5 = tk.Label(root,
                   bg='#DDEBF7',
                   font=('Arial', 12),
                   text='型        号：')
    lb5.place(x=5, y=300)

    lb6 = tk.Label(root,
                   bg='#DDEBF7',
                   font=('Arial', 12),
                   text='数        量：：')
    lb6.place(x=5, y=350)

    En1 = tk.Entry(root, bd=2)
    En1.place(x=100, y=100)
    En2 = tk.Entry(root, bd=2)
    En2.place(x=100, y=150)
    En3 = tk.Entry(root, bd=2)
    En3.place(x=100, y=200)
    En4 = tk.Entry(root, bd=2)
    En4.place(x=100, y=250)
    En5 = tk.Entry(root, bd=2)
    En5.place(x=100, y=300)
    En6 = tk.Entry(root, bd=2)
    En6.place(x=100, y=350)

    forms = En1, En2, En3, En4, En5, En6, root

    btn_finsh = tk.Button(root, text="确认", command=lambda _forms=forms: add_purchase(_forms))
    btn_finsh.place(x=100, y=400)


def add_purchase(forms):
    global FORM
    En1, En2, En3, En4, En5, En6, root = forms
    form = {'采购单号': En1.get(),
            '采购单位': En2.get(),
            '采购日期': En3.get(),
            '规格': En4.get(),
            '型号': En5.get(),
            '数量': En6.get()}
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
