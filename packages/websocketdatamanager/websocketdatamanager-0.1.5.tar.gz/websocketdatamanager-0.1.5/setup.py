from setuptools import setup

from pathlib import Path

path = Path(__file__).resolve().parent

with open(path/'README.md', encoding='utf-8') as f:
    long_description = f.read()

with open(path/'VERSION') as version_file:
    version = version_file.read().strip()

setup(name='websocketdatamanager',
      version=version,
      description='Websocket data manager, from rmq to ws',
      url='https://gitlab.com/pineiden/websocketsoftware',
      author='David Pineda Osorio',
      author_email='dpineda@csn.uchile.cl',
      license='GPLv3',
      packages=["websocketdatamanager"],
      install_requires=["ujson", "click",
                        "django","pytz",
                        "networktools",
                        "data_amqp",
                        "tasktools",
                        "basic_queuetools",],
      long_description=long_description,
      long_description_content_type='text/markdown',
      zip_safe=False)
