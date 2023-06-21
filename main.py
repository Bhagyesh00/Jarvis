from time import sleep as s
from pyfirmata import Arduino, util  # for Serial Communication with Arduino
import random

board = Arduino("COM6") 

for i in range(100):

    board.digital[13].write(0)
    board.digital[12].write(1)
    s(0.2)
    board.digital[13].write(1)
    board.digital[12].write(0)
    s(0.2)
print("done")
