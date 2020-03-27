import sys
sys.path.append('C:\\Users\\xuyang\\Desktop\\DSP2.0\\IoT')
import Interface


if __name__ == '__main__':
    print(Interface.dataForPID(1,1))
    Interface.controlRoom(1,1,90)