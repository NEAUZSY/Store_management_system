import pickle
import tkinter as tk
from tkinter import messagebox  # import this to fix messagebox error


class LogIn(object):
    def __init__(self):

        self.window_Log = tk.Tk()

        self.is_running = True
        self.Log_Variable = False
        self.new_pwd = tk.StringVar()
        self.var_usr_name = tk.StringVar()
        self.var_usr_name.set('admin')
        self.new_pwd_confirm = tk.StringVar()
        self.new_name = tk.StringVar()
        self.new_name.set('example@python.com')

        screenwidth = self.window_Log.winfo_screenwidth()  # 屏幕宽度
        screenheight = self.window_Log.winfo_screenheight()  # 屏幕高度
        self.window_Log.title('Oscar云库存管理系统V1.1')
        width = 440
        height = 220
        x = int((screenwidth - width) / 2)
        y = int((screenheight - height) / 2)
        self.window_Log.geometry('{}x{}+{}+{}'.format(width, height, x, y))  # 大小以及位置

        # welcome image
        canvas = tk.Canvas(self.window_Log, height=240, width=600)
        image_file = tk.PhotoImage(file='../file/Logo.gif')
        canvas.create_image(0, 0, anchor='nw', image=image_file)
        canvas.pack(side='top')

        # user information
        tk.Label(self.window_Log, text='User name: ').place(x=160, y=50)
        tk.Label(self.window_Log, text='Password: ').place(x=160, y=90)

        entry_usr_name = tk.Entry(self.window_Log, textvariable=self.var_usr_name)
        entry_usr_name.place(x=260, y=50)
        self.var_usr_pwd = tk.StringVar()
        entry_usr_pwd = tk.Entry(self.window_Log, textvariable=self.var_usr_pwd, show='*')
        entry_usr_pwd.place(x=260, y=90)

        # login and sign up button
        btn_login = tk.Button(self.window_Log, font=('Arial', 12), text='登录', command=self.usr_login)
        btn_login.place(x=260, y=130)
        btn_sign_up = tk.Button(self.window_Log, font=('Arial', 12), text='注册', command=self.usr_sign_up)
        btn_sign_up.place(x=340, y=130)

        self.window_Log.protocol('WM_DELETE_WINDOW', self.exit)
        self.window_Log.focus_set()
        self.window_Log.bind('<Key-Return>', self.usr_login)
        self.window_Log.mainloop()

    def sign_to_Reasoning_Hall(self):
        np = self.new_pwd.get()
        npf = self.new_pwd_confirm.get()
        nn = self.new_name.get()
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
            self.window_sign_up.destroy()

    def usr_login(self, event=None):
        print('正在登陆')
        usr_name = self.var_usr_name.get()
        usr_pwd = self.var_usr_pwd.get()
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
                self.Log_Variable = True
                self.window_Log.destroy()
            else:
                tk.messagebox.showerror(message='Error, your password is wrong, try again.')
                self.Log_Variable = False
        else:
            is_sign_up = tk.messagebox.askyesno('Welcome',
                                                'You have not signed up yet. Sign up today?')
            if is_sign_up:
                self.usr_sign_up()

    def usr_sign_up(self):
        self.window_sign_up = tk.Toplevel(self.window_Log)
        self.entry_new_name = tk.Entry(self.window_sign_up, textvariable=self.new_name)
        self.window_sign_up.geometry('350x200')
        self.window_sign_up.title('Sign up window')

        tk.Label(self.window_sign_up, text='User name: ').place(x=10, y=10)
        self.entry_new_name.place(x=150, y=10)

        self.new_pwd = tk.StringVar()
        tk.Label(self.window_sign_up, text='Password: ').place(x=10, y=50)
        entry_usr_pwd_ = tk.Entry(self.window_sign_up, textvariable=self.new_pwd, show='*')
        entry_usr_pwd_.place(x=150, y=50)

        tk.Label(self.window_sign_up, text='Confirm password: ').place(x=10, y=90)
        entry_usr_pwd_confirm = tk.Entry(self.window_sign_up, textvariable=self.new_pwd_confirm, show='*')
        entry_usr_pwd_confirm.place(x=150, y=90)

        btn_comfirm_sign_up = tk.Button(self.window_sign_up, text='Sign up', command=self.sign_to_Reasoning_Hall)
        btn_comfirm_sign_up.place(x=150, y=130)

    def exit(self):
        self.window_Log.destroy()
        self.is_running = False


def Log_In_main():
    Log = LogIn()
    return Log.Log_Variable, Log.is_running


if __name__ == "__main__":
    Log_In_main()
