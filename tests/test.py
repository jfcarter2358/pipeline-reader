import pipeline_reader as pr

global do_action
def do_action():
    print('Doing an action')

with open('tests/test.pipeline') as f:
    p = pr.load(f)
pr.run(p, globals(), locals())