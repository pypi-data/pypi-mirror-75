from .dialogue_manager import DialogueManager
from .task_engine import TaskEngine
from .knowledge_graph import KnowledgeGraph
from .question_answering import QuestionAnswering
from .intent_answering import IntentAnswering

class Bot:
    """
    机器人
    """
    def __init__(self, app_id):
        self.app_id = app_id
        self.intent = IntentAnswering(app_id)
        self.qa = QuestionAnswering(app_id)
        self.kg = KnowledgeGraph(app_id)
        self.te = TaskEngine(app_id)
        self.dm = DialogueManager(app_id)
