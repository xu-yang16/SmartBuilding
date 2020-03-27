# -*- coding: utf-8 -*-
import sys
sys.path.append('C:\\Users\\xuyang\\Desktop\\DSP2.0\\IoT')
import Interface
import time
from time import sleep

if __name__ == '__main__':
    # 房间号
    i = [(5,1),(5,6),(5,10),(5,14),(5,9),(5,2),(5,3),(5,5),(5,7),(5,12)]
    j = -1
    for room in i:
        if j <= 7:
            j = j + 2
            Interface.controlRoom(room[0], room[1], j*10)
            with open("setting.txt", "a") as f:
                f.write("room:{} ,kaidu:{}\n".format(room,j*10))
    while True:
        for room in i:
            value = Interface.dataForPID(room[0],room[1])
            t_set = value[0];  #设定的温度
            t_now = value[1];  #当前温度
            kaidu_now = value[2];   #当前开度
            date = time.strftime("%Y-%m-%dY%H:%M:%S")
            localtime = time.time()
            #写入文件
            with open("state_in_{}_{}.txt".format(room[0],room[1]), "a") as f:
                f.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(localtime,date,room[0],room[1],t_set,t_now,kaidu_now))
            #打印输出
            print(localtime,date,room,t_set,t_now,kaidu_now)
        sleep(20)