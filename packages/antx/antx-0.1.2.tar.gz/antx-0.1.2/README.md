# antx - Annotation Transfer
Transfer annotations from source text to destination using diff match patch.

![Test](https://github.com/Esukhia/annotation_transfer/workflows/Test/badge.svg)
[![PyPI version](https://badge.fury.io/py/antx.svg)](https://badge.fury.io/py/antx)

## Usage

### Install using pip.
```
$ pip install antx
```

### Import
```
from antx import transfer
```

### Transfer
```
new_target = transfer(source_text, target_text, annotations, output="txt", optimized=True)
```
**source_text** := contains source text

**target_text** := contains target text

**annotations** := contains list of annotations in source text that you want to transfer to target text

**output** := Flag to indicate type of output. It can be txt or yaml.

**optimized** := Boolean flag to choose whether you want to proceed with **node dmp** or not. By default it is set to true. 
