'''
本程序用于读取6层所有房间一天内的温度变化曲线
'''
# -*- coding: utf-8 -*-
# ping 39.100.78.210
import sys
sys.path.append('../IoT')
import Interface
import time
from time import sleep

if __name__ == '__main__':
    TIME_FLAG = 0
    DAY = 0
    # 房间号
    i = [(6, 1, 100), (6, 2, 100), (6, 3, 100), (6, 4, 60), (6, 5, 60), (6, 6, 60), (6, 7, 30), (6, 8, 30), (6, 9, 30), (6, 10, 10), (6, 11, 10), (6, 12, 10)]
    for room in i:
        Interface.controlRoom(room[0], room[1], room[2])
    # 写入开度设置
    with open("./daily_temp_record/setting.txt", "a") as f:
        for room in i:
            f.write("time:{}\troom:{}\tkaidu:{}\n".format(time.strftime("%Y-%m-%d %H:%M:%S"), room[0:2], room[2]))
    while True:
        try:
            for room in i:
                #设定的温度, 当前温度, 当前开度
                t_set, t_now, kaidu_now, time_now = Interface.dataForPID(room[0], room[1])
                # 写入日期信息
                if(t_set[0] == 0 and TIME_FLAG == 0):
                    DAY = DAY + 1
                    TIME_FLAG = 1
                elif t_set[0] != 0:
                    TIME_FLAG = 0
                #写入文件
                with open("./daily_temp_record/state_in_{}_{}.txt".format(room[0],room[1]), "a") as f:
                    f.write("{}:{}:{}:{}\t{}\t{}\t{}\t{}\t{}\n".format(DAY,time_now[0],time_now[1],time_now[2], room[0], room[1], t_set, t_now, kaidu_now))
                #打印输出
                print("{}:{}:{}\t{}\t{}\t{}\t{}\t{}\n".format(time_now[0],time_now[1],time_now[2], room[0], room[1], t_set, t_now, kaidu_now))
        except Exception as e:
            print("*********************读取温度数据出现错误...*******************")
        sleep(60)