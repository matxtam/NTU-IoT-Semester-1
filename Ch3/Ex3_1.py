#!/usr/bin/env python

import sys
import serial
import threading
import time
from queue import Queue

### Receive readings of photo interrupter
class RxThread(threading.Thread):
    def __init__(self, ser, queue):
        threading.Thread.__init__(self)
        self.ser = ser
        self.sig_temp = 1
        self.count = 0
        self._running = True
        self.freq = queue
        self.freq.put(0)
        self.period = 0
        
    def run(self):
        freq = 0
        tStart = time.time()
        while self._running:
            while self._running and self.ser.inWaiting():
                ## read from the serial port
                sig = ""
                try:
                    sig = self.ser.readline().decode('utf8')[:-2]
                except:
                    pass
                
                # if signal changed from 0 to 1, count++ 
                if self.sig_temp == '0' and sig == '1':
                    self.count+=1
                
                ## Timing setups
                tEnd = time.time()
                self.period = float(tEnd - tStart)
                if self.period > 0.3: # resets every 0.3 seconds
                    freq = (self.count/2)/self.period
                    self.freq.put(freq)
                    self.count = 0
                    tStart = time.time()
                self.sig_temp = sig
                
    def resume(self):
        self._running = True
        
    def stop(self):
        self._running = False
        self.ser.close()

### Transmit pwm of motor
class TxThread(threading.Thread):
    def __init__(self, ser, queue):
        threading.Thread.__init__(self)
        self.ser = ser
        self.freq_target = 0
        self.freq_now = 0
        self.freq = queue
        self._running = True
        
    def run(self):
        pwm = 0
        while self._running:
            ## print the frequency
            if not self.freq.empty():
                self.freq_now = self.freq.get() 
                sys.stdout.flush()
                sys.stdout.write("\r{:^10} {:^10}".format(self.freq_target,round(self.freq_now,2)))
            else:
                pass

            ## pwm +- 1 to match target frequency
            if self.freq_target - self.freq_now > 1:
                if pwm < 255:
                    pwm += 1
                trans = str(pwm)+'o'
                self.ser.write(trans.encode())
                time.sleep(0.1)
            elif self.freq_now - self.freq_target > 1:
                if pwm > 0:
                    pwm -= 1
                trans = str(pwm)+'o'
                self.ser.write(trans.encode())
                time.sleep(0.1)
            else:
                pass

    def resume(self):
        self._running = True

    def stop(self):
        self._running = False
        self.ser.close()

def main():
    print('input rps or q for quit: ')
    print('{:^10} {:^10} {:^10}'.format('target','current','input'))
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout= 0.5 ) #RPi serial port
    
    ### frequency data queue
    # frequency is calculated from the reading of photo-interrupter (RX thread),
    # and is used to tune pwm commands to the fan (TX thread)
    queue = Queue()

    ### Communication with Arduino Uno
    # use thread for simultaneous work
    rx = RxThread(ser, queue)
    tx = TxThread(ser, queue)
    rx.start()
    tx.start()
    

    while True:
        input_temp = input()
        
        if input_temp == 'q':
            rx.stop()
            tx.stop()
            ser.close()
            break
        try:
            tx.freq_target = float(input_temp)
        except:
            break

if __name__=='__main__':
    main()
