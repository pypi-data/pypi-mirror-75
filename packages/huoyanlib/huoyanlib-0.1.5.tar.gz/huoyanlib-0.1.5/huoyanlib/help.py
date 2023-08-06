def help(name):
    """
    大家有没有觉得系统自带的help函数输出的东西你都看不懂呢？
    那就来试试这个函数吧！我把所有讲解都换成了中文！
    """
    unused = [
        'callable',
        'chr',
        'compile',
        'copyright',
        'credits',
        'dir',

    ]

    if name == 'abs':
        print("常用形参数：1（int类型）\n翻译：就是返回绝对值")
    elif name == 'all':
        print("常用形参数：1（可迭代对象，也就是说可以是元组或列表）\n翻译：如果bool(x)对迭代中的所有值x都为真，则返回True。")
        print("（如果列表是空的，会返回True）")
    elif name == 'any':
        print("常用形参数：1（可迭代对象，也就是说可以是元组或列表）\n翻译：如果bool(x)对迭代中的任何x都为真，则返回True。")
        print("（如果列表是空的，会返回False）")
    elif name == 'ascii':
        print("常用形参数：1（任何类型）\n翻译：返回对象的纯ascii表示形式。")
        print("它的前身是Python2里面的repr()")
    elif name == 'bin':
        print("常用形参数：1（int类型）\n翻译：返回整数的二进制表达形式")
    elif name == 'breakpoint':
        print("常用形参数：1（任何类型）\n翻译：这个函数调用了sys.breakpointthook()")
        print("Breakpointhook()必须接受传递的任何参数。默认情况下，这会将您放入pdb调试器。")
    elif name == 'credits':
        print("没有形参，没有用处，就是一个声明，调用后会输出以下内容：")
        print("Thanks to CWI, CNRI, BeOpen.com, Zope Corporation and a cast of thousands")
        print("for supporting Python development.  See www.python.org for more information.")
    elif name == 'delattr':
        print("形参数：2（一个是列表名，第二个是元素名\n翻译：从给定对象中删除命名属性。 Delattr (x，‘ y’)等价于“ del x.y”")
    elif name == 'divmod':
        print('形参数：2（都是int类型）\n翻译：divmod(x, y)返回一个元组，两个元素分别是x÷y的商（整数）和余数')
    elif name == 'eval':
        print('这个函数被大家吹的神乎其神，其实并不厉害，只是把传给他的参数尝试转换为Python代码')
    elif name == 'exec':
        print('跟eval函数类似，没什么好解释的')
    elif name == 'exit':
        print('不接受参数，作用就是直接停止程序')
    elif name == 'format':
        print('接收形参数：无数，主要作用就是编辑字符串')
    elif name == 'getatter':
        print('获取属性值')
    elif name == 'globals':
        print("返回全局变量的字典")
    elif name == 'hasattr':
        print("hasattr(x, y)检查对象x有没有对象y，如果对象有该属性返回True，否则返回False")
    elif name == 'hash':
        print("返回对象的哈希值（别问我哈希值是什么，他解释太长了，自己查去）")
    elif name == 'help':
        print("这个原版的help函数返回一个函数的功能（英文的），所以建议你们使用我这个库【滑稽】")
    elif name == 'hex':
        print("返回整数的16进制表达形式")
