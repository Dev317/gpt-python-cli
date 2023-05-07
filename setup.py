from setuptools import setup

with open("./requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

setup(
    name='pyopengpt_cli',
    version='0.1.2',
    py_modules=['main'],
    install_requires=[requirements],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'gpt = main:cli',
        ],
    },
)