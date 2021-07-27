# Pipeline Reader

## About

`pipeline-reader` is a package designed to make it easier to user Jenkinsfile-like pipeline files in Python projects. While JSON and YAML are generally sufficient for this task, there may be times where you want to execute code, which JSON and YAML are not well-suited for. In this case, pipeline-reader allows you to define stages containing Python code which are then run sequentially.

## Examples

### Writing a Pipeline

A basic pipeline consists of a pipeline block containing stages as follows:
```
pipeline {
    stages {
        stage('foo') {
            print('do something')
        }
    }
}
```
You can then add an options block like so
```
pipeline {
    options {
        "foo1": "bar1"
        "foo2": "bar2"
    }
    stages {
        stage('foo') {
            print('do something')
        }
    }
}
```
These options will then be stored in a dictionary and made available via the Pipeline object that `pipeline-reader` returns
In addition, the code context carries over between stages, so running
```
pipeline {
    stages {
        stage('foo') {
            variable = True
        }
        stage('bar') {
            print(variable)
        }
    }
}
```
will output `True`.
Finally, Python and C style comments are both supported inside the pipeline files.
```
# this will be ignored when the file is loaded in
pipeline {
    stages {
        // this will also be ignored
        stage('foo') {
            # even comments inside of stages are stripped out
            print('do something')
        }
    }
}
```

### Using `pipeline-reader` in an Application
To utilize `pipeline-reader`, you'll want to use something like what is shown below

```Python
import pipeline_reader

# this will load your pipeline
with open('filename.pipeline') as f:
    pipeline = pipeline_reader.load(f)

# this will execute your pipeline
pipeline_reader.run(pipeline, globals(), locals())

```
## To Do

- [x] Parse pipeline file
- [x] Run loaded pipelines
- [ ] Pre-stage
- [ ] Post-stage
- [ ] Catch stage success
- [ ] Catch stage failure
- [ ] Allow loading of arbitrary block types

## Contact

If you have any questions or concerns, please reach out to me (John Carter) at jfcarter2358@gmail.com