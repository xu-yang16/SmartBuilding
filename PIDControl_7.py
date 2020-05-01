# -*- coding: utf-8 -*-
import sys
sys.path.append('../IoT')
import Interface
import time
from time import sleep


SET_TEMP = 22
def PIDControl(Kp, Ki, Kd, roomList):
    # 记录天数信息
    TIME_FLAG = 0
    DAY = 1
    # 文件名
    txtName = "./control_record_7/PID_room_"
    # 初始值
    t_set = SET_TEMP
    error_last = [0] * len(roomList)
    error_llast = [0] * len(roomList)
    val_open = [0] * len(roomList)
    for i, room in enumerate(roomList):
        _, t_now, kaidu_now, time_now = Interface.dataForPID(*room[0:2])
        error_last[i] = t_set - t_now
        error_llast[i] = error_last[i]
        val_open[i] = kaidu_now
    while True:
        try:
            for i, room in enumerate(roomList):
                # 设定的温度, 当前温度, 当前开度, 当前时间
                _, t_now, kaidu_now, time_now = Interface.dataForPID(*room[0:2])
                # 写入日期信息
                if time_now[0] == '0' and TIME_FLAG == 0:
                    DAY = DAY + 1
                    TIME_FLAG = 1
                elif time_now[0] != '0':
                    TIME_FLAG = 0
                #写入文件
                with open(txtName + "{}_{}.txt".format(*room[0:2]), "a") as f:
                    f.write("{}:{}:{}:{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(DAY,*time_now[0:3], *room[0:2], t_set, t_now, kaidu_now, val_open[i]))
                    #打印输出
                    print("{}:{}:{}:{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(DAY,*time_now[0:3], *room[0:2], t_set, t_now, kaidu_now, val_open[i]))
                
                # 执行温度控制的时间范围：8:00~18:00
                if int(time_now[0])>=0 and int(time_now[0])<=24:
                    # 控制律
                    error_now = t_set - t_now
                    if error_now >= 0.5:
                        val_open[i] = 0
                    elif error_now <= -0.5:
                        val_open[i] = 100
                    else:
                        print("new={:.2f}-{}*({:.2f}-{:.2f})-{}*{:.2f}-{}*({:.2f}-2*{:.2f}+{:.2f})={:.2f}\n".format(val_open[i],Kp,error_now,error_last[i],Ki,error_now,Kd,error_now,error_last[i],error_llast[i],val_open[i] - Kp * (error_now - error_last[i]) - Ki * error_now - Kd * (error_now - 2 * error_last[i] + error_llast[i])))
                        val_open[i] -= Kp * (error_now - error_last[i]) + Ki * error_now + Kd * (error_now - 2 * error_last[i] + error_llast[i])
                        error_llast[i] = error_last[i]
                        error_last[i] = error_now
                        
                        # 限制幅度
                        if val_open[i] >= 100:
                            val_open[i] = 100
                        elif val_open[i] <= 0:
                            val_open[i] = 0
                    Interface.controlRoom(*room[0:2], val_open[i])
        except Exception as e:
            print("*********************读取温度数据出现错误...*******************")
        sleep(60)
if __name__ == '__main__':
    roomList=[]
    for index in range(1, 16 + 1):
        roomList.append((7, index))
    
    # PID参数设置
    Kp = 50
    Ki = 10
    Kd = 15

    PIDControl(Kp, Ki, Kd, roomList)
    