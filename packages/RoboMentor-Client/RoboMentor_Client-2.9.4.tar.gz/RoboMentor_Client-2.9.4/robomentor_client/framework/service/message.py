import os
import json
import paho.mqtt.client as mqtt
from queue import Queue, PriorityQueue
from ..device import Serial

class Message:

    def __init__(self, host, client_id, username, password):
        self.host = host
        self.port = 1883
        self.client_id = client_id
        self.username = username
        self.password = password
        self.mqtt_client = None
        self.timeout = 60
        self.remote_message = Queue(100)

    def on_connect(self, client, userdata, flags, rc):
        self.subscribe("robot/" + self.client_id)

    def on_message(self, client, userdata, msg):
        message_data = json.loads(msg.payload)
        if message_data["message_type"] == "remote_message":
            self.remote_message.put(str(msg.payload, encoding="utf-8"))
        else:
            self.callback_robot_message(str(msg.payload, encoding="utf-8"))

    def read_remote_message(self):
        data = None
        if not self.remote_message.empty():
            data = self.remote_message.get()
        return data

    def subscribe(self, topic):
        self.mqtt_client.subscribe(topic, 0)

    def publish(self, blob):
        self.mqtt_client.publish("robot/" + self.client_id, blob)

    def start(self):
        if self.mqtt_client is None:
            self.mqtt_client = mqtt.Client("robot-" + self.client_id)
            self.mqtt_client.username_pw_set(self.username, self.password)
            self.mqtt_client.on_connect = self.on_connect
            self.mqtt_client.on_message = self.on_message
            self.mqtt_client.connect(self.host, self.port, self.timeout)
            self.mqtt_client.loop_start()
        return self

    def callback_robot_message(self, msg):
        robot_message_json = json.loads(msg)
        if robot_message_json["message_type"] == "robot_run":
            if robot_message_json["robot_run"]["type"] == "update":
                os.system("sudo cp /robot/RoboMentor_Client/robot.py /robot/RoboMentor_Client/robot.bak")
                robot_file = open("/robot/RoboMentor_Client/robot.py", 'w')
                robot_file.write(robot_message_json["robot_run"]["content"])
                robot_file.close()
                notice_data = {"message_type": "robot_run", "robot_run": {"type": "update_success"}}
                self.publish(json.dumps(notice_data))
            if robot_message_json["robot_run"]["type"] == "restart":
                robot_restart = os.popen("sudo sh /robot/RoboMentor_Client/robot_restart.sh " + self.username + " " + self.password).read()
                if robot_restart != "success":
                    notice_data = {"message_type": "robot_run", "robot_run": {"type": "start_error"}}
                    self.publish(json.dumps(notice_data))
        if robot_message_json["message_type"] == "serial_message":
            serial_conn = Serial(robot_message_json["serial_message"]["port"], int(robot_message_json["serial_message"]["rate"]), int(robot_message_json["serial_message"]["size"]))
            serial_conn.write(robot_message_json["serial_message"]["content"].encode('utf-8'))
            if robot_message_json["serial_message"]["switch"]:
                serial_data = serial_conn.read()
                notice_data = {"message_type": "serial_message_read", "serial_message_read": {"content": serial_data}}
                self.publish(json.dumps(notice_data))
        if robot_message_json["message_type"] == "pwm_message":
            serial_conn = Serial(robot_message_json["pwm_message"]["port"], int(robot_message_json["pwm_message"]["rate"]), int(robot_message_json["pwm_message"]["size"]))
            write_data = {"type": robot_message_json["pwm_message"]["type"], "channel": int(robot_message_json["pwm_message"]["channel"]), "width": robot_message_json["pwm_message"]["width"], "rate": int(robot_message_json["pwm_message"]["hz"])}
            serial_conn.write(json.dumps(write_data).encode('utf-8'))

    def stop(self):
        if self.mqtt_client is not None:
            self.mqtt_client.loop_stop()
            self.mqtt_client.disconnect()
            self.mqtt_client = None