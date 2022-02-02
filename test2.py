from tkinter import filedialog
import tkinter


# 定义文件路径选择时间
def Button_command():
    # Folderpath = filedialog.askdirectory()  # 获得选择好的文件夹
    Filepath = filedialog.askopenfilename()  # 获得选择好的文件

    t1 = tkinter.StringVar()
    t1.set(Filepath)
    entry = tkinter.Entry(root1, textvariable=t1).place(x=80, y=15)
    print(t1.get())


if __name__ == '__main__':
    root1 = tkinter.Tk()
    root1.geometry('300x400')
    root1.wm_title('GUI')
    label0 = tkinter.Label(root1, text='文件路径：')
    label0.place(x=10, y=10)
    t2 = tkinter.Entry(root1, width=20).place(x=80, y=15)
    btn = tkinter.Button(root1, text='...', width=2, height=1, command=Button_command).place(x=240, y=10)
    root1.mainloop()
