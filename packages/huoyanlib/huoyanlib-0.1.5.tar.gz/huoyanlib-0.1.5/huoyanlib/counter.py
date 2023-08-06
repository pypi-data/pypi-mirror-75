def counting(time):
    import time as t
    import os
    time = int(time)
    y = 1
    for i in range(1, time + 1):
        print(y)
        y += 1
        t.sleep(1)
        os.system('clear')

