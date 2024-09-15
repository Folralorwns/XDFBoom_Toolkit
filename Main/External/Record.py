import time

def record_time(flag):
    if flag == 0:
        global t0
        t0 = time.time()
    else:
        t1 = time.time()
        print("程序结束，运行时间：%.2fs" % (t1 - t0))
    print(time.strftime('程序开始/结束时间%Y-%m-%d %H:%M:%S', time.localtime(time.time())))