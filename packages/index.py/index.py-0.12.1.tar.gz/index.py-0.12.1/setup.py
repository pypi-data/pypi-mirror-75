# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['indexpy', 'indexpy.http', 'indexpy.openapi', 'indexpy.websocket']

package_data = \
{'': ['*']}

install_requires = \
['a2wsgi>=1.0.0,<2.0.0',
 'aiofiles>=0.5.0,<0.6.0',
 'jinja2>=2.10.3,<3.0.0',
 'pydantic>=1.6,<2.0',
 'python-multipart>=0.0.5,<0.0.6',
 'pyyaml>=5.3,<6.0',
 'starlette>=0.13.6,<0.14.0',
 'uvicorn>=0.11.3,<0.12.0']

extras_require = \
{':python_version < "3.8"': ['typing-extensions>=3.7.4,<4.0.0'],
 'gunicorn': ['gunicorn>=20.0.4,<21.0.0'],
 'test': ['requests>=2.24.0,<3.0.0']}

entry_points = \
{'console_scripts': ['index-cli = indexpy.cli:main']}

setup_kwargs = {
    'name': 'index.py',
    'version': '0.12.1',
    'description': 'An easy-to-use asynchronous web framework based on ASGI.',
    'long_description': '# index.py\n\n中文 | [English](https://github.com/abersheeran/index.py/tree/master/README-en.md)\n\n[![Github Action Test](https://github.com/abersheeran/index.py/workflows/Test/badge.svg)](https://github.com/abersheeran/index.py/actions?query=workflow%3ATest)\n[![Build setup.py](https://github.com/abersheeran/index.py/workflows/Build%20setup.py/badge.svg)](https://github.com/abersheeran/index.py/actions?query=workflow%3A%22Build+setup.py%22)\n[![Publish PyPi](https://github.com/abersheeran/index.py/workflows/Publish%20PyPi/badge.svg)](https://github.com/abersheeran/index.py/actions?query=workflow%3A%22Publish+PyPi%22)\n[![PyPI](https://img.shields.io/pypi/v/index.py)](https://pypi.org/project/index.py/)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/index.py)\n\n一个基于 ASGI 协议的高性能 web 框架。[Index.py 文档](https://abersheeran.github.io/index.py/)\n\n- 灵活且高效的路由系统 (基于 Radix Tree)\n- 自动解析请求 & 生成文档 (基于 `pydantic`)\n- 可视化 API 接口 (基于 `ReDoc`, 针对中文字体优化)\n- 非常简单的部署 (基于 `uvicorn` 与 `gunicorn`)\n- 挂载 ASGI/WSGI 应用 (基于 [a2wsgi](https://github.com/abersheeran/a2wsgi/))\n- 进程内后台任务 (基于 `asyncio`)\n- 可使用任何可用的 ASGI 生态\n\n## Install\n\n```bash\npip install -U index.py\n```\n\n或者直接从 Github 上安装最新版本（不稳定）\n\n```bash\npip install -U git+https://github.com/abersheeran/index.py@setup.py\n```\n',
    'author': 'abersheeran',
    'author_email': 'me@abersheeran.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/abersheeran/index.py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
