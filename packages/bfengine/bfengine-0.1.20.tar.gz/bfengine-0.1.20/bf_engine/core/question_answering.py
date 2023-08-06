import time
import traceback
import os

from tqdm import tqdm

from .module import Module
from ..caller.qa_caller import QACaller
from ..entity.answer import Answer
from ..entity.enums import QuestionType, QuestionMode,QuestionField
from ..entity.exception import BfEngineException, ErrorCode
from ..logger import log


class QuestionAnswering(Module):
    """
    问答
    """
    tmp_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    faq_sq_empty_path = tmp_dir + "/data/问答上传模板.xlsx"
    faq_lq_empty_path = tmp_dir + "/data/语料上传模板.xlsx"

    def __init__(self, app_id):
        super().__init__(app_id, 'qa')
        self.caller = QACaller(app_id)
    def train(self, data: str = None, question_path: str = None, corpus_path: str = None,append: bool = True):
        """
        :param data:
        :param question_path: 标准问路径
        :param corpus_path: 语料路径
        :param append: 是否追加，True
        :return: 训练是否成功
        """
        try:
            log.info('qa: prepare train')
            if data:
                # 清空FAQ
                if not append:
                    self._upload_question(self.faq_sq_empty_path, is_log=False)
                    self._upload_corpus(self.faq_lq_empty_path, is_log=False)
                self._upload_json(data)
            else:
                self._upload_question(question_path,append)
                if corpus_path:
                    self._upload_corpus(corpus_path,append)
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
        return self.caller.call_module('faq', text,online)
    def qa_tag_list(self):
        """
        获取标签列表
        """
        return self.caller.qa_tag_list()
    def qa_tag_add(self,name:str=None):
        """
        添加标签
        :param name 标签名称
        """
        return self.caller.qa_tag_add(name)
    def qa_list(self) -> str:
        """
        : 查询标准问列表
        :return: 标准问列表
        """
        return self.caller.qa_list(QuestionField.ALL)
    def question_list(self) -> str:
        """
        : 查询标准问列表
        :return: 标准问列表
        """
        return self.caller.sq_list(QuestionField.ALL)

    def corpus_list(self,question_id) -> str:
        """
        : 查询标准问下语料列表
        :return: 标准问列表
        """
        return self.caller.lq_list(question_id)
    def _train(self):
        log.info('qa: start training')
        train_id = self.caller.train()
        progress = 0

        with tqdm(total=100) as bar:
            bar.set_description("qa training...")
            while progress < 100:
                old_progress = progress
                progress = self.caller.train_status(train_id)
                bar.update(progress - old_progress)
                time.sleep(1)
            bar.set_description("qa train finished")
        time.sleep(5)
    def _pulish(self):
        log.info('qa: start release')
        publish_id = self.caller.publish()
        progress = 0

        with tqdm(total=100) as bar:
            bar.set_description("qa release...")
            while progress < 100:
                old_progress = progress
                progress = self.caller.publish_status(publish_id)
                bar.update(progress - old_progress)
                time.sleep(1)
            bar.set_description("qa release finished")
        time.sleep(5)
    def _upload_json(self, content):
        """
        获取从路径中json
        """
        try:
            data = content["data"]
            for item in data:
                data_id = self.caller.upload_json_sq(item)
                self.caller.upload_json_lq(data_id, item)
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
        data_id = self.caller.upload(QuestionType.LQ, QuestionMode.INCRE if append else QuestionMode.FULL, corpus_path)

        progress = 0
        while progress < 100:
            progress = self.caller.upload_status(data_id, is_log=is_log)
            time.sleep(1)

    def _upload_question(self, question_path, is_log=True,append: bool = False):
        if not question_path:
            raise BfEngineException(ErrorCode.argument_missing_error, 'missing question path')

        data_id = self.caller.upload(QuestionType.SQ_ANS, QuestionMode.INCRE if append else QuestionMode.FULL, question_path)

        progress = 0
        while progress < 100:
            progress = self.caller.upload_status(data_id, is_log=is_log)
            time.sleep(1)
    def _export(self,sq_path: str = None, lq_path: str = None):
        """
        导出问答和语料文件
        :param sq_path 问答文件路径
        :param lq_path 语料文件路径
        """
        try:
            if sq_path:
                data_path = self.caller.download_launch(QuestionType.SQ_ANS)
                self.caller.download(sq_path,data_path)
            if lq_path:
                data_path = self.caller.download_launch(QuestionType.LQ)
                self.caller.download(lq_path, data_path)
        except BfEngineException as bfe:
            log.error(bfe)
        except Exception as e:
            log.error(e)
