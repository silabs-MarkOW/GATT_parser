import time

bs = b'\x00\xd8_\x00\xfd'
bs = b'\x02\xd8_\x00\xfd\xe7\x07\x05\x03\x10\x11\x23'

def decode_medfloat32(bytestr) :
    mantissa = int.from_bytes(bytestr[:3],'little',signed=True)
    exponent = int.from_bytes(bytestr[3:],'little',signed=True)
    numstr = '%de%d'%(mantissa,exponent) # side step issue of math libraries
    return float(numstr)                 # with ugly trick

def decode_dataTime(bytestr) :
    year = int.from_bytes(bytestr[:2],'little')
    month = bytestr[2]
    mday = bytestr[3]
    hours = bytestr[4]
    minutes = bytestr[5]
    seconds = bytestr[6]
    ## this ignores DST and timezones
    return time.mktime((year,month,mday,hours,minutes,seconds,0,0,0))
    
def dump_temperature_measurement(bytestr) :
    flags = bytestr[0]
    bytestr = bytestr[1:]
    isFahrenheit = 0 != (flags & 1)
    timeStampPresent = 0 != (flags & 2)
    temperatureTypePresent = 0 != (flags & 4)
    if 0 != (flags & 0xf8) :
        raise RuntimeError('Reserved bit set in flag: 0x%02x'%(flags & 0xf8))
    temperature = decode_medfloat32(bytestr[:4])
    bytestr = bytestr[4:]
    if timeStampPresent :
        unixtime = decode_dataTime(bytestr[:7])
        bytestr = bytestr[7:]
    if temperatureTypePresent :
        bytestr = bytestr[1:]
        raise RuntimeError('Decoding temperature type not implemented')
    if len(bytestr) > 0 :
        raise RuntimeError('trailing data found: "%s"'%(bytestr.__str__()))
    if isFahrenheit :
        unit = '&deg;F'
    else :
        unit = 'C'
    print('Temperature: %f %s'%(temperature,unit))
    if timeStampPresent :
        print('Timestamp: %s'%(time.ctime(unixtime)))
    
dump_temperature_measurement(bs)
