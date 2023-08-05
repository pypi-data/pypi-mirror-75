import requests

from .base import CallerBase
from ..config import Config
from ..entity.enums import QuestionType, QuestionMode, QuestionField
from ..entity.exception import BfEngineException


class IntentCaller(CallerBase):
    """
    QA api调用
    """
    def __init__(self, app_id):
        super().__init__(app_id)
        self.app_id = app_id
        self.module = 'qa'
        self.header = {
            "X-locale": "zh-cn",
            "app_id": app_id,
            "user_id": "bf-engine-sdk",
            "Authorization": "Bearer EMOTIBOTDEBUGGER",
            "Accept": "application/json,text/plain, */*"
        }
        self.predict_url                            = '{}:{}'.format(Config.base_url, Config.predict_port)
        self.predict_intent_url              = self.predict_url + "/predict"

    def predict(self, text: str,online: bool=False) -> list:
        """
        预测标准问
        :param text: 用户query
        :param online: 线上|线下
        :return 上传id
        """
        data =  {
            "Text":text,
            "Robot":self.app_id,
            "IsRelease": online
        }
        resp = requests.post(self.predict_intent_url, headers=self.header,json=data).json()

        # 问题$答案上传进度
        code = int(resp["code"])
        msg = str(resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        return resp["data"]
