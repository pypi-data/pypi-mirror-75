# %%

from setuptools import setup
import os
from pypandoc import convert_file


def read_md(f):
    return convert_file(f, 'rst')


README = os.path.join(os.path.dirname(__file__), "README.md")
a_ = read_md(README)
print(a_)
setup(
    name='Pack_2',
    scripts=['Greetings.py'],
    version='1.1.35',
    # long_description=open('README.md').read(),
    # long_description_content_type='text/markdown',
    # license=open("LICENSE").read()
)


# %%
