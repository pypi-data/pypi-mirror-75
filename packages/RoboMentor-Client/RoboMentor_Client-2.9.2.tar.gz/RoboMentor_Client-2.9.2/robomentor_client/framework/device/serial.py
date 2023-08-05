import serial
from ..log import Log

class Serial:

    def __init__(self, port, baudrate, size):
        self.status = False

        try:
            self.conn = serial.Serial()
            self.conn.port = port
            self.conn.baudrate = baudrate
            self.conn.bytesize = size
            self.conn.stopbits = serial.STOPBITS_ONE
            self.conn.parity = serial.PARITY_NONE
            self.conn.timeout = 0.2
            self.conn.open()

            self.status = True
        except Exception as e:
            Log.error(str(e))
            return


    def write(self, command):
        if self.status:
            self.conn.write(command)

    def read(self):
        read_data = ""

        if self.status:
            read_data = self.conn.readall()

        return read_data.decode('utf-8')

    def close(self):
        if self.status:
            self.conn.close()