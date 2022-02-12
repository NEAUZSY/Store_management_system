import os, base64
from file.logo import logo
with open("../file/Logo.gif","rb") as f:
    # b64encode是编码，b64decode是解码
    base64_data = base64.b64encode(f.read())

    print(base64_data)#输出生成的base64码


#img_str = 'abcdefgh12345oK='#比如生成后的码就这么放，替换下面的base64_data即可
img_data = base64.b64decode(logo)
# 注意：如果是"data:image/jpg:base64,"，那你保存的就要以png格式，如果是"data:image/png:base64,"那你保存的时候就以jpg格式。
with open('logo.png', 'wb') as f:
    f.write(img_data)


# coding=utf-8
