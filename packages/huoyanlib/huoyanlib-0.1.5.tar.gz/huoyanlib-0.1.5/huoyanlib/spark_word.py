colors = [31, 32, 33, 34, 35, 36, 37, 91, 92, 93, 94, 95, 96, 97]


def spark(word, times):
    import random
    import time
    import sys
    for i in range(times):
        print("\033[{}m{}".format(random.choice(colors), word))
        time.sleep(0.1)
        sys.stdout.write('\033[2J\033[00H')


def spark_2(word, times):
    from random import choice
    import time
    import sys
    word_2 = []
    for i in range(0, len(word)):
        word_2.append(word[i])
    word_3 = []
    for i in range(times):
        for iii in word_2:
            word_3.append('\033[{}m{}'.format(choice(colors), iii))
        for ii in word_3:
            print(ii, end='')
            time.sleep(0.1)
            sys.stdout.write('\033[2J\033[00H')
        print('\n')


spark_2('hello', 25)
