from TSL2561 import TSL2561
import time

def get_lux():
        tsl = TSL2561(0x39,"/dev/i2c-1")
        tsl.enable_autogain()
        tsl.set_time(0x00)
        
        return tsl.lux()