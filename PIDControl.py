# -*- coding: utf-8 -*-
# ping 39.100.78.210
import sys
sys.path.append('C:\\Users\\xuyang\\Desktop\\DSP2.0\\IoT')
import Interface
import time
from time import sleep

Kp = 20
Ki = 10
Kd = 0
if __name__ == '__main__':
    # 房间号
    # i = [(5, 1, 60), (5, 3, 60), (5, 5, 60), (5, 6, 60), (5, 7, 60), (5, 9, 60), (5, 12, 60)]
    i = [(5, 1)]
    error_sum = 0
    # 初始值
    t_set, t_now, kaidu_now, time_now = Interface.dataForPID(5, 1)
    t_set = 19.5
    var_open = Kp * (t_now - t_set) + 60
    if var_open >= 100:
        var_open = 100
    elif var_open <= 60:
        var_open = 60
    t_last = t_now
    while True:
        try:
            for room in i:
                # 设定的温度, 当前温度, 当前开度, 当前时间
                t_set, t_now, kaidu_now, time_now = Interface.dataForPID(room[0], room[1])
                date = time.strftime("%Y-%m-%d %H:%M:%S")
                #写入文件
                with open("state_in_{}_{}.txt".format(room[0],room[1]), "a") as f:
                    f.write("{}:{}:{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(time_now[0],time_now[1],time_now[2], room[0], room[1], t_set, t_now, kaidu_now, var_open))
                #打印输出
                print("{}:{}:{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(time_now[0],time_now[1],time_now[2], room[0], room[1], t_set, t_now, kaidu_now, var_open))
                
                # 控制律
                t_set = 19.5
                var_open = var_open + Kp * (t_now - t_last) + Ki * (t_now - t_set) + Kd * (t_now - t_last)
                t_last = t_now
                if var_open >= 100:
                    var_open = 100
                elif var_open <= 60:
                    var_open = 60
                Interface.controlRoom(room[0], room[1], var_open)
                '''
                # 写入开度设置
                with open("setting.txt", "a") as f:
                    f.write("******************Time: {}********************\n".format(time.strftime("%Y-%m-%d %H:%M:%S")))
                    f.write("room: {}, t_set: {}, kaidu: {}\n".format(room[0:2], t_set, var_open))
                '''
        except Exception as e:
            print("*********************读取温度数据出现错误...*******************")
        sleep(60)