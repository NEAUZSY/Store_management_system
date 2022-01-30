from datetime import datetime
import tkinter as tk

tt = datetime.now().strftime('%Y-%m-%d')
yy = tt[0:4]
mm = tt[5:7]
dd = tt[8:10]
print(yy, '年', mm, '月', dd, '日')
