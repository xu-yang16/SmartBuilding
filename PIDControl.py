# -*- coding: utf-8 -*-
# ping 39.100.78.210
import sys
sys.path.append('../IoT')
import Interface
import time
from time import sleep


def PIDControl(Kp, Ki, Kd, i):
    # 记录天数信息
    TIME_FLAG = 0
    DAY = 1
    # 文件名
    txtName = "./control_record/PID_{}_{}_{}_room_".format(Kp, Ki, Kd)
    # 初始值
    t_set, t_now, kaidu_now, time_now = Interface.dataForPID(5, 3)
    t_set = 16.5
    error_last = t_now - t_set
    error_llast = error_last
    t_last = t_now
    var_open = kaidu_now
    while True:
        try:
            for room in i:
                # 设定的温度, 当前温度, 当前开度, 当前时间
                t_set, t_now, kaidu_now, time_now = Interface.dataForPID(*room[0:2])
                # 写入日期信息
                if time_now[0] == '0' and TIME_FLAG == 0:
                    DAY = DAY + 1
                    TIME_FLAG = 1
                elif time_now[0] != '0':
                    TIME_FLAG = 0
                # 设定温度为24度
                t_set = 24
                #写入文件
                with open(txtName + "{}_{}.txt".format(*room[0:2]), "a") as f:
                    f.write("{}:{}:{}:{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(DAY,*time_now[0:3], *room[0:2], t_set, t_now, kaidu_now, var_open))
                #打印输出
                print("{}:{}:{}:{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(DAY,*time_now[0:3], *room[0:2], t_set, t_now, kaidu_now, var_open))
                
                # 执行温度控制的时间范围：8:00~18:00
                if int(time_now[0])>=8 and int(time_now[0])<=18:
                    # 控制律
                    error_now = t_now - t_set
                    var_open = var_open + Kp * (error_now - error_last) + Ki * error_now + Kd * (error_now - 2 * error_last + error_llast)
                    error_llast = error_last
                    error_last = error_now
                    # 限制幅度
                    if var_open >= 100:
                        var_open = 100
                    elif var_open <= 0:
                        var_open = 0
                    Interface.controlRoom(*room[0:2], var_open)
        except Exception as e:
            print("*********************读取温度数据出现错误...*******************")
        sleep(60)
if __name__ == '__main__':
    i=[]
    for index in range(1, 16 + 1):
        i.append((5, index))
    
    # PID参数设置
    Kp = 50
    Ki = 5
    Kd = 15

    PIDControl(Kp, Ki, Kd, i)
    