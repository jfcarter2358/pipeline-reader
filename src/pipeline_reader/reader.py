import re
from pipeline_reader.objects import Pipeline
from pipeline_reader.objects import Stage
from pipeline_reader.objects import Options
from pipeline_reader.objects import Pre
from pipeline_reader.objects import Post
from pipeline_reader.objects import When
from pipeline_reader.objects import Success
from pipeline_reader.objects import Failure
from pipeline_reader.objects import Always
from pipeline_reader.objects import Goto
from pipeline_reader.objects import Retry
import cartils.external
from cartils.logger import Logger
import cartils.helpers
import uuid

def sh(cmd, redirect_stdout=False, redirect_stderr=False, fail_on_error=True):
    rc = 0
    out = ''
    err = ''
    if redirect_stdout and redirect_stderr:
        rc, out, err = cartils.external.cmd(cmd, redirect_stdout=redirect_stdout, redirect_stderr=redirect_stderr)
    elif redirect_stdout:
        rc, out = cartils.external.cmd(cmd, redirect_stdout=redirect_stdout, redirect_stderr=redirect_stderr)
    elif redirect_stderr:
        rc, err = cartils.external.cmd(cmd, redirect_stdout=redirect_stdout, redirect_stderr=redirect_stderr)
    else:
        rc = cartils.external.cmd(cmd, redirect_stdout=redirect_stdout, redirect_stderr=redirect_stderr)
    if rc != 0 and fail_on_error:
        exit(rc)
    return rc, out, err

