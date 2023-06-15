class Pipeline:
    def __init__(self):
        self.agent = None
        self.stages = []
        self.options = []


    def __str__(self):
        return f'Pipeline(stages="{self.stages}", options="{self.options}")'

    def __repr__(self):
        return self.__str__()

class Agent:
    def __init__(self):
        self.code = ''
        self.indent = -1
        self.kubernetes = None
        self.ecs = None

    def __str__(self):
        return f'Agent(kubernetes="{self.kubernetes}", ecs="{self.ecs}")'
    
    def __repr__(self):
        return self.__str__()

class Kubernetes:
    def __init__(self):
        self.code = ''
        self.indent = -1
        self.inheritFrom = None
        self.yaml = None

    def __str__(self):
        return f'Kubernetes(inheritFrom="{self.inheritFrom}", yaml="{self.yaml}")'

    def __repr__(self):
        return self.__str__()

class Ecs:
    def __init__(self):
        self.code = ''
        self.indent = -1
        self.inheritFrom = None
        self.cpu = None
        self.memory =None
        self.image = None
        self.logDriver = None
        self.logDriverOptions = None
        self.portMappings = None

    def __str__(self):
        return f'Ecs(inheritFrom="{self.inheritFrom}",cpu="{self.cpu}",memory="{self.memory}",image="{self.image}",logDriver="{self.logDriver}",logDriverOptions="{self.logDriverOptions}",portMappings="{self.portMappings}",)'

    def __repr__(self):
        return self.__str__()

class Stage:
    def __init__(self, name=''):
        self.name = name
        self.code = ''
        self.indent = -1
        self.pre = None
        self.post = None
        self.when = None
        self.retry = None

    def __str__(self):
        return f'Stage(name="{self.name}", code="{self.code}", pre="{self.pre}", post="{self.post}", when="{self.when}", retry="{self.retry}")'

    def __repr__(self):
        return self.__str__()

class Pre:
    def __init__(self):
        self.code = ''
        self.indent = -1

    def __str__(self):
        return f'Pre(code="{self.code}")'

    def __repr__(self):
        return self.__str__()

class Post:
    def __init__(self):
        self.success = None
        self.failure = None
        self.always = None

    def __str__(self):
        return f'Post(success="{self.success}", failure="{self.failure}", always="{self.always}")'

    def __repr__(self):
        return self.__str__()

class Success:
    def __init__(self):
        self.code = ''
        self.indent = -1
        self.goto = None

    def __str__(self):
        return f'Success(code="{self.code}", goto="{self.goto}")'

    def __repr__(self):
        return self.__str__()

class Failure:
    def __init__(self):
        self.code = ''
        self.indent = -1
        self.goto = None

    def __str__(self):
        return f'Failure(code="{self.code}", goto="{self.goto}")'

    def __repr__(self):
        return self.__str__()

class Always:
    def __init__(self):
        self.code = ''
        self.indent = -1
        self.goto = None

    def __str__(self):
        return f'Always(code="{self.code}", goto="{self.goto}")'

    def __repr__(self):
        return self.__str__()

class When:
    def __init__(self):
        self.code = ''
        self.indent = -1

    def __str__(self):
        return f'When(code="{self.code}")'

    def __repr__(self):
        return self.__str__()

class Goto:
    def __init__(self, code):
        self.code = code.strip()

    def __str__(self):
        return f'Goto(code="{self.code}")'

    def __repr__(self):
        return self.__str__()

class Retry:
    def __init__(self, retries):
        self.retries = int(retries.strip())

    def __str__(self):
        return f'Retry(retries="{self.retries}")'

    def __repr__(self):
        return self.__str__()

class Options:
    def __init__(self):
        self.code = ''
        self.indent = -1

    def __str__(self):
        return f'Options(code="{self.code}")'

    def __repr__(self):
        return self.__str__()