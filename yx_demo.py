import sys
sys.path.append('C:\\Users\\xuyang\\Desktop\\DSP2.0\\IoT')
# -*- coding: utf-8 -*-  
import Interface
import time
from time import sleep

if __name__ == '__main__':
    # 房间号
    i = [(5, 1)]
    Interface.controlRoom(5, 1, 10)
    while True:
        try:
            for room in i:
                value = Interface.dataForPID(room[0], room[1])
                t_set = value[0];  #设定的温度
                t_now = value[1];  #当前温度
                kaidu_now = value[2];   #当前开度
                date = time.strftime("%Y-%m-%d %H:%M:%S")
                localtime = time.time()
                #写入文件
                with open("state_in_{}_{}.txt".format(room[0],room[1]), "a") as f:
                    f.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(localtime, date, room[0], room[1], t_set, t_now, kaidu_now))
                #打印输出
                print(localtime, date, room, t_set, t_now, kaidu_now)
        except Exception as e:
            pass      
        sleep(20)