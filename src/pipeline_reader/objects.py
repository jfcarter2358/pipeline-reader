class Pipeline:
    def __init__(self):
        self.stages = []
        self.options = []

    def __str__(self):
        return f'Pipeline(stages="{self.stages}", options="{self.options}")'

    def __repr__(self):
        return self.__str__()

class Stage:
    def __init__(self, name=''):
        self.name = name
        self.code = ''
        self.indent = -1

    def __str__(self):
        return f'Stage(name="{self.name}", code="{self.code}")'

    def __repr__(self):
        return self.__str__()

class Options:
    def __init__(self):
        self.code = ''