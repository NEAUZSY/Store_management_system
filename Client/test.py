import win32com.client


def main():
    xlApp = win32com.client.Dispatch('Excel.Application')
    xlApp.Visible = 0  # 不在后台运行
    xlApp.EnableEvents = False
    xlApp.DisplayAlerts = False  # 显示弹窗
    xlBook = xlApp.Workbooks.Open(r'C:\Users\NEAUZSY\Desktop\新建 Microsoft Excel 工作表 (2).xlsx')  # 打印的文件
    xlApp.ActiveWorkbook.Sheets(1).PageSetup.Zoom = False
    xlApp.ActiveWorkbook.Sheets(1).PageSetup.FitToPagesWide = 1  # 页数范围
    xlApp.ActiveWorkbook.Sheets(1).PageSetup.FitToPagesTall = 10
    # xlBook.Save() #保存
    ename = xlApp.ActiveWorkbook.name  # 获取打开工作表名称
    print('正在打印>', ename)
    xlBook.PrintOut()
    # xlBook.PrintOut(1,5) # 打印页数1-5
    xlApp.quit()  # 退出


if __name__ == '__main__':
    main()
