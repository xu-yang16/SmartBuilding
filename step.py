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
    '''
    对(5,3)房间给100->80的阶跃信号，记录阶跃响应曲线。
    '''
    i = [(5, 3), (5, 4)]
    Interface.controlRoom(5, 3, 80)
    while True:
        try:
            for room in i:
                # 设定的温度, 当前温度, 当前开度, 当前时间
                t_set, t_now, kaidu_now, time_now = Interface.dataForPID(room[0], room[1])
                #写入文件
                with open("./step/state_in_{}_{}.txt".format(room[0],room[1]), "a") as f:
                    f.write("{}:{}:{}\t{}\t{}\t{}\t{}\t{}\n".format(time_now[0],time_now[1],time_now[2], room[0], room[1], t_set, t_now, kaidu_now))
                #打印输出
                print("{}:{}:{}\t{}\t{}\t{}\t{}\t{}\n".format(time_now[0],time_now[1],time_now[2], room[0], room[1], t_set, t_now, kaidu_now))
        except Exception as e:
            print("*********************读取温度数据出现错误...*******************")
        sleep(60)