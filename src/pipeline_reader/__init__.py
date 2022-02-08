import re
import pipeline_reader.reader as reader
from pipeline_reader.objects import Pipeline
from pipeline_reader.objects import Stage
from pipeline_reader.objects import Options

def loads(data):
    return reader.loads(data)

def load(f):
    return reader.load(f)

def run(_pipeline, gs=None, ls=None):
    return reader.run(_pipeline, gs=gs, ls=ls)

if __name__ == '__main__':
    with open('tests/test.pipeline') as f:
        p = load(f)
    run(p)