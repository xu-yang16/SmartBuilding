# -*- coding: utf-8 -*-
# ping 39.100.78.210
import sys
sys.path.append('C:\\Users\\xuyang\\Desktop\\DSP2.0\\IoT')
import Interface
import time
from time import sleep
import datetime

if __name__ == '__main__':
    # flag=0标志着开度为70; flag=1标志着开度为80
    flag = 0
    # 开始记录的时间
    start_time = datetime.datetime.now()
    # 房间号
    i=[]
    for i in range(1, 16+1):
        i.append((5, i, 70))
    
    while True:
        try:
            # 设定开始阶跃的时刻
            passtime = datetime.datetime.now() - start_time
            if passtime.hours >= 5 and flag = 0:
                flag = 1
                # 对(5,3)房间给70->80的阶跃信号，记录阶跃响应曲线。
                i=[]
                for i in range(1, 16+1):
                    i.append((5, i, 80))
                for room in i: 
                        Interface.controlRoom(room[0], room[1], room[2])
                    # 写入开度设置
                    with open("./floor_5_step/setting.txt", "a") as f:
                        for room in i:
                            f.write("time:{}\troom:{}\tkaidu:{}\n".format(time.strftime("%Y-%m-%d %H:%M:%S"), room[0:2], room[2]))
            # 记录房间温度变化曲线
            for room in i:
                # 设定的温度, 当前温度, 当前开度, 当前时间
                t_set, t_now, kaidu_now, time_now = Interface.dataForPID(room[0], room[1])
                #写入文件
                with open("./floor_5_step/state_in_{}_{}.txt".format(room[0],room[1]), "a") as f:
                    f.write("{}:{}:{}\t{}\t{}\t{}\t{}\t{}\n".format(time_now[0],time_now[1],time_now[2], room[0], room[1], t_set, t_now, kaidu_now))
                #打印输出
                print("{}:{}:{}\t{}\t{}\t{}\t{}\t{}\n".format(time_now[0],time_now[1],time_now[2], room[0], room[1], t_set, t_now, kaidu_now))
        except Exception as e:
            print("*********************读取温度数据出现错误...*******************")
        sleep(60)