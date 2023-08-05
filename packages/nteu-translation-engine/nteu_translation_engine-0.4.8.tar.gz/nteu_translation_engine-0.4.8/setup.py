from setuptools import setup

setup(
    name='nteu_translation_engine',
    version='0.4.8',
    description='NTEU translation engine',
    url='https://github.com/Pangeamt/nteu-translation-engine',
    author='PangeaMT',
    author_email='a.cerda@pangeanic.es',
    license='MIT',
    packages=[
        'nteu_translation_engine'
    ],
    install_requires=[
        "aiohttp==3.6.2",
        "click",
        "pangeamt-nlp",
        "PyYAML",
        "uvloop"
    ],
    zip_safe=False
)
