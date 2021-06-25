import os
import sys


# 将日期字符串20200101变成2020-01-01
def date_insert(src):
    src_list = list(src)

    src_list.insert(4, '-')
    src_list.insert(7, '-')
    dec = "".join(src_list)
    return dec


print(date_insert("20200101"))

# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):
    print("sys")
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)
    print("__file__")

print(application_path)
