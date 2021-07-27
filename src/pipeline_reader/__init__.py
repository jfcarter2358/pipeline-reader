import re
from pipeline_reader.objects import Pipeline
from pipeline_reader.objects import Stage
from pipeline_reader.objects import Options

def loads(data):
    # define patterns for cleaning out comments
    inline_patterns = [
        '(?:^|[ \t])+\/\/(.*)',
        '(?:^|[ \t])+#(.*)'
    ]

    # clean out comments
    for inline_pattern in inline_patterns:
        data = re.sub(inline_pattern, '', data)

    lines = data.split('\n')

    # define patterns for parsing pipeline file
    pipeline_pattern = '^\\s*pipeline\\s*\\{'
    stage_pattern = '^\\s*stage\\s*\\([\'\"](.*)[\'\"]\\)\\s*\\{'
    options_pattern = '^\\s*options\\s*\\{'
    close_pattern = '^\\s*\\}'

    # holder objects
    pipeline = None
    stage = None
    options = None

    is_stage = False
    is_options = False

    for line in lines:
        if not line.strip():
            continue
        m = re.match(pipeline_pattern, line)
        if m:
            obj = Pipeline()
            pipeline = obj
            continue
        m = re.match(stage_pattern, line)
        if m:
            is_stage = True
            obj = Stage(m.groups(1)[0])
            stage = obj
            continue
        m = re.match(options_pattern, line)
        if m:
            is_options = True
            obj = Options()
            options = obj
            continue
        m = re.match(close_pattern, line)
        if m:
            if is_stage:
                pipeline.stages.append(stage)
            if is_options:
                pipeline.options = eval('{{{}}}'.format(' '.join([f'{o},' for o in options.code.split('\n')])[:-1]))
            is_stage = False
            is_options = False
            continue
        if is_stage:
            if stage.indent == -1:
                stage.indent = len(line) - len(line.lstrip())
            stage.code += line[stage.indent:] + '\n'
        if is_options:
            options.code += line.strip() + '\n'
    return pipeline

def load(f):
    return loads(f.read())

def run(obj, gs={}, ls={}):
    g = {**globals(), **gs}
    l = {**locals(), **ls}
    for stage in obj.stages:
        exec(stage.code, g, l)

if __name__ == '__main__':
    with open('tests/test.pipeline') as f:
        p = load(f)
    run(p)