def _goto(stage_name, pipeline):
    stage_name = stage_name.replace('\n', '').strip()
    for index, stage in enumerate(pipeline.stages):
        if stage.name == stage_name:
            return index
    return -1

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
    pre_pattern = '^\\s*pre\\s*\\{'
    post_pattern = '^\\s*post\\s*\\{'
    when_pattern = '^\\s*when\\s*\\{'

    # holder objects
    pipeline = None
    stage = None
    options = None

    is_stage = False
    is_options = False
    is_pre = False
    is_post = False
    is_when = False

    key = ["pipeline"]

    structure = {
        "pipeline": {
            "pattern": '^\\s*pipeline\\s*\\{',
            "code": "",
            "class": Pipeline,
            "object": None,
            "takes_param": False,
            "single_line": False,
            "children": {
                "options": {
                    "pattern": '^\\s*options\\s*\\{',
                    "code": "structure['pipeline']['object'].options = eval('{{{}}}'.format(' '.join([f'{o},' for o in structure['pipeline']['children']['options']['object'].code.split('\\n')])[:-1]))",
                    "class": Options,
                    "object": None,
                    "takes_param": False,
                    "single_line": False,
                    "children": {}
                },
                "stage": {
                    "pattern": '^\\s*stage\\s*\\([\'\"](.*)[\'\"]\\)\\s*\\{',
                    "code": "structure['pipeline']['object'].stages.append(structure['pipeline']['children']['stage']['object'])",
                    "class": Stage,
                    "object": None,
                    "takes_param": True,
                    "single_line": False,
                    "children": {
                        "retry": {
                            "pattern": '^\\s*retry\\s*\\{(.*)\\}',
                            "code": "structure['pipeline']['children']['stage']['object'].retry = structure['pipeline']['children']['stage']['children']['retry']['object']",
                            "class": Retry,
                            "object": None,
                            "takes_param": True,
                            "single_line": True,
                            "children": {}
                        },
                        "pre": {
                            "pattern": '^\\s*pre\\s*\\{',
                            "code": "structure['pipeline']['children']['stage']['object'].pre = structure['pipeline']['children']['stage']['children']['pre']['object']",
                            "class": Pre,
                            "object": None,
                            "takes_param": False,
                            "single_line": False,
                            "children": {}
                        },
                        "post": {
                            "pattern": '^\\s*post\\s*\\{',
                            "code": "structure['pipeline']['children']['stage']['object'].post = structure['pipeline']['children']['stage']['children']['post']['object']",
                            "class": Post,
                            "object": None,
                            "takes_param": False,
                            "single_line": False,
                            "children": {
                                "success": {
                                    "pattern": '^\\s*success\\s*\\{',
                                    "code": "structure['pipeline']['children']['stage']['children']['post']['object'].success = structure['pipeline']['children']['stage']['children']['post']['children']['success']['object']",
                                    "class": Success,
                                    "object": None,
                                    "takes_param": False,
                                            "single_line": False,
                                    "children": {
                                        "goto": {
                                            "pattern": '^\\s*goto\\s*\\{(.*)\\}',
                                            "code": "structure['pipeline']['children']['stage']['children']['post']['children']['success']['object'].goto = structure['pipeline']['children']['stage']['children']['post']['children']['success']['children']['goto']['object']",
                                            "class": Goto,
                                            "object": None,
                                            "takes_param": True,
                                            "single_line": True,
                                            "children": {}
                                        }
                                    }
                                },
                                "failure": {
                                    "pattern": '^\\s*failure\\s*\\{',
                                    "code": "structure['pipeline']['children']['stage']['children']['post']['object'].failure = structure['pipeline']['children']['stage']['children']['post']['children']['failure']['object']",
                                    "class": Failure,
                                    "object": None,
                                    "takes_param": False,
                                    "children": {
                                        "goto": {
                                            "pattern": '^\\s*goto\\s*\\{(.*)\\}',
                                            "code": "structure['pipeline']['children']['stage']['children']['post']['children']['failure']['object'].goto = structure['pipeline']['children']['stage']['children']['post']['children']['failure']['children']['goto']['object']",
                                            "class": Goto,
                                            "object": None,
                                            "takes_param": True,
                                            "single_line": True,
                                            "children": {}
                                        }
                                    }
                                },
                                "always": {
                                    "pattern": '^\\s*always\\s*\\{',
                                    "code": "structure['pipeline']['children']['stage']['children']['post']['object'].always = structure['pipeline']['children']['stage']['children']['post']['children']['always']['object']",
                                    "class": Always,
                                    "object": None,
                                    "takes_param": False,
                                    "children": {
                                        "goto": {
                                            "pattern": '^\\s*goto\\s*\\{(.*)\\}',
                                            "code": "structure['pipeline']['children']['stage']['children']['post']['children']['always']['object'].goto = structure['pipeline']['children']['stage']['children']['post']['children']['always']['children']['goto']['object']",
                                            "class": Goto,
                                            "object": None,
                                            "takes_param": True,
                                            "single_line": True,
                                            "children": {}
                                        }
                                    }
                                },
                            }
                        },
                        "when": {
                            "pattern": '^\\s*when\\s*\\{',
                            "code": "structure['pipeline']['children']['stage']['object'].when = structure['pipeline']['children']['stage']['children']['when']['object']",
                            "class": When,
                            "object": None,
                            "takes_param": False,
                            "single_line": False,
                            "children": {}
                        }
                    }
                }
            }
        }
    }

    for line in lines:
        if not line.strip():
            continue
        m = re.match(cartils.helpers.get_from_key_list(structure, key + ["pattern"]), line)
        if m:
            structure = cartils.helpers.set_from_key_list(structure, key + ["object"], cartils.helpers.get_from_key_list(structure, key + ["class"])())
            continue
        should_continue = False
        for child in cartils.helpers.get_from_key_list(structure, key + ["children"]):
            m = re.match(cartils.helpers.get_from_key_list(structure, key + ["children", child, "pattern"]), line)
            if m:
                key += ["children", child]
                if cartils.helpers.get_from_key_list(structure, key + ["takes_param"]):
                    structure = cartils.helpers.set_from_key_list(structure, key + ["object"], cartils.helpers.get_from_key_list(structure, key + ["class"])(m.groups(1)[0]))
                else:
                    structure = cartils.helpers.set_from_key_list(structure, key + ["object"], cartils.helpers.get_from_key_list(structure, key + ["class"])())
                should_continue = True
                if cartils.helpers.get_from_key_list(structure, key + ["single_line"]):
                    exec(cartils.helpers.get_from_key_list(structure, key + ["code"]), globals(), locals())
                    key = key[:-2]
                break
        if should_continue:
            continue
        m = re.match(close_pattern, line)
        if m:
            exec(cartils.helpers.get_from_key_list(structure, key + ["code"]), globals(), locals())
            if len(key) > 2:
                key = key[:-2]
                continue
            break
        if hasattr(cartils.helpers.get_from_key_list(structure, key + ["object"]), "code"):
            obj = cartils.helpers.get_from_key_list(structure, key + ["object"])
            if obj.indent == -1:
                obj.indent = len(line) - len(line.lstrip())
            obj.code += line[obj.indent:] + '\n'
            structure = cartils.helpers.set_from_key_list(structure, key + ["object"], obj)
    return structure['pipeline']['object']

def load(f):
    return loads(f.read())

def run(_pipeline, gs=None, ls=None):
    _logger = Logger("TRACE")
    if gs is None:
        gs = {}
    if ls is None:
        ls = {}
    _g = {**globals(), **gs}
    _l = {**locals(), **ls}
    _logger.TRACE(_pipeline)
    _logger.INFO('Starting pipeline')
    _stage_index = 0
    while _stage_index < len(_pipeline.stages):
        _stage = _pipeline.stages[_stage_index]
        _logger.DEBUG(f'Running stage {_stage.name}')
        _failed = False
        try:
            if _stage.when:
                if not eval(_stage.when.code):
                    _logger.INFO("Stage exited due to when condition")
                    _stage_index += 1
                    continue
            if _stage.pre:
                exec(_stage.pre.code, _g, _l)
            exec(_stage.code, _g, _l)
            if _stage.post:
                if _stage.post.always:
                    exec(_stage.post.always.code, _g, _l)
                    if _stage.post.always.goto:
                        _temp_index = _goto(_stage.post.always.goto.code, _pipeline)
                        if _temp_index == -1:
                            _logger.ERROR("Goto stage name is not valid")
                        else:
                            _stage_index = _temp_index - 1
                if _stage.post.success:
                    exec(_stage.post.success.code, _g, _l)
                    if _stage.post.success.goto:
                        _temp_index = _goto(_stage.post.success.goto.code, _pipeline)
                        if _temp_index == -1:
                            _logger.ERROR("Goto stage name is not valid")
                        else:
                            _stage_index = _temp_index - 1
        except SystemExit:
            _failed = True
            if _stage.retry:
                if _stage.retry.retries > 0:
                    _stage.retry.retries -= 1
                    continue     
            if _stage.post:
                if _stage.post.always:
                    exec(_stage.post.always.code, _g, _l)
                    if _stage.post.always.goto:
                        _temp_index = _goto(_stage.post.always.goto.code, _pipeline)
                        if _temp_index == -1:
                            _logger.ERROR("Goto stage name is not valid")
                        else:
                            _stage_index = _temp_index - 1
                if _stage.post.failure:
                    exec(_stage.post.failure.code, _g, _l)
                    if _stage.post.failure.goto:
                        _temp_index = _goto(_stage.post.failure.goto.code, _pipeline)
                        if _temp_index == -1:
                            _logger.ERROR("Goto stage name is not valid")
                        else:
                            _stage_index = _temp_index - 1
            if _pipeline.options["exit_on_failure"]:
                _logger.FAILURE('Pipeline failed')
                exit(1)
        _stage_index += 1
    _logger.SUCCESS('Pipeline finished successfully')

if __name__ == '__main__':
    with open('tests/test.pipeline') as f:
        p = load(f)
    run(p)