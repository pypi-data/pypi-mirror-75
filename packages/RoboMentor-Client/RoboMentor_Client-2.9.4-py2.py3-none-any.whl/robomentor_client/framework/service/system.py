import socket
import re
import uuid
import platform
import psutil

class System:

    @staticmethod
    def get_host_ip():
        try:
            ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            ip.connect(('8.8.8.8', 80))
            ip_adds = ip.getsockname()[0]
        finally:
            ip.close()
        return ip_adds

    @staticmethod
    def get_mac_address():
        return ":".join(re.findall(r".{2}", uuid.uuid1().hex[-12:]))

    @staticmethod
    def get_platform():
        return platform.system() + " " + platform.machine()

    @staticmethod
    def get_cpu_info():
        return psutil.cpu_percent(interval=1)

    @staticmethod
    def get_memory_info():
        virtual_memory = psutil.virtual_memory()
        return virtual_memory.percent