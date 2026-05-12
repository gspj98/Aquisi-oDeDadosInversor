from machine import Pin, SPI
from time import ticks_ms, sleep_ms
import onewire
import ds18x20
import sdcard
import os

ds = Pin(4)
ds18 = ds18x20.DS18X20(onewire.OneWire(ds))
roms = ds18.scan()

spi=SPI(2)
sd=sdcard.SDCard(spi,Pin(2))
vfs=os.VfsFat(sd)
os.mount(sd,'/sd')
temperaturas = [];
taxa = 5000
id = 1

while True:
    
    if ticks_ms() >= taxa:
        id = 1
        ds18.convert_temp()
        for i in roms:
            print(f'T{id}: {ds18.read_temp(i)}')
            temperaturas.append(f'T{id}: {(ds18.read_temp(i))}')
            id += 1
        temperaturasCsv = ';'.join(temperaturas)
        print(temperaturasCsv)
        with open ("/sd/ds18_teste1.csv","a") as arq:
            arq.write(f'\n{temperaturasCsv}')
        temperaturas.clear()
        taxa = ticks_ms() + 1000



