import os
import re
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import AutoDateLocator
from datetime import datetime
import time
from time import sleep
plt.style.use('ggplot')

def get_dir(path):  # 获取目录路径
        print("所有目录路径是：")
        for root, dirs, files in os.walk(path):  # 遍历path及每个目录，有3个参数，root表示目录路径，dirs表示当前目录的目录名，files代表当前目录的文件名
            for dir in dirs:
                if ".git" not in os.path.join(root, dir):
                    print(dir)
# 输出当前目录非git的文件夹name
# get_dir("./")

def fig_name(txtName):
    name = re.split('/|\.', txtName)
    return(name[2]+"_"+name[3]+".png")

def myplot(txtName):
    # plot daily_temp_record
    df = pd.read_table(txtName, sep='[ |\t]', header=None, engine='python')
    df.columns = ['time', 'floor_id', 'room_id', 'set_tmp', 'real_tmp', 'var_open']
    df['time'] = pd.to_datetime(df['time'], format='%d:%H:%M:%S')
    '''
    fig = plt.figure()
    ax1 = fig.add_subplot(2,1,1)
    ax2 = fig.add_subplot(2,1,2)

    df.plot(ax=ax1, x='time', y='real_tmp', grid=True, legend=False, color='r')
    df.plot(ax=ax2, x='time', y='var_open', grid=True, legend=False,color='b')
    plt.savefig('test.png')
    '''
    # 配置时间坐标轴
    plt.figure()
    

    plt.subplot(2,1,1)
    plt.plot_date(df['time'], df['real_tmp'],linestyle="-",marker="None",color='indigo')
    # 坐标轴，标题设置
    plt.xticks([])
    plt.ylabel('Temperature',size=10)
    plt.title('Temperature record',size=10)
    plt.gcf().autofmt_xdate()  # 自动旋转日期标记
    plt.grid(True)
    plt.axis("tight")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M')) # 显示时间坐标的格式
    autodates = AutoDateLocator()# 时间间隔自动选取
    plt.gca().xaxis.set_major_locator(autodates)

    plt.subplot(2,1,2)
    plt.plot_date(df['time'], df['var_open'],linestyle="-",marker="None",color='firebrick')
    # 坐标轴，标题设置
    plt.xlabel('Time',size=10)
    plt.ylabel('var_open',size=10)
    plt.title('Var_open record',size=10)
    plt.gcf().autofmt_xdate()  # 自动旋转日期标记
    plt.grid(True)
    plt.axis("tight")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M')) # 显示时间坐标的格式
    autodates = AutoDateLocator()# 时间间隔自动选取
    plt.gca().xaxis.set_major_locator(autodates)
    
    
    plt.savefig("./realtime_figure/"+fig_name(txtName),dpi=500)
    plt.show()
    #'''

def auto_plot(txtNameList):
    while 1:
        try:
            print("time:{}\n".format(time.strftime("%Y-%m-%d %H:%M:%S")))
            for txtName in txtNameList:
                if not(os.path.exists(txtName)):
                    continue
                myplot(txtName)
        except Exception as e:
            print("*********************Plot出现错误...*******************")
        sleep(600)


if __name__ == "__main__":
    txtNameList = ["./daily_temp_record/state_in_6_1.txt","./control_record/PID_50_5_15_room_5_1.txt", "./floor_5_step/state_in_5_1.txt"]
    auto_plot(txtNameList)
