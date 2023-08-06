import os

from .util import random_str


class Config:
    default_app_id = os.environ.get('BF_ENGINE_DEFAULT_APP_ID', 'emotibotisthebestrobotoftheworld')
    base_url = os.environ.get('BF_ENGINE_BASE_URL', 'http://172.16.103.106')
    user_id = os.environ.get('BF_ENGINE_DEFAULT_USER_ID', 'bf-engine-user')
    session_id = os.environ.get('BF_ENGINE_DEFAULT_SESSION_ID', 'bf-engine-session' + random_str(8))
    robot_url = os.environ.get('BF_ENGINE_ROBOT_URL', 'openapi/v1/robot')
    robot_port = os.environ.get('BF_ENGINE_ROBOT_PORT', 9080)
    ssm_port = os.environ.get('BF_ENGINE_SSM_PORT', 8686)
    predict_port = os.environ.get('BF_ENGINE_PREDICT_PORT', 11035)
    te_port = os.environ.get('BF_ENGINE_TE_PORT', 14101)
    api_port = os.environ.get('BF_ENGINE_API_PORT', 81)
    dm_port = os.environ.get('BF_ENGINE_DM_PORT', 10000)
    remote_url = os.environ.get('BF_ENGINE_REMOTE_URL', 'http://172.16.103.106')
    backfill_speech = '我还在学习'
