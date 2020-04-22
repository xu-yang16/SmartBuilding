import os
import sys
sys.path.append('../IoT')
import Interface
import time
from time import sleep


def get_dir(path):  # 获取目录路径
        print("所有目录路径是：")
        for root, dirs, files in os.walk(path):
            for file in files:
                print(os.path.join(path,file))

if __name__ == "__main__":
    roomList=[]
    for index in range(1, 3 + 1):
        roomList.append((5, index))
    for i, room in enumerate(roomList):
        print("{}th:{}".format(i,room))