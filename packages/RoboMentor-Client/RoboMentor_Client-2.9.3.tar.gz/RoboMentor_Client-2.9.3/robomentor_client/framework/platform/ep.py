import socket
import time

EP_IP_PORT: int = 40926
EP_CONN_PORT: int = 40923

class EP:

    def __init__(self):
        self.status = False
        self.scan_sock = None
        self.ep = []

    def scan_robot(self, count):
        for i in range(count):
            self.scan_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.scan_sock.bind(("0.0.0.0", EP_IP_PORT))
            robot, (ip, port) = self.scan_sock.recvfrom(1024)
            if ip not in self.ep:
                self.ep.append(ip)

        self.scan_sock.close()

        return self.ep
