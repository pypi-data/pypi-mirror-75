import py, os

s = """from __future__ import unicode_literals
"""

with open(os.path.join(os.path.dirname(__file__), 'test_dlopen.py')) as f:
    s += f.read()

exec(py.code.compile(s))
