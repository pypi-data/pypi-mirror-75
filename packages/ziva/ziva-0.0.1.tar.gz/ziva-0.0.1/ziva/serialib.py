from time import sleep

from serial.tools import list_ports
import serial
import logging

logger = logging.getLogger()

def comports():
    """Lists available comports"""
    available_ports = []
    ports = list_ports.comports()
    for port in ports:
        available_ports.append(str(port))
    return available_ports

def serial_ports():
    """Filter serial ports from all comports"""
    ports = comports()
    ser_ports = list(filter(lambda x: 'Serial Port' in x, ports))
    return ser_ports

def autodetermine_port():
    """Auto select first serial port"""
    ser_ports = serial_ports()
    if ser_ports:
        return serial_ports()[0].split(' - ')[0]

class SerialComm(object):
    def __init__(self):
        pass
    def open(self, port:str, baudrate=38400, timeout=0.1):
        """Connect to serial port
        serial.serialutil.SerialException is thrown if connection can't be established.
        """
        self.n_retry = 3
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        for i in range(self.n_retry):
            try:
                self.ser = serial.Serial(
                    port=port,
                    baudrate=baudrate,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=timeout
                )
                self.ser.flushInput()
            except Exception as e:
                logger.error(f"Failed to open serial port:{port}")
                sleep(1)
            else:
                logger.debug(f"Serial port opened:{port}, baud:{baudrate}")
                break


    def __close(self):
        self.ser.close()

    def reopen_port(self):
        """Reopen serial port. This is sometimes necessary if it stops working."""
        self.__close()
        self.open(port=self.port, baudrate=self.baudrate, timeout=self.timeout)

    def write(self, data:bytes = None):
        """
        Write bytes to serial port
        """
        if not data:
            raise ValueError('No bytes to send')

        logger.debug(f"Data sent: {data}")
        if data:
            # self.ser.flush()
            self.ser.write(data)

    def readline(self):
        line = self.ser.readline()
        return line

    def read(self, to_string=True, last_char=b'\x83'):
        """Read from serial 1 byte at a time. Stop when last_char is received."""

        frame = b""
        while True:
            byte = self.ser.read(1)
            if byte:
                frame += byte
                if byte == last_char:
                    break
            else:
                break
        logger.debug(f"Data received: {frame}")
        # if to_string:
        #     frame = ''.join(chr(i) for i in frame)
        return frame

if __name__ == '__main__':
    #print ("Available comports:", comports())
    print ("Available serial ports:", serial_ports())
