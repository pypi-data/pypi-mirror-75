class Answer:
    """
    机器人回答
    """
    def __init__(self, text: str, score: float):
        self.text = text
        self.score = score

    def __str__(self):
        return 'text: {}, score: {}'.format(self.text, self.score)

    def __repr__(self):
        return self.__str__()
