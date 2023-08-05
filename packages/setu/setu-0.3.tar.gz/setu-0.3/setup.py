import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(name='setu',
      version='0.3',
      description='Setu\'s deeplink pckage',
      url='https://gitlab.com/setu-lobby/setu-pypi',
      author='Gandharva B',
      author_email='gandharva@setu.co',
      license='MIT',
      install_requires=["requests", "uuid", "PyJWT"],
      packages=['setu'],
      zip_safe=False)