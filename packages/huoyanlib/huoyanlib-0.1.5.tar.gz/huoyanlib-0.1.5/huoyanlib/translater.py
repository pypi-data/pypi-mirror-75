from tkinter import *
from tkinter import messagebox

import requests

root = Tk()
root.title('作品(翻译)')
root.geometry('370x100')
print("只支持中文和英文哦")
s_with = root.winfo_screenwidth()
s_height = root.winfo_screenheight()
l_x = str(round((s_with - 370) / 2))
l_y = str(round((s_height - 100) / 2))
root.geometry('+' + l_x + '+' + l_y)
lable = Label(root, text='请输入内容：')
lable.grid()
extry = Entry(root, font=('微软雅黑', 15))
extry.grid(row=0, column=1)
res = StringVar()
lable1 = Label(root, text='翻译结果：')
lable1.grid(row=1, column=0)
extry1 = Entry(root, font=('微软雅黑', 15), textvariable=res)
extry1.grid(row=1, column=1)


def translate():
    content = extry.get()
    content = content.strip()
    if content == '':
        messagebox.showinfo('提示', '请输入翻译内容')
    else:
        url = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule"
        data = {}
        data['i'] = content
        data['from'] = 'AUTO'
        data['to'] = 'AUTO'
        data['smartresult'] = 'dict'
        data['client'] = 'fanyideskweb'
        data['salt'] = '1538295833420'
        data['sign'] = '07'
        data['doctype'] = 'json'
        data['version'] = '2.1'
        data['keyfrom'] = 'fanyi.web'
        data['action'] = 'FY_BY_REALTIME'
        data['typoResult'] = 'false'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }
        result = requests.post(url, data, headers=headers)
        trans = result.json()
        tran = trans['translateResult'][0][0]['tgt']
        res.set(tran)


button = Button(root, text='点击翻译', width='10', command=translate)
button.grid(row=2, column=0, sticky=W)
exit_button = Button(root, text='退出键', width='10', command=root.quit)
exit_button.grid(row=2, column=1, sticky=E)
root.mainloop()
