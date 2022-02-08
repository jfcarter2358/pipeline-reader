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
These options will then be stored in a dictionary and made available via the Pipeline object that `pipeline-reader` returns (this object is also available to the pipeline itself at the `_pipeline` variable)
You can then access these options inside your pipeline script like so:
```
pipeline {
    options {
        "foo1": "bar1"
        "foo2": "bar2"
    }
    stages {
        stage('foo') {
            print(_pipeline.options)
        }
    }
}
```
There are also a group of "protected" options, in the sense that they have an effect on how the pipieline runs. The list of protected options is shown below:
- `exit_on_failure`
    - boolean
    - If True, then pipeline exits on a failed stage, otherwise pipeline will continue running
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
You can also get a little bit fancy with the stages by utilizing a `when` block to control if it fires or not
```
pipeline {
    options {
        "foo": "bar"
    }
    stages {
        stage('foo') {
            when {
                _pipeline.options["foo"] == "bar"
            }
            # This will run only if the "foo" option is set to "bar"
        }
    }
}
```
If you need to run specific code before your stage executes, you can use a `pre` block to make it more readable
```
pipeline {
    stages {
        stage('foo') {
            pre {
                message = 'hello world'
            }
            # this will print "hello world"
            print(message)
        }
    }
}
```
You can then control what happens after a stage through the use of a `post` block. `post` blocks support `always`, `success`, and `failure` sub-blocks with `always` being run first
```
pipeline {
    stages {
        stage('foo') {
            # if this succeeds then it will run the `always` block followed by the `success` block
            post {
                success {
                    print('Success!')
                }
                failure {
                    print('failure!')
                }
                always {
                    print('Always!')
                }
            }
        }
    }
}
```
To help with processes that fail often, you can set a `retry` directive in your stage to tell the pipeline how many times you'll want that staged to be retried
```
pipeline {
    stages {
        stage('foo') {
            retry {5}
            # this will retry 5 times after the inital try
        }
    }
}
```
You can also jump to another stage in any of the post blocks if you so desire with the `goto` directive
```
pipeline {
    stages {
        stage('foo') {
            # this stage will jump to another depending on success or failure
            post {
                success {
                    goto {Success Stage}
                }
                failure {
                    goto {Failure Stage}
                }
            }
        }
        stage('Success Stage') {
            # this will be run on a success of the `foo` stage
        }
        stage('Failure Stage') {
            # this will be run on a failure of the `foo` stage
        }
    }
}
```
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
- [x] Pre-stage
- [x] Post-stage
- [x] When-condition
- [x] Catch stage success
- [x] Catch stage failure
- [x] Goto directive
- [x] Retry directive
- [ ] Allow loading of arbitrary block types as plugins

## Contact

If you have any questions or concerns, please reach out to me (John Carter) at jfcarter2358@gmail.com