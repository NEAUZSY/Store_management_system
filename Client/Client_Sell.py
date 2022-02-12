# -*- encoding=utf-8 -*-
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
from SQL import MyDb

info = [
    ['1001', '李华', '男', '2014-01-25', '广东', '计算5班', '1001', '李华', 10, 1, 10, '计算5班'],
    ['1002', '小米', '男', '2015-11-08', '深圳', '计算5班', '1002', '小米', 10, 2, 20, '计算5班'],
    ['1003', '刘亮', '男', '2015-09-12', '福建', '计算5班', '1003', '刘亮', 10, 3, 30, '计算5班'],
    ['1004', '白鸽', '女', '2016-04-01', '湖南', '计算5班', '1004', '白鸽', 10, 4, 40, '计算5班']]


class Sell(object):
    def __init__(self, info_, db):

        self.db = db

        # 输入为当前tb_store中的库存表
        self.is_selected = True
        self.is_quare = True
        self.public_info = Tk()  # 创建获取往来单位和日期信息的窗口
        self.selected_id = []  # 出库的商品id
        tt = datetime.now().strftime('%Y-%m-%d')
        yy = tt[0:4]
        mm = tt[5:7]
        dd = tt[8:10]
        self.var_yy = StringVar(value=yy)
        self.var_mm = StringVar(value=mm)
        self.var_dd = StringVar(value=dd)
        self.target = StringVar(value='')

        self.quantity = StringVar(value=0)  # 出库商品数量
        self.value = StringVar(value=0)  # 出库商品单价

        self.value_sum = StringVar(value='')  # 出库商品总价

        self.sell = True

        self.info_list = []  # 在第三集窗口中储存信息的列表
        self.item_store = []  # 显示商品对应的真实库存
        self.sell_dic_list = []  # 用来存放出库信息的字典列表 元素师包含某个商品的全部出库信息的字典
        # 初始化往来单位和日期窗口
        self.public_info_get()

        if self.sell:
            # 完成了基本信息的录入 往来单位和出库时间
            self.info_ = info_
            self.win = Tk()  # 窗口
            self.is_quare = True

            self.item_list = ''  # 选中了的商品列表 内容为id 名称 数量和金额
            # 初始化商品信息选择窗口
            self.root_init()

            # 如果在商品选择窗口进行了选择
            if self.is_selected:
                self.value_info = Tk()  # 创建获取往来单位和日期信息的窗口
                # 初始化数量金额指定窗口
                self.value_info_get()

                # print(self.item_store, self.item_list)

                # print('删除了所选内容')
                # print(self.selected_id)
                # self.db.delete(self.selected_id)
                # self.db.refresh_store('delete')
                # 在数据库中更新内容 添加出库单
                self.db.add_sell_info(self.sell_dic_list)
                self.db.reduce(self.sell_dic_list, self.item_store)
                print(self.sell_dic_list)
                print(self.item_store)

    def root_init(self):
        self.win.title('库存查询')  # 标题
        screenwidth = self.win.winfo_screenwidth()  # 屏幕宽度
        screenheight = self.win.winfo_screenheight()  # 屏幕高度
        width = 1300
        height = 500
        x = int((screenwidth - width) / 2)
        y = int((screenheight - height) / 2)
        self.win.geometry('{}x{}+{}+{}'.format(width, height, x, y))  # 大小以及位置

        tabel_frame = Frame(self.win)
        tabel_frame.pack()

        xscroll = Scrollbar(tabel_frame, orient=HORIZONTAL)
        yscroll = Scrollbar(tabel_frame, orient=VERTICAL)

        columns = ['序号', '入库时间', '往来单位', '一级分类',
                   '二级分类', '商品名称', '规格型号', '单位',
                   '数量', '单价', '金额', '备注/序列号']
        table = ttk.Treeview(
            master=tabel_frame,  # 父容器
            height=15,  # 表格显示的行数,height行
            columns=columns,  # 显示的列
            show='headings',  # 隐藏首列
            selectmode="extended",  # 选择模式为可多选
            xscrollcommand=xscroll.set,  # x轴滚动条
            yscrollcommand=yscroll.set,  # y轴滚动条
        )
        # 设置树属性
        for column in columns:
            table.heading(column=column, text=column, anchor=CENTER,
                          command=lambda name=column:
                          messagebox.showinfo('', '{}描述信息~~~'.format(name)))  # 定义表头
            table.column(column=column, width=100, minwidth=100, anchor=CENTER, )  # 定义列
        xscroll.config(command=table.xview)
        xscroll.pack(side=BOTTOM, fill=X)
        yscroll.config(command=table.yview)
        yscroll.pack(side=RIGHT, fill=Y)
        # 向树中添加数据
        for index, data in enumerate(self.info_):
            table.insert('', END, values=data)  # 添加数据到末尾

        # 选择树中内容后的回调函数
        table.bind('<<TreeviewSelect>>', self.selectTree)
        table.pack(fill=BOTH, expand=True)
        self.table = table

        btn_sell = Button(self.win, text="下一步", command=self.Sell)
        btn_sell.place(x=150, y=400)

        btn_back = Button(self.win, text="退出", command=self.Back)
        btn_back.place(x=50, y=400)

        self.win.mainloop()

    def public_info_get(self):
        # 获取往来单位和出库日期
        self.public_info.title('公共信息录入')
        screenwidth = self.public_info.winfo_screenwidth()  # 屏幕宽度
        screenheight = self.public_info.winfo_screenheight()  # 屏幕高度
        width = 300
        height = 180
        x = int((screenwidth - width) / 2)
        y = int((screenheight - height) / 2)
        self.public_info.geometry('{}x{}+{}+{}'.format(width, height, x, y))  # 大小以及位置

        self.public_info.configure(bg='#DDEBF7')
        title = Label(self.public_info,
                      bg='#DDEBF7',
                      font=('Arial', 16),
                      text='商品出库')
        title.place(x=110, y=20)

        lb_yy = Label(self.public_info,
                      bg='#DDEBF7',
                      font=('Arial', 12),
                      text='年')
        lb_yy.place(x=150, y=60)

        lb_mm = Label(self.public_info,
                      bg='#DDEBF7',
                      font=('Arial', 12),
                      text='月')
        lb_mm.place(x=195, y=60)

        lb_dd = Label(self.public_info,
                      bg='#DDEBF7',
                      font=('Arial', 12),
                      text='日')
        lb_dd.place(x=240, y=60)

        En_yy = Entry(self.public_info, textvariable=self.var_yy, bd=2, justify='center', width=6, bg='#DDEBF7',
                      relief="flat")
        En_yy.place(x=105, y=60)
        En_mm = Entry(self.public_info, textvariable=self.var_mm, bd=2, justify='center', width=3, bg='#DDEBF7',
                      relief="flat")
        En_mm.place(x=170, y=60)
        En_dd = Entry(self.public_info, textvariable=self.var_dd, bd=2, justify='center', width=3, bg='#DDEBF7',
                      relief="flat")
        En_dd.place(x=215, y=60)

        lb1 = Label(self.public_info,
                    bg='#DDEBF7',
                    font=('Arial', 12),
                    text='往来单位:')
        lb1.place(x=15, y=90)

        En1 = Entry(self.public_info, textvariable=self.target, bd=2)
        En1.place(x=110, y=90)

        btn_finsh = Button(self.public_info, text="确认", command=self.check_input)
        btn_finsh.place(x=100, y=130)

        btn_back = Button(self.public_info, text="返回", command=self.info_back)
        btn_back.place(x=200, y=130)

        self.public_info.mainloop()

    def check_input(self):
        self.public_info.destroy()

    def info_back(self):
        self.public_info.destroy()
        self.is_quare = False
        self.sell = False

    def value_info_get(self):

        screenwidth = self.value_info.winfo_screenwidth()  # 屏幕宽度
        screenheight = self.value_info.winfo_screenheight()  # 屏幕高度
        width = 800
        height = 130 + len(self.item_list) * 10
        # print(height)
        x = int((screenwidth - width) / 2)
        y = int((screenheight - height) / 2)
        self.value_info.geometry('{}x{}+{}+{}'.format(width, height, x, y))  # 大小以及位置
        self.value_info.title('价格信息录入')

        columns = ("id", "name", "quantity", "value")
        tree = ttk.Treeview(self.value_info, show="headings", columns=columns, selectmode=BROWSE)
        tree.column("id", anchor=CENTER)
        tree.column("name", anchor=CENTER)
        tree.column("quantity", anchor=CENTER)
        tree.column("value", anchor=CENTER)

        # 设置表格头部标题
        tree.heading("id", text="商品编号")
        tree.heading("name", text="商品名称")
        tree.heading("quantity", text="数量")
        tree.heading("value", text="金额")

        # 绘制树
        value_sum = 0
        for i, data in enumerate(self.item_list):
            # print(data)
            tree.insert('', i, values=(data[0], data[1], data[2], data[3]))
            i += 1
            value_sum += float(data[3])
        tree.pack(expand=True, fill=BOTH)

        # 显示总金额
        self.value_sum = StringVar()    # 这里需要重新声明才能正常使用
        self.value_sum.set('出库总额：{}'.format(value_sum))

        display_en = Entry(self.value_info, textvariable=self.value_sum, bd=2, justify='center', width=20, relief="flat")
        display_en.place(x=400, y=height - 50)

        # 金额指定窗口中树的选择回调函数
        tree.bind('<ButtonRelease-1>', self.treeviewClick)
        # 将此窗口属性化
        self.tree = tree

        def Back(master):
            master.destroy()

        btn_back = Button(self.value_info, text="返回", command=lambda: Back(self.value_info))
        btn_back.place(x=350, y=height - 50)

        btn_sell = Button(self.value_info, text="确认", command=self.sell_submit)
        btn_sell.place(x=150, y=height - 50)

        # En1 = Entry(self.public_info, textvariable=self.target, bd=2)
        # En1.place(x=110, y=90)

        self.value_info.mainloop()

    def sell_submit(self):
        """出售提交函数，在金额数量选择窗口处点击确认按钮后的回调函数"""
        # print(self.info_list)
        # print(self.item_list)
        data = "{}-{}-{}".format(self.var_yy.get(), self.var_mm.get(), self.var_dd.get())
        print(self.quantity.get(), self.value.get())
        # 遍历外部传入的列表 此处为所有库存
        for rows in self.info_:
            # 定位到某一个存在于被选择列表中的商品
            if str(rows[0]) in self.selected_id:
                # 生成一个储存单个出库信息的字典
                dic = {'序号': rows[0],
                       '日期': data,
                       '往来单位': self.target.get(),
                       '一级分类': rows[3],
                       '二级分类': rows[4],
                       '商品名称': rows[5],
                       '规格型号': rows[6],
                       '单位': rows[7],
                       '数量': self.quantity.get(),
                       '单价': '%.2f' % (float(self.value.get()) / float(self.quantity.get())),
                       '金额': self.value.get(),
                       '备注/序列号': rows[11],
                       '是否含税': 1}
                self.sell_dic_list.append(dic)
        # print(self.sell_dic_list)
        try:
            self.value_info.destroy()
            # self.public_info.destroy()
        except Exception as e:
            print(e)

    def treeviewClick(self, event):  # 单击
        # for item in self.tree.selection():
        #     item_text = self.tree.item(item, "values")
        #     print(item_text)
        # 获取点击的商品
        item = self.tree.selection()
        self.item_select = self.tree.item(item, "values")
        # 创建一个单独的信息录入窗口
        one_info = Tk()

        winWidth = 300
        winHeight = 150
        # 获取屏幕分辨率
        screenWidth = one_info.winfo_screenwidth()
        screenHeight = one_info.winfo_screenheight()

        x = int((screenWidth - winWidth) / 2)
        y = int((screenHeight - winHeight) / 2)

        # 设置主窗口标题
        one_info.title("单品价格录入")
        # 设置窗口初始位置在屏幕居中
        one_info.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y))
        lb_quantity = Label(one_info, bg='#DDEBF7', font=('Arial', 12), text='数量')
        lb_value = Label(one_info, bg='#DDEBF7', font=('Arial', 12), text='金额')
        lb_quantity.place(x=10, y=20)
        lb_value.place(x=140, y=20)

        En_quantity = Entry(one_info, textvariable=self.quantity, bd=2, justify='center', width=10, bg='#DDEBF7')
        En_value = Entry(one_info, textvariable=self.value, bd=2, justify='center', width=10, bg='#DDEBF7')

        En_quantity.place(x=60, y=20)
        En_value.place(x=180, y=20)

        # 小窗口的取消按钮回调函数
        def cancle():
            one_info.destroy()

        # def confirm():
        #     Sell.confirm_self(one_info, En_quantity.get(), En_value.get())

        btn_cancle = Button(one_info, text="取消", command=cancle)
        btn_confirm = Button(one_info, text="确认",
                             # 确认函数传入参数包括窗口对象和窗口中几个输入框的值
                             command=lambda: self.confirm_self(one_info, En_quantity.get(), En_value.get()))

        btn_cancle.place(x=60, y=120)
        btn_confirm.place(x=180, y=120)

        one_info.mainloop()

    def confirm_self(self, master, quantity, value):

        # print('储存：', self.item_store)
        # print(self.item_select)
        # 在被选择的商品列表中循环
        self.quantity.set(quantity)
        self.value.set(value)
        for i, data in enumerate(self.item_list):
            if float(quantity) > float(self.item_store[i][2]):
                # 如果输入的出库数量大于库存数量择退出本次输入
                messagebox.askokcancel('输入有误', '库存商品不足以出库')  # 弹出对话框
                master.destroy()
                return
            # 在被选择到的所有商品列表中定位刚刚录入过信息的那条商品信息并更新出库列表 item_list
            if str(data[0]) == self.item_select[0]:
                self.item_list[i][2] = quantity
                self.item_list[i][3] = value
        # print('显示：', self.item_list)

        # 关闭小窗口
        master.destroy()

        # 更新金额和数量选择窗口的树
        x = self.tree.get_children()
        for item in x:
            self.tree.delete(item)

        value_sum = 0
        for i, data in enumerate(self.item_list):
            self.tree.insert('', i, values=(data[0], data[1], data[2], data[3]))
            value_sum += float(data[3])

        self.value_sum.set('出库总额：{}'.format(value_sum))
        self.tree.pack(expand=True, fill=BOTH)

    def Sell(self):
        a = messagebox.askokcancel('出库确认', '您是否要要将 %s 出库？' % self.selected_id)  # 弹出对话框
        if a:
            # print(self.selected_id)
            self.win.destroy()
            self.is_selected = True
        else:
            self.is_selected = False

    def Back(self):
        self.is_quare = False
        self.win.destroy()
        self.is_selected = False

    def selectTree(self, event):
        item_list = []
        # 获取选择到的商品部分信息并存到一个列表中
        for row in self.table.selection():
            item = self.table.item(row, "values")
            # print(item_text)
            ID = item[0]
            NAME = item[5]
            QUANTITY = item[8]
            VALUE = item[10]
            item_list.append([ID, NAME, QUANTITY, VALUE])  # 提取库中数据
            self.selected_id.append(ID)
        # selected_id = ', '.join(item_list)
        # print(selected_id)
        # self.selected_id = selected_id

        # 将处理好的列表放到对象属性中
        self.item_list = item_list
        # 复制一个用于储存的元组列表 将在后面库存更新时用到
        self.item_store = [tuple(i) for i in item_list]

    def checkout(self):
        # 更新出库表
        pass

    def refresh_store(self):
        task = []  # 返回一个任务列表 [0]表示需要删除的内容 [1]存储需要修改的内容
        for i, data in enumerate(self.item_list):
            if self.item_store[i] == data:
                print('第 %d 项没有修改' % i)
                continue
            if self.item_store[i][2] == data[2]:
                print('出库数量与当前库存相等，该项库存清空')
                pass
            elif self.item_store[i][2] > data[2]:
                print('库存数量大于出库数量，减少库存')
                pass


def Quare(info_):
    quare = Sell(info_, MyDb())
    selected_id = quare.selected_id
    return selected_id


if __name__ == '__main__':
    Quare(info)
