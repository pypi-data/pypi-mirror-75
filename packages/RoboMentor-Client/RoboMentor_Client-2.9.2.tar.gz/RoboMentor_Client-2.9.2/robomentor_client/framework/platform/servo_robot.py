import time
from ..device import Serial
from ..log import Log

class ServoRobot:

    def __init__(self, port):
        self.status = False
        self.conn = Serial(port, 115200, 8)
        self.foot_list = ["", "500", "500", "500", "500", "500", "500", "500", "500", "500", "500", "500", "500", "500", "500", "500", "500", "500", "500"]

    def write_format(self, servo_id, command, angle = None, t = None):
        buf = bytearray(b'\x55\x55')
        try:
            length = 3
            buf1 = bytearray(b'')

            if angle is not None:
                length += 2
                buf1.extend([(0xff & angle), (0xff & (angle >> 8))])
            if t is not None:
                length += 2
                buf1.extend([(0xff & t), (0xff & (t >> 8))])
            buf.extend([(0xff & servo_id), (0xff & length), (0xff & command)])
            buf.extend(buf1)

            count = 0x00
            for b in buf:
                count += b
            count = count - 0x55 - 0x55
            count = ~count
            buf.append(0xff & count)
            self.conn.write(buf)
        except Exception as e:
            Log.error(e)

    def command(self, servo_id, command, angle, t = 0):
        self.write_format(servo_id, command, angle, t)

    def debug(self, servo_id, angle, t = 0):
        self.command(servo_id, 1, int(angle), t)

    def start(self):
        self.foot_list[7] = 800
        self.foot_list[8] = 800
        self.foot_list[9] = 800
        self.foot_list[10] = 800
        self.foot_list[11] = 800
        self.foot_list[12] = 800
        self.foot_list[13] = 435
        self.foot_list[14] = 435
        self.foot_list[15] = 435
        self.foot_list[16] = 435
        self.foot_list[17] = 435
        self.foot_list[18] = 435

        for index, angle in enumerate(self.foot_list):
            if index > 0:
                self.command(index, 1, int(angle), 500)
                time.sleep(0.01)

    def stand_up(self):
        self.foot_list[7] = 700
        self.foot_list[8] = 700
        self.foot_list[9] = 700
        self.foot_list[10] = 700
        self.foot_list[11] = 700
        self.foot_list[12] = 700

        self.foot_list[13] = 350
        self.foot_list[14] = 350
        self.foot_list[15] = 350
        self.foot_list[16] = 350
        self.foot_list[17] = 350
        self.foot_list[18] = 350

        for index, angle in enumerate(self.foot_list):
            if index > 0:
                self.command(index, 1, int(angle), 500)
                time.sleep(0.01)

    def sit_down(self):
        self.foot_list[7] = 750
        self.foot_list[8] = 750
        self.foot_list[9] = 750
        self.foot_list[10] = 750
        self.foot_list[11] = 750
        self.foot_list[12] = 750
        for index, angle in enumerate(self.foot_list):
            if index > 0:
                self.command(index, 1, int(angle), 500)
                time.sleep(0.01)

    def forward(self):
        self.foot_list[8] = 800
        self.foot_list[14] = 550

        self.foot_list[9] = 800
        self.foot_list[15] = 400
        self.foot_list[3] = 450

        self.foot_list[12] = 800
        self.foot_list[18] = 400
        self.foot_list[6] = 650

        for index, angle in enumerate(self.foot_list):
            if index > 0:
                self.command(index, 1, int(angle), 300)
                time.sleep(0.01)

    def stand_step(self):
        while True:
            self.foot_list[7] = 800
            self.foot_list[10] = 800
            self.foot_list[11] = 800

            for index, angle in enumerate(self.foot_list):
                if index > 0:
                    self.command(index, 1, int(angle), 300)
                    time.sleep(0.01)

            time.sleep(0.5)

            self.foot_list[7] = 700
            self.foot_list[10] = 700
            self.foot_list[11] = 700

            self.foot_list[8] = 800
            self.foot_list[9] = 800
            self.foot_list[12] = 800

            for index, angle in enumerate(self.foot_list):
                if index > 0:
                    self.command(index, 1, int(angle), 300)
                    time.sleep(0.01)

            time.sleep(0.5)

            self.foot_list[8] = 700
            self.foot_list[9] = 700
            self.foot_list[12] = 700

    def twist_body(self):
        self.foot_list[8] = 800
