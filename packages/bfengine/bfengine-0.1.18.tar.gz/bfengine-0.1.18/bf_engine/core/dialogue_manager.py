import json
import copy
import os
import traceback
import uuid

from ..caller.dialogue_manager_caller import DialogueManagerCaller
from ..config import Config
from ..core.module import Module
from ..entity.exception import BfEngineException
from ..logger import log

module_name_map = {
    "qa": "faq",
    "kg": "domain_kg",
    "te": "task_engine"
}
module_template = {
    "ccs_id": "",
    "name": "",
    "url": "",
    "app_id": "",
    "modules": [],
    "request_header": "",
    "request_body": "",
    "active": True,
    "timeout": 2000,
    "scenario_id": "",
    "subscribeKeys": {},
    "publishKeys": {}
}
phase_template = {
    "phase_id": "",
    "action_rules": [],
    "group": [{"name": "group1", "flowMode": "ALL", "bots": []}],
    "dispatcher": {"applyCurTask": False, "applyPreTask": False, "dispatchers": [
        {"exclusive": False, "filter": {"op": "and", "operands": []}, "groups": ["group1"]}]},
    "score_rules": [],
    "respond_rules": [],
    "priority_rules": [],
    "thresholds": [],
    "bots": [],
    "models": [],
    "actions": []
}
threshold_template = {
    "condition": {},
    "threshold": 60,
    "bot": ""
}
config_template = {
    "ccs_id": "",
    "confid": 2020,
    "name": "dialogue_manager_config",
    "status": "active",
    "ranker": {"respond_rules": [], "priority_rules": [], "score_rules": [], "bots": []},
    "chat_config": {"chat_config": {"dispatchers": []}, "bots": [], "models": []},
    "workflow": []
}


class ConfigGenerator:
    @staticmethod
    def get_module(raw_module_name: str, app_id: str, url: str):
        if not raw_module_name:
            return None

        if raw_module_name in module_name_map:
            module_name = module_name_map[raw_module_name]
        else:
            module_name = raw_module_name
        module = copy.deepcopy(module_template)
        module['ccs_id'] = app_id
        module['name'] = raw_module_name
        module['url'] = url
        module['app_id'] = app_id
        module['modules'].append(module_name)
        return module

    @staticmethod
    def get_config(app_id: str):
        config = copy.deepcopy(config_template)
        config['ccs_id'] = app_id
        return config

    @staticmethod
    def get_phase():
        return copy.deepcopy(phase_template)

    @staticmethod
    def get_threshold(module_name: str, threshold_score: int):
        threshold = copy.deepcopy(threshold_template)
        threshold['bot'] = module_name
        threshold['threshold'] = threshold_score
        return threshold


class DialogueManager(Module):
    """
    对话管理
    """

    def __init__(self, app_id):
        super().__init__(app_id, 'dm')
        self.app_id = app_id
        self.module_call_url = '{}:{}/{}'.format(Config.base_url, Config.robot_port, Config.robot_url)
        self.caller = DialogueManagerCaller(app_id)
        tmp_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        self.default_dm_config_path = tmp_dir + "/data/default_dm.json"

    """
    加载对话管理配置，不传配置数据则加载默认配置
    
    """

    def load(self, data: dict = None):
        try:
            if not data:
                data = json.load(open(self.default_dm_config_path))
            config = self._config_generate(data)
            return self.caller.load_config(config)
        except BfEngineException as bfe:
            log.error(bfe)
            return False
        except Exception as e:
            log.error("dm: 加载对话配置异常")
            log.error(e)
            traceback.print_exc()
            return False

    def load_by_path(self, config_path: str = None):
        simple_phases = json.load(open(config_path))
        if not config_path:
            simple_phases = json.load(open(self.default_dm_config_path))
        return self.load(simple_phases)

    """
    根据传入参数生成出话配置
    """

    def _config_generate(self, simple_phases):
        module_map = {}
        workflow = []
        config = ConfigGenerator.get_config(self.app_id)
        config['workflow'] = workflow
        for simple_phase in simple_phases:
            modules = []
            phase = ConfigGenerator.get_phase()
            for module_name in simple_phase.keys():
                threshold_score = simple_phase[module_name]

                if module_name not in module_map:
                    module = ConfigGenerator.get_module(module_name, self.app_id, self.module_call_url)
                    module_map[module_name] = module
                else:
                    module = module_map[module_name]

                modules.append(module)
                threshold = ConfigGenerator.get_threshold(module_name, threshold_score)
                phase['group'][0]['bots'].append(module_name)
                phase['thresholds'].append(threshold)
            phase['phase_id'] = str(uuid.uuid4())
            phase['bots'] = modules
            workflow.append(phase)
        return config

    def query(self, msg):
        try:
            answer = self.caller.call(msg)
            return answer
        except BfEngineException as bfe:
            log.error(bfe)
            return False
        except Exception as e:
            log.error("dm: 出话异常")
            log.error(e)
            traceback.print_exc()
            return False

    """
    检查传入配置
    """

    def _check_config(self):
        pass
