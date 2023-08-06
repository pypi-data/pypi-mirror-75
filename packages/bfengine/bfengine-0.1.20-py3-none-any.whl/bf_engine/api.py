from . import util
from .config import Config
from .core.bot import Bot


def init():
    """
    创建整个BF Engine系统环境，包含初始化数据库及核心模块
    """
    pass


def create_bot(app_id: str = None, local=False, url=None) -> Bot:
    """
    创建bot，并返回实例
    """
    if not app_id:
        app_id = util.random_uuid()

    if local:
        Config.base_url = 'http://172.17.0.1'
    elif url:
        Config.base_url = url
    else:
        Config.base_url = Config.remote_url

    bot = Bot(app_id)
    bot.dm.load()
    return bot
