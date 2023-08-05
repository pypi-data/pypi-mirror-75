from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as readme:
    description = readme.read()
setup(
    name='graphical-formula',
    version='0.0.7',
    py_modules=['graphical'],
    license='MIT LICENSE',
    author='17097231932',
    author_email='17097231932@163.com',
    url='https://github.com/17097231932/graphical/',
    description='快速的创建和使用图形公式',
    long_description=description
)
