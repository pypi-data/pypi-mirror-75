import time
import traceback
import os
import xlsxwriter
import xlrd

from tqdm import tqdm

from .module import Module
from ..caller.qa_caller import QACaller
from ..caller.intent_caller import  IntentCaller
from ..entity.answer import Answer
from ..entity.enums import QuestionType, QuestionMode,QuestionField
from ..entity.exception import BfEngineException, ErrorCode
from ..logger import log


class IntentAnswering(Module):
    """
    问答
    """
    tmp_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    faq_sq_empty_path = tmp_dir + "/data/问答上传模板.xlsx"
    faq_lq_empty_path = tmp_dir + "/data/语料上传模板.xlsx"

    def __init__(self, app_id):
        super().__init__(app_id, 'qa')
        self.qaCaller = QACaller(app_id)
        self.intentCaller = IntentCaller(app_id)
    def train(self, data: str = None,intent_path: str = None,append: bool = False):
        """
        :param data:
        :param append: 是否追加，True
        :return: 训练是否成功
        """

        try:
            log.info('intent: prepare train')
            if data:
                # 清空FAQ
                if not append:
                    self._upload_question(self.faq_sq_empty_path, is_log=False)
                    self._upload_corpus(self.faq_lq_empty_path, is_log=False)
                json = []
                for item in data["data"]:
                    json.append({"sq": str(item["name"]),
                                 "lq": list(item["corpus"]),
                                 "answer": str(item["name"])
                                 })
                self._upload_json({"data": json})
            elif intent_path:
                # 清空FAQ
                if not append:
                    self._upload_question(self.faq_sq_empty_path, is_log=False)
                    self._upload_corpus(self.faq_lq_empty_path, is_log=False)
                intent = self._read_intent_path(intent_path)
                json = []
                for item in intent.keys():
                    json.append({"sq": str(item),
                                 "lq": list(intent[item]),
                                 "answer": str(item)
                                 })
                self._upload_json({"data": json})
            self._train()
        except BfEngineException as bfe:
            log.error(bfe)
            return False
        except Exception as e:
            log.error('unknown exception')
            log.error(e)
            traceback.print_exc()
            return False
        return True
    def publish(self):
        """
        :发布
        :return: 机器人回答
        """
        self._pulish()
    def export(self,sq_path: str = None, lq_path: str = None):
        """
        导出问答和语料文件
        :param sq_path 问答文件路径
        :param lq_path 语料文件路径
        """
        self._export(sq_path,lq_path)

    def query(self, text: str,online: bool=False) -> Answer:
        """
        :param text: 用户问
        :return: 机器人回答
        """

        data = self.intentCaller.predict(text,online)
        if len(data)>0:
            return Answer(data[0]["matchQuestion"],data[0]["score"])
        else:
            return None
    def _train(self):
        log.info('qa: start training')
        train_id = self.qaCaller.train()
        progress = 0

        with tqdm(total=100) as bar:
            bar.set_description("intent training...")
            while progress < 100:
                old_progress = progress
                progress = self.qaCaller.train_status(train_id)
                bar.update(progress - old_progress)
                time.sleep(1)
            bar.set_description("intent train finished")
        time.sleep(5)
    def _pulish(self):
        log.info('intent: start release')
        publish_id = self.qaCaller.publish()
        progress = 0

        with tqdm(total=100) as bar:
            bar.set_description("intent release...")
            while progress < 100:
                old_progress = progress
                progress = self.qaCaller.publish_status(publish_id)
                bar.update(progress - old_progress)
                time.sleep(1)
            bar.set_description("intent release finished")
        time.sleep(5)
    def _upload_json(self, content):
        """
        获取从路径中json
        """
        try:
            data = content["data"]
            for item in data:
                data_id = self.qaCaller.upload_json_sq(item)
                self.qaCaller.upload_json_lq(data_id, item)
        except BfEngineException as bfe:
            log.error(bfe)
            return False
        except Exception as e:
            return None

    def _upload_corpus(self, corpus_path, is_log: bool = True,append: bool = False):
        """
        上传qa语料
        :param corpus_path 语料路径
        :param append True:增量,false:全量
        """
        data_id = self.qaCaller.upload(QuestionType.LQ, QuestionMode.INCRE if append else QuestionMode.FULL, corpus_path)

        progress = 0
        while progress < 100:
            progress = self.qaCaller.upload_status(data_id, is_log=is_log)
            time.sleep(1)

    def _upload_question(self, question_path, is_log=True,append: bool = False):
        if not question_path:
            raise BfEngineException(ErrorCode.argument_missing_error, 'missing question path')

        data_id = self.qaCaller.upload(QuestionType.SQ_ANS, QuestionMode.INCRE if append else QuestionMode.FULL, question_path)

        progress = 0
        while progress < 100:
            progress = self.qaCaller.upload_status(data_id, is_log=is_log)
            time.sleep(1)
    def _export(self,sq_path: str = None, lq_path: str = None):
        """
        导出问答和语料文件
        :param sq_path 问答文件路径
        :param lq_path 语料文件路径
        """
        try:
            if sq_path:
                data_path = self.qaCaller.download_launch(QuestionType.SQ_ANS)
                self.qaCaller.download(sq_path,data_path)
            if lq_path:
                data_path = self.qaCaller.download_launch(QuestionType.LQ)
                self.qaCaller.download(lq_path, data_path)
        except BfEngineException as bfe:
            log.error(bfe)
        except Exception as e:
            log.error(e)
    def _read_intent_path(self,intent_path:str=None)->list:
        workbook = xlrd.open_workbook(intent_path)
        if workbook.sheets()==0:
            return []
        sheet = workbook.sheet_by_index(0)
        intent = {}
        for row in range(1, sheet.nrows):  # 行
            name = sheet.cell_value(row, 0)  # 语料
            corpus = sheet.cell_value(row, 1) # 意图名称
            if name in intent.keys():
                intent[name].append(corpus)
            else:
                intent[name]=[corpus]
        return intent