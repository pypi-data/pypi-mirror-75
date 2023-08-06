# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['readkeys']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'readkeys',
    'version': '1.0.0',
    'description': 'Python library to read from stdin a single char, keypress (with escape sequences) or line.',
    'long_description': '# readkeys\n\n[![pypi version](https://img.shields.io/pypi/v/readkey)](https://pypi.org/project/readkey/)\n[![supported Python version](https://img.shields.io/pypi/pyversions/readkey)](https://pypi.org/project/readkey/)\n[![license](https://img.shields.io/pypi/l/readkey)](https://pypi.org/project/readkey/)\n\nPython library to read from stdin a single char, keypress (with escape sequences) or line.\n\nOriginally a fork of [magmax/python-readchar](https://github.com/magmax/python-readchar), it was rewritten to fix some bugs and better support UNIX and Windows systems.\n\n## Usage\n\n```python\nimport readkeys\n\nch = readkeys.getch()  # get a single character\nkey = readkeys.getkey()  # get a single keypress\nline = readkeys.getline()  # get a line of text\nline2 = readkeys.getline(raw=False)  # Get a line of text and print out characters as they are typed, similar to built-in input.\nflush = readkeys.flush()  # flush stdin\n```\n\n## Functions\n\n### `getch`\n\nThe `getch` function reads a single character byte from stdin. The buffer is not flushed after read.\n\nThe function has the following type signature:\n`getch(NONBLOCK: bool = False, encoding: str = None, raw: bool = True) -> str`\n\n* `NONBLOCK: bool` use non-blocking mode when reading from stdin, defaults to False. The library may encounter unforeseen errors if set to `True`.\n* `encoding: str` specify an encoding (e.g. utf-8) to be used to decode bytes from the stdin buffer. If unspecified it assumes characters can be directly extracted from stdin.\n* `raw: bool` put tty terminal in raw mode before reading, see [tty.setraw](https://docs.python.org/3/library/tty.html#tty.setraw). If set to `False` the characters will still appear in the terminal as they are typed. Settings before changing to raw mode are saved and restored when the read operation is complete.<br>\nThe option is ignored on Windows systems as they use a completely different terminal environment and a different library is necessary to read character from stdin: [`msvcrt`](https://docs.python.org/3.8/library/msvcrt.html).\n\n### `getkey`\n\nThe `getkey` function reads a single keypress from stdin, including escape sequences of function keys. For example arrow keys are returned with their full escape sequence, without leaving anything in the buffer (`0x1b5b41`, `0x1b5b42`, `0x1b5b43` or `0x1b5b44`).\n\nThe function has the following type signature:\n`getch(getch_fn: Callable[[], str] = None, encoding: str = "", raw: bool = True) -> str`\n\n* `getch_fn: Callable[[], str]` if passed, use the this function instead of the built-in [`getch`](#getch) to read the single bytes from stdin. The library may encounter unforeseen errors if this option is used.\n* `encoding: str` specify an encoding (e.g. utf-8) to be used to decode bytes from the stdin buffer. See [`getch`](#getch).\n* `raw: bool` put tty terminal in raw mode before reading. See [`getch`](#getch).\n\n### `getline`\n\nThe `getline` function reads a full line of characters from stdin, including non-standard keys (e.g. arrow keys). It defaults to raw mode, leaving characters unprinted on screen.\n\nThe function has the following type signature:\n`(getch_fn: Optional[Callable[[], str]] = None, encoding: str = None, raw: bool = True) -> str`\n\n* `getch_fn: Callable[[], str]` if passed, use the this function instead of the built-in [`getch`](#getch) to read the single bytes from stdin. The library may encounter unforeseen errors if this option is used.\n* `encoding: str` specify an encoding (e.g. utf-8) to be used to decode bytes from the stdin buffer. See [`getch`](#getch).\n* `raw: bool` put tty terminal in raw mode before reading. See [`getch`](#getch).\n\n### `flush`\n\nThe `flush` function removes any leftover byte from stdin and returns them as a string. It is useful to clear the buffer from any remaining bytes after doing a single read with `getch`.\n\nThe function has the following type signature:\n`flush() -> str`',
    'author': 'Matteo Campinoti',
    'author_email': 'matteo.campinoti94@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/MatteoCampinoti94/PythonRead',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
