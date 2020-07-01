import schedule
import time
from up_fan_rank import stat

schedule.every().minutes.do(stat,'fans')               # 每隔 10 分钟运行一次 job 函数
schedule.every().minutes.do(stat,'playNum')               # 每隔 10 分钟运行一次 job 函数
# schedule.every(10).minutes.do(stat,time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),'playNum')               # 每隔 10 分钟运行一次 job 函数
# # schedule.every().hour.do(job)                    # 每隔 1 小时运行一次 job 函数
# schedule.every().hour.do(stat,'fans')                        # 每隔 1 小时运行一次 job 函数
# schedule.every().hour.do(stat,'playNum')                    # 每隔 1 小时运行一次 job 函数
# schedule.every().day.at("22:30").do(stat,'fans')         # 每天在 10:30 时间点运行 job 函数
# schedule.every().day.at("22:30").do(stat,'fans')         # 每天在 10:30 时间点运行 job 函数
# schedule.every().day.at("22:30").do(stat,'playNum')         # 每天在 10:30 时间点运行 job 函数
# schedule.every().monday.do(job)                  # 每周一 运行一次 job 函数
# schedule.every().wednesday.at("13:15").do(job)   # 每周三 13：15 时间点运行 job 函数
# schedule.every().saturday.at("17:56").do(stat,time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),'playNum')     # 每周三 13：15 时间点运行 job 函数
# schedule.every().minute.at(":01").do(stat,time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),'playNum')        # 每分钟的 17 秒时间点运行 job 函数
# schedule.every().minute.at(":30").do(stat,time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),'fans')        # 每分钟的 17 秒时间点运行 job 函数

while True:
    schedule.run_pending()   # 运行所有可以运行的任务
    time.sleep(1)