import time
import pickle
import tkinter as tk

from tkinter import messagebox  # import this to fix messagebox error

Log_Variable = False


window_Log = tk.Tk()
screenwidth = window_Log.winfo_screenwidth()  # 屏幕宽度
screenheight = window_Log.winfo_screenheight()  # 屏幕高度
window_Log.title('缘客推理馆信息管理系统V2.0')
width = 440
height = 220
x = int((screenwidth - width) / 2)
y = int((screenheight - height) / 2)
window_Log.geometry('{}x{}+{}+{}'.format(width, height, x, y))  # 大小以及位置

# welcome image
canvas = tk.Canvas(window_Log, height=240, width=600)
image_file = tk.PhotoImage(file='../file/Logo.gif')
image = canvas.create_image(0, 0, anchor='nw', image=image_file)
canvas.pack(side='top')

# user information
tk.Label(window_Log, text='User name: ').place(x=160, y=50)
tk.Label(window_Log, text='Password: ').place(x=160, y=90)

var_usr_name = tk.StringVar()
var_usr_name.set('admin')
entry_usr_name = tk.Entry(window_Log, textvariable=var_usr_name)
entry_usr_name.place(x=260, y=50)
var_usr_pwd = tk.StringVar()
entry_usr_pwd = tk.Entry(window_Log, textvariable=var_usr_pwd, show='*')
entry_usr_pwd.place(x=260, y=90)


def usr_login():
    global Log_Variable
    usr_name = var_usr_name.get()
    usr_pwd = var_usr_pwd.get()
    try:
        with open('../usrs_info.pickle', 'rb') as usr_file:
            usrs_info = pickle.load(usr_file)
    except FileNotFoundError:
        with open('../usrs_info.pickle', 'wb') as usr_file:
            usrs_info = {'admin': 'admin'}
            pickle.dump(usrs_info, usr_file)
    if usr_name in usrs_info:
        if usr_pwd == usrs_info[usr_name]:
            # tk.messagebox.showinfo(title='Welcome', message='How are you? ' + usr_name)
            Log_Variable = True
            window_Log.destroy()
        else:
            tk.messagebox.showerror(message='Error, your password is wrong, try again.')
            Log_Variable = False
    else:
        is_sign_up = tk.messagebox.askyesno('Welcome',
                                            'You have not signed up yet. Sign up today?')
        if is_sign_up:
            usr_sign_up()


def usr_sign_up():
    def sign_to_Reasoning_Hall():
        np = new_pwd.get()
        npf = new_pwd_confirm.get()
        nn = new_name.get()
        with open('../usrs_info.pickle', 'rb') as usr_file:
            exist_usr_info = pickle.load(usr_file)
        if np != npf:
            tk.messagebox.showerror('Error', 'Password and confirm password must be the same!')
        elif nn in exist_usr_info:
            tk.messagebox.showerror('Error', 'The user has already signed up!')
        else:
            exist_usr_info[nn] = np
            with open('../usrs_info.pickle', 'wb') as usr_file:
                pickle.dump(exist_usr_info, usr_file)
            tk.messagebox.showinfo('Welcome', 'You have successfully signed up!')
            window_sign_up.destroy()

    window_sign_up = tk.Toplevel(window_Log)
    window_sign_up.geometry('350x200')
    window_sign_up.title('Sign up window')

    new_name = tk.StringVar()
    new_name.set('example@python.com')
    tk.Label(window_sign_up, text='User name: ').place(x=10, y=10)
    entry_new_name = tk.Entry(window_sign_up, textvariable=new_name)
    entry_new_name.place(x=150, y=10)

    new_pwd = tk.StringVar()
    tk.Label(window_sign_up, text='Password: ').place(x=10, y=50)
    entry_usr_pwd_ = tk.Entry(window_sign_up, textvariable=new_pwd, show='*')
    entry_usr_pwd_.place(x=150, y=50)

    new_pwd_confirm = tk.StringVar()
    tk.Label(window_sign_up, text='Confirm password: ').place(x=10, y=90)
    entry_usr_pwd_confirm = tk.Entry(window_sign_up, textvariable=new_pwd_confirm, show='*')
    entry_usr_pwd_confirm.place(x=150, y=90)

    btn_comfirm_sign_up = tk.Button(window_sign_up, text='Sign up', command=sign_to_Reasoning_Hall)
    btn_comfirm_sign_up.place(x=150, y=130)


# login and sign up button
btn_login = tk.Button(window_Log, font=('Arial', 12), text='登录', command=usr_login)
btn_login.place(x=260, y=130)
btn_sign_up = tk.Button(window_Log, font=('Arial', 12), text='注册', command=usr_sign_up)
btn_sign_up.place(x=340, y=130)


def Log_In_main():
    window_Log.mainloop()
    return Log_Variable


if __name__ == "__main__":
    Log_In_main()
