from tkinter import *


# 定义的方法 监听键盘事件
def printkey(event):
    print('你按下了: ' + event.char)


# 实例化tk
root = Tk()
# 实例化一个输入框
# entry = Entry(root)
entry = Frame(root, width=100, height=100)
entry.focus_set()
# 给输入框绑定按键监听事件<Key>为监听任何按键 <Key-x>监听其它键盘，如大写的A<Key-A>、回车<Key-Return>
entry.bind('<Key-Return>', printkey)
# 显示窗体
entry.pack()
root.mainloop()