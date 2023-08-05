
# ipyquiz

[![Build Status](https://travis-ci.org/boyuai/ipyquiz.svg?branch=master)](https://travis-ci.org/boyuai/ipyquiz)
[![codecov](https://codecov.io/gh/boyuai/ipyquiz/branch/master/graph/badge.svg)](https://codecov.io/gh/boyuai/ipyquiz)


A Custom Jupyter Widget Library

## Installation

You can install using `pip`:

```bash
pip install ipyquiz
```

Or if you use jupyterlab:

```bash
pip install ipyquiz
jupyter labextension install @jupyter-widgets/jupyterlab-manager
```

If you are using Jupyter Notebook 5.2 or earlier, you may also need to enable
the nbextension:
```bash
jupyter nbextension enable --py [--sys-prefix|--user|--system] ipyquiz
```

## Development

```bash
docker run --rm -it -p 8888:8888 -v $(pwd):/home/jovyan jupyter/minimal-notebook bash
```

```bash
pip install -e ".[test, examples]"
jupyter nbextension install --sys-prefix --symlink --overwrite --py ipyquiz
jupyter nbextension enable --sys-prefix --py ipyquiz
jupyter notebook
```

[http://localhost:8888](http://localhost:8888)

## Publish

### python部分

```bash
python setup.py sdist bdist_wheel
pip install twine
twine upload dist/ipyquiz-*
```

### npm部分

去掉antd和react的依赖，防止和本来项目冲突

#### css/widget.css

删除：

```css
@import '~antd/dist/antd.css';
```

#### package.json

删除：

```
"antd": "^4.2.0",
"react": "^16.13.1",
"react-dom": "^16.13.1"
```
