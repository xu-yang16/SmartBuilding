# -*- coding: utf-8 -*-
# ping 39.100.78.210
import sys
sys.path.append('C:\\Users\\xuyang\\Desktop\\DSP2.0\\IoT')
import Interface
import time
from time import sleep

if __name__ == '__main__':
    # 房间号
    i = [(5, 1, 60), (5, 3, 60), (5, 5, 60), (5, 6, 60), (5, 7, 60), (5, 9, 60), (5, 12, 60)]
    # i = [(5, 5, 100)]
    '''
    for room in i:
        Interface.controlRoom(room[0], room[1], room[2])
    # 写入开度设置
    with open("setting.txt", "a") as f:
        f.write("******************Time: {}********************\n".format(time.strftime("%Y-%m-%d %H:%M:%S")))
        for room in i:
            f.write("room: {}, kaidu: {}\n".format(room[0:2], room[2]))
    '''
    while True:
        try:
            for room in i:
                #设定的温度, 当前温度, 当前开度
                t_set, t_now, kaidu_now = Interface.dataForPID(room[0], room[1])
                date = time.strftime("%Y-%m-%d %H:%M:%S")
                localtime = time.time()
                #写入文件
                with open("state_in_{}_{}.txt".format(room[0],room[1]), "a") as f:
                    f.write("{:.7f}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(localtime, date, room[0], room[1], t_set, t_now, kaidu_now))
                #打印输出
                print(localtime, date, room, t_set, t_now, kaidu_now)
        except Exception as e:
            print("*********************读取温度数据出现错误...*******************")
        sleep(30)