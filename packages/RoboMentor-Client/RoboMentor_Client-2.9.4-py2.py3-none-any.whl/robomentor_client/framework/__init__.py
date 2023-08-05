import time
import sys
import json
import threading
from .log import Log
from .service import System, Requests, Message, Socket, Ai
from .device import Serial, GPIO, Camera
from .platform import EP, ServoRobot
from ..__config__ import __apiUrl__, __imUrl__, __version__

class Init:

    def __init__(self):
        Log.info("Robot " + __version__)

        self.auth_time = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
        self.version = str(__version__)
        self.app_id = str(sys.argv[1])
        self.app_secret = str(sys.argv[2])
        self.ip = System.get_host_ip()
        self.mac = System.get_mac_address()
        self.platform = System.get_platform()
        self.token = ""

        register_token_params = {"app_id": self.app_id, "app_secret": self.app_secret}
        register_token_headers = {
            "Content-Type": "application/json"
        }
        register_token = Requests.api(__apiUrl__ + "/oauth/access_token", register_token_params, register_token_headers, 'GET')
        register_token_json = register_token.json()
        if register_token_json["code"] != 0:
            Log.error("Robot AccessToken Error")
            sys.exit()

        self.access_token = register_token_json["data"]["access_token"]

        params = {"robot_mac": self.mac, "robot_ip": self.ip, "robot_platform": self.platform, "robot_version": __version__}
        headers = {
            "Content-Type": "application/json",
            "Mentor-Token": self.access_token
        }
        register = Requests.api(__apiUrl__ + "/oauth/robot/register", params, headers, 'GET')
        register_json = register.json()
        if register_json["code"] != 0:
            Log.error("Robot Init Error")
            sys.exit()

        self.token = str(register_json["data"]["token"])
        self.name = str(register_json["data"]["robot_title"])
        self.net_ip = str(register_json["data"]["robot_net_ip"])

        self.message = Message(__imUrl__, self.mac, self.app_id, self.app_secret).start()

        notice_data = {"message_type": "robot_run", "robot_run": {"type": "start_success"}}
        self.message.publish(json.dumps(notice_data))

        self.system_task_thread = threading.Thread(name="system_task_thread", target=self.system_task)
        self.system_task_thread.start()

    def system_task(self):
        while True:
            notice_data = {"message_type": "system_message", "system_message": {"time": time.strftime('%H:%M:%S', time.localtime(time.time())), "cpu": System.get_cpu_info(), "memory": System.get_memory_info()}}
            self.message.publish(json.dumps(notice_data))
            time.sleep(2)

