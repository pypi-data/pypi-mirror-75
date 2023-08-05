import time
from .requests import Requests
from ...__config__ import __apiUrl__

class Ai:

    def __init__(self, common_token):
        self.access_token = ""
        self.common_token = common_token


    def get_access_token(self, ai_type, robot_token):

        params = {"type":ai_type,"token":robot_token}

        headers = {
            "Content-Type": "application/json",
            "Mentor-Token": self.common_token
        }

        access_token = Requests.api(__apiUrl__ + "/oauth/robot/ai/access_token", params, headers, 'GET')
        access_token_json = access_token.json()
        if access_token_json["code"] == 0:
            self.access_token = access_token_json["data"]["access_token"]

        return self.access_token

    def get_detect_face(self, image_data):

        api_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect?access_token=" + self.access_token

        params = {"image": image_data, "image_type": "BASE64", "face_field":"age,beauty,expression,face_shape,gender,glasses,landmark,landmark150,race,quality,eye_status,emotion,face_type,mask,spoofing"}

        headers = {
            "Content-Type": "application/json"
        }

        detect = Requests.api(api_url, params, headers, 'POST')

        detect_json = detect.json()

        return detect_json

    def get_detect_face_search(self, image_data, quality = "NONE", user_id = "", max_user_num = 1):

        api_url = "https://aip.baidubce.com/rest/2.0/face/v3/search?access_token=" + self.access_token

        params = {"image":image_data, "image_type":"BASE64", "group_id_list":self.app_id, "quality_control":quality, "user_id":user_id, "max_user_num":max_user_num}

        headers = {
            "Content-Type": "application/json"
        }

        detect = Requests.api(api_url, params, headers, 'POST')

        detect_json = detect.json()

        return detect_json

    def get_detect_body_attr(self, image_data):

        api_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/body_attr?access_token=" + self.access_token

        params = {"image": image_data}

        headers = {
            "Content-Type": "application/json"
        }

        detect = Requests.api(api_url, params, headers, 'POST')

        detect_json = detect.json()

        return detect_json

    def get_detect_body_num(self, image_data):

        api_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/body_num?access_token=" + self.access_token

        params = {"image": image_data}

        headers = {
            "Content-Type": "application/json"
        }

        detect = Requests.api(api_url, params, headers, 'POST')

        detect_json = detect.json()

        return detect_json

    def get_detect_body_gesture(self, image_data):
        api_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/gesture?access_token=" + self.access_token

        params = {"image": image_data}

        headers = {
            "Content-Type": "application/json"
        }

        detect = Requests.api(api_url, params, headers, 'POST')

        detect_json = detect.json()

        return detect_json

    def get_detect_object(self, api_url ,image_data):

        api_url = api_url + "?access_token=" + self.access_token

        params = {"image": image_data}

        headers = {
            "Content-Type": "application/json"
        }

        detect = Requests.api(api_url, params, headers, 'POST')

        detect_json = detect.json()

        return detect_json