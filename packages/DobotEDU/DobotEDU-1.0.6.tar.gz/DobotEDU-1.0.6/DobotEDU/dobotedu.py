from aip import AipSpeech
from aip import AipNlp
from aip import AipImageClassify
from aip import AipOcr
from aip import AipFace
from DobotRPC import m1_api, magician_api, lite_api
import cv2
import sounddevice as sd
import soundfile as sf
import requests


class DobotEDU(object):
    def __init__(self, user_name: str, school_key: str):
        address = f"http://49.235.112.128:8052/{user_name}/{school_key}"
        json_result = eval(requests.get(address).content.decode())
        API_ID = f'{json_result[0]}'
        API_KEY = f'{json_result[1]}'
        SECRET_KEY = f'{json_result[2]}'

        api_id = API_ID
        api_key = API_KEY
        secret_key = SECRET_KEY

        self.__speech = AipSpeech(api_id, api_key, secret_key)
        self.__nlp = AipNlp(api_id, api_key, secret_key)
        self.__image_classify = AipImageClassify(api_id, api_key, secret_key)
        self.__ocr = AipOcr(api_id, api_key, secret_key)
        self.__face = AipFace(api_id, api_key, secret_key)

        self.__host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id='+api_key+'&client_secret='+SECRET_KEY

    @property
    def m1(self):
        return m1_api

    @property
    def magician(self):
        return magician_api

    @property
    def m_lite(self):
        return lite_api

    @property
    def speech(self):
        return self.__speech

    @property
    def nlp(self):
        return self.__nlp

    @property
    def image_classify(self):
        return self.__mage_classify

    @property
    def ocr(self):
        return self.__ocr

    @property
    def face(self):
        return self.__face

    def get_file_content(self, file_path):  # 读取照片文件

        with open(file_path, 'rb') as fp:
            return fp.read()

    def get_image(self, file_path, count_down, port, flip=False):  # count_down为拍照时间,port相机端口，flip是否水平翻转标志
        cap = cv2.VideoCapture(port, cv2.CAP_DSHOW)  # 用摄像头拍照
        t = count_down * 1000
        cnt = count_down
        # print("拍照倒计时....")
        while True:
            ret, frame = cap.read()  # 读取摄像头拍照的图片
            if flip:
                frame = cv2.flip(frame, 1)  # 左右翻转摄像头获取的照片
            cv2.imshow("video", frame)  # 显示照片
            c = cv2.waitKey(1)  # 显示的帧数
            if c == 27:
                break
            if t == 0:
                cv2.imwrite(file_path, frame)
                return
            if t % 1000 == 0:
                print(cnt)
                cnt = cnt - 1
            t = t - 20

    def record(self, file_name, count_down):

        RATE = 16000  # 采样率
        RECORD_SECONDS = count_down  # 录制时长Duration of recording
        print("录制开始...")
        myrecording = sd.rec(int(RECORD_SECONDS * RATE),
                             samplerate=RATE,
                             channels=1)
        sd.wait()  # 等到录制结束
        print("录制结束...")
        sf.write(file_name, myrecording, RATE, subtype='PCM_16')

    def conversation_robot(self, query, session_id):
        '''智能对话'''
        response = requests.get(self.__host)
        access_token = response.json()['access_token']
        url = 'https://aip.baidubce.com/rpc/2.0/unit/service/chat?access_token='+str(access_token)
        # 下面的log_id在真实应用中要自己生成，可是递增的数字
        log_id = '7758521'
        # 下面的user_id在真实应用中要是自己业务中的真实用户id、设备号、ip地址等，方便在日志分析中分析定位问题
        user_id = '222333'
        # 下面要替换成自己的s_id,是你的机器人ID
        s_id = 'S29652'
        post_data = "{\"log_id\":\""+log_id+"\",\"version\":\"2.0\",\"service_id\":\"" + s_id +\
                    "\",\"session_id\":\""+session_id+"\",\"request\":{\"query\":\""+query+"\",\"user_id\":\"" + user_id +\
                    "\"},\"dialog_state\":{\"contexts\":{\"SYS_REMEMBERED_SKILLS\":[\"1027488\",\"1027844\",\"1027543\",\"1027486\",\"1028485\"]}}}"
        headers = {'Content-Type': 'application/json'}
        r = requests.post(url, data=post_data.encode('utf-8'), headers=headers)
        ret = r.json()
        return ret
