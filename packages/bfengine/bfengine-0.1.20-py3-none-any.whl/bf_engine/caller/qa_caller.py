import requests

from .base import CallerBase
from ..config import Config
from ..entity.enums import QuestionType, QuestionMode, QuestionField
from ..entity.exception import BfEngineException


class QACaller(CallerBase):
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
        self.dac_url                            = '{}:{}'.format(Config.base_url, Config.ssm_port)
        self.upload_faq_upload_url              = self.dac_url + "/ssm/dac/upload"
        self.upload_faq_upload_status_url       = self.dac_url + "/ssm/dac/upload/"
        self.upload_faq_train_url               = self.dac_url + "/ssm/dac/train"
        self.upload_faq_train_status_url        = self.dac_url + "/ssm/dac/trainhistory"
        self.upload_faq_json_sq_url             = self.dac_url + "/ssm/dac/sq"
        self.upload_faq_json_lq_url             = self.dac_url + "/ssm/dac/lq"
        self.upload_faq_json_publish_url        = self.dac_url + "/ssm/dac/release/online"
        self.upload_faq_json_publish_status_url = self.dac_url + "/ssm/dac/release/progress"
        self.upload_faq_json_publish_status_url = self.dac_url + "/ssm/dac/release/progress"
        self.upload_faq_json_tag_url            = self.dac_url + "/ssm/dac/tag"
        self.download_faq_download_url          = self.dac_url + "/ssm/dac/download"
        self.download_faq_download_export_url   = self.dac_url + "/ssm/dac/common/minio/excelfile"
        self.search_faq_json_question_list_url  = self.dac_url + "/ssm/dac/info"
        self.search_faq_json_corpus_list_url    = self.dac_url + "/ssm/dac/lq"
        self.search_faq_json_related_sq_list_url= self.dac_url + "/ssm/dac/sq/related_candidate"

    def upload(self, data_type: QuestionType, data_model: QuestionMode, file_path: str) -> str:
        """
        上传标注问/语料
        :param data_type: 上传类型 (SQ_ANS|LQ|TQ)
        :param data_model: 上传模型 (全量|增量)
        :param file_path: 上传文件路径
        :return 上传id
        """
        # 上传问题$答案
        files = {"file": (self.app_id + ".xlsx", open(file_path, 'rb'))}
        data = {"type": data_type, "mode": data_model, "comment": "BFEngine 导入 qa"}
        resp = requests.request("POST", self.upload_faq_upload_url, headers=self.header, data=data, files=files).json()

        # 问题$答案上传进度
        code = int(resp["code"])
        msg = str(resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        return str(resp["data"])


    def upload_status(self, data_id: str, is_log: bool = True) -> int:
        """
        查询上传状态
        :param is_log: 是否打日志
        :param data_id: 上传id
        :return 上传进度
        """
        resp = requests.get(self.upload_faq_upload_status_url + "/" + data_id, headers=self.header, json={}).json()
        code = int(resp["code"])
        msg = str(resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        progress = resp["data"]["progress"]
        # if is_log:
        #     log.info(self.module + ": 上传进度==" + str(progress) + "%")
        return progress

    def download_launch(self, data_type: QuestionType)-> str:
        """
        发起导出标注问/语料
        :param data_type: 下载类型 (SQ_ANS|LQ|TQ)
        :param file_path: 下载文件路径
        :return 服务器文件下载路径
        """
        resp = requests.get(self.download_faq_download_url + "?type=" + data_type, headers=self.header, json={}).json()
        code = int(resp["code"])
        msg = str(resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        return resp["data"]
    def download(self,file_path: str, service_file_path: str, is_log: bool = True):
        """
        从服务获取文件
        :param is_log: 是否打日志
        :param file_path: 本地文件保存路径
        :param data_path: 服务文件路径
        :return 上传进度
        """
        resp = requests.get(self.download_faq_download_export_url + "?filename=" + service_file_path,stream=True)
        with open(file_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=512):
                f.write(chunk)
    def upload_json_sq(self, data: dict) -> str:
        """
        上传标准问
        :param data: 上传数据
        :return id
        """
        tag_id_list = []
        if "tags" in data.keys():
            temps = self._tags_add(data["tags"])
            for temp in temps:
                tag_id_list.append(temp)
        related_sq_id_list = []
        if "related" in data.keys():
            temps = self._related_sq_search(data["related"])
            for temp in temps:
                related_sq_id_list.append(temp["id"])
        data = {
            "sq": data["sq"],
            "category_id": -1,
            "tag_id_list": tag_id_list,
            "answers": data["answers"] if "answers" in data.keys() else [
                {
                    "answer": data["answer"],
                    "property": {
                        "dimension_id_list": []
                    },
                    "start_time": "",
                    "end_time": "",
                    "period_type": 0,
                    "related_sq_id_list": related_sq_id_list
                }
            ]
        }
        resp = requests.post(self.upload_faq_json_sq_url, headers=self.header, json=data).json()
        code = int(resp["code"])
        msg = str(resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        return resp["data"]["id"]

    def upload_json_lq(self, data_id: str, data: dict) -> bool:
        """
        上传标准问
        :param data_id: 上传id
        :return 上传进度
        """
        data = {
            "records": [
                {
                    "sq_id": data_id,
                    "lq_list": list(map(lambda lq: {'lq': lq}, data["lq"]))
                }
            ]
        }
        resp = requests.post(self.upload_faq_json_lq_url, headers=self.header, json=data).json()
        code = int(resp["code"])
        msg = str(resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        return True
    def train(self):
        """
        训练标准问题
        :return 训练id
        """
        resp = requests.get(self.upload_faq_train_url, headers=self.header, json={}).json()
        code = int(resp["code"])
        msg = str(resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        return str(resp["data"])

    def train_status(self, train_id):
        """
        查询训练状态
        :param train_id: 训练id
        :return 训练进度
        """
        resp = requests.get(self.upload_faq_train_status_url + "/" + train_id, headers=self.header, json={}).json()
        code = int(resp["code"])
        msg = str(resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        progress = resp["data"]["progress"]
        # log.info(self.module + ": training..." + str(progress) + "%")
        return progress

    def publish(self):
        """
        开始发布
        :return 发布id
        """
        resp = requests.get(self.upload_faq_json_publish_url, headers=self.header, json={}).json()
        code = int(resp["code"])
        msg = str(resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        return str(resp["data"])
    def publish_status(self,publish_id) -> int:
        """
        查询发布状态
        :param publish_id: 发布id
        :return 发布进度
        """
        resp = requests.get(self.upload_faq_json_publish_status_url + "/" + publish_id, headers=self.header, json={}).json()
        code = int(resp["code"])
        msg = str(resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        progress = int(resp["data"])
        return progress
    def qa_tag_add(self,name:str=None):
        """
        添加qa标签
        :param name 标签名称
        :return 标签ID
        """
        data = {"name": name}
        resp = requests.post(self.upload_faq_json_tag_url, headers=self.header,
                            json=data).json()
        code = int(resp["code"])
        msg = str(resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        return resp["data"]["id"]

    def qa_tag_list(self):
        """
        获取标签列表
        :return 标签列表
        """
        resp = requests.get(self.upload_faq_json_tag_url, headers=self.header,
                             json={}).json()
        code = int(resp["code"])
        msg = str(resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        return resp["data"]
    def qa_list(self,field: QuestionField):
        data = self.sq_list(field)
        for item in data:
            corpus = self.lq_list(str(item["id"]))
            item["corpus"]=corpus
        return data
    def sq_list(self,field: QuestionField):
        """
        标准问列表查询
        :return 标准问列表
        """
        data = {"search":[{"keyword":"","field":str(field)}]}
        resp = requests.post(self.search_faq_json_question_list_url, headers=self.header,json=data).json()
        code = int(resp["code"])
        msg = str(resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        return resp["data"]
    def lq_list(self,qa_id:str):
        """
        查询标准问下语料
        :return 语料列表
        """
        resp = requests.get(self.search_faq_json_corpus_list_url + "/" + qa_id, headers=self.header,
                            json={}).json()
        code = int(resp["code"])
        msg = str(resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        return resp["data"]["list"]

    def _related_sq_search(self,relates):
        """
        获取相关问列表
        :return 语料列表
        """
        related_list = []
        resp = requests.get(self.search_faq_json_related_sq_list_url, headers=self.header,
                            json={}).json()
        code = int(resp["code"])
        msg = str(resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        data_list = resp["data"]
        for data in data_list:
            if data["content"] in relates:
                related_list.append(data)
        return related_list


    def _tags_add(self,tags):
        """
        添加标签集
        :return 返回添加后的标签ID集
        """
        tag_ids = []
        exist_tag_name_list = [] #已存在标签名称
        tmp = list(set(tags))
        for tag in tmp:
            try:
                tag_ids.append(self.qa_tag_add(tag))
            except BfEngineException as bfe:
                exist_tag_name_list.append(tag)
        exist_tag_list = self._qa_tag_search(exist_tag_name_list)
        for exist_tag in exist_tag_list:
            if "id" in exist_tag.keys():
                tag_ids.append(exist_tag["id"])
        return tag_ids
    def _qa_tag_search(self, tags):
        """
        查询已经存在标签的IDS
        :param 查询tags
        :return 标签列表
        """
        tag_objs = [];
        tag_obj_list = self.qa_tag_list()
        for tag_name in tags:
            for tag_obj in tag_obj_list:
                if tag_name == tag_obj["name"]:
                    tag_objs.append(tag_obj)
        return tag_objs;