import sys
sys.path.append('../IoT')
import Interface
import time
from time import sleep


def test():
    t_set, t_now, kaidu_now, time_now = Interface.dataForPID(6, 1)
    print(time_now[0]=='0')

if __name__ == "__main__":
    test()