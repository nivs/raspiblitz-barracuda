import smbus
import os
import time

# MAX17040G I2C address and registers
ADDR = 0x36
REG_VCELL = 0x02
REG_SOC = 0x04

bus = smbus.SMBus(1)

def read_capacity():
    # Read battery percentage (State of Charge)
    read = bus.read_word_data(ADDR, REG_SOC)
    swapped = ((read & 0xFF) << 8) | (read >> 8)
    return swapped / 256.0

while True:
    capacity = read_capacity()
    print(f"Battery Capacity: {capacity:.2f}%")
    
    if capacity <= 1.0:
        print("Low battery! Initiating safe shutdown...")
        os.system("sudo shutdown -h now")
        break
        
    time.sleep(60) # Check every minute
