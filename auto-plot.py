import os
import re
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import AutoDateLocator
import matplotlib.patches as patches
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
    return(name[2]+"_"+name[3] + ".png")

def myplot(txtName, indexList):
    all_df = []
    for index in indexList:
        # plot daily_temp_record
        df = pd.read_table(txtName + str(index) + ".txt", sep='[ |\t]', header=None, engine='python')
        columnNames = ['time', 'floor_id', 'room_id', 'set_tmp', 'real_tmp', 'real_var_open', 'var_open']
        df.columns = columnNames[0:df.shape[1]]
        df['time'] = pd.to_datetime(df['time'], format='%d:%H:%M:%S')
        all_df.append(df)

    # 配置时间坐标轴
    plt.figure()

    plt.subplot(2,1,1)
    for i, df in enumerate(all_df):
        index = indexList[i]
        plt.plot_date(df['time'], df['real_tmp'],linestyle="-",marker="None",label=str(index))
    # 坐标轴，标题设置
    plt.legend(bbox_to_anchor=(1.05, 0), loc=3, borderaxespad=0)
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
    
    for i, df in enumerate(all_df): # color='firebrick'
        index = indexList[i]
        plt.plot_date(df['time'], df['real_var_open'],linestyle="-",marker="None",label=str(index))
    # 坐标轴，标题设置
    plt.legend(bbox_to_anchor=(1.05, 0), loc=3, borderaxespad=0)
    plt.xlabel('Time',size=10)
    plt.ylabel('var_open',size=10)
    plt.title('Var_open record',size=10)
    plt.gcf().autofmt_xdate()  # 自动旋转日期标记
    plt.grid(True)
    plt.axis("tight")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M')) # 显示时间坐标的格式
    autodates = AutoDateLocator()# 时间间隔自动选取
    plt.gca().xaxis.set_major_locator(autodates)
    
    plt.savefig("./realtime_figure/"+fig_name(txtName),dpi=500,bbox_inches='tight')
    plt.close()

def auto_plot(txtNameList):
    while 1:
        #try:
        print("time:{}".format(time.strftime("%Y-%m-%d %H:%M:%S")))
        # False代表文件不存在; True代表文件存在
        flag = True
        for txtName, indexList in txtNameList:
            for index in indexList:
                if not(os.path.exists(txtName + str(index) + ".txt")):
                    print(txtName + str(index) + ".txt" + "不存在")
                    flag = False
                    break
            if flag:
                myplot(txtName, indexList)
                flag = True
        #except Exception as e:
        #    print("*********************Plot出现错误...*******************")
        sleep(600)


if __name__ == "__main__":
    txtNameList = [("./daily_temp_record/state_in_6_", [1,2,3,4,5]),
     ("./control_record/PID_50_5_15_room_5_", [1,2,3]),
      ("./floor_5_step/state_in_5_", [1])]
    auto_plot(txtNameList)
