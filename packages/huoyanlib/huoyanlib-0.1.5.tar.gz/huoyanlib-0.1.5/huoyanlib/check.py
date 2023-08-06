import tkinter as tk
import webbrowser
import re

window = tk.Tk()
window.title('查询器')
window.geometry('500x300')

a = tk.Label(window, text='请在下面输入你要破译的作品网址')
a.pack()

b1 = tk.StringVar()
b = tk.Entry(window, textvariable=b1)
b.pack()


def checking():
    b2 = b1.get()
    d = re.findall(r"\d+", b2)
    d = ''.join(d)
    s = "http://code.xueersi.com/code/ide/code/" + d
    webbrowser.open(s)


c = tk.Button(window, text='破译', command=checking)
c.pack()


window.mainloop()
