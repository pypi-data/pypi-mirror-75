from setuptools import setup, find_packages

from pathlib import Path

path = Path(__file__).resolve().parent
with open(path/'README.md', encoding='utf-8') as f:
    long_description = f.read()

with open(path/'VERSION') as version_file:
    version = version_file.read().strip()


setup(name='gnsocket',
      version=version,
      description='GPS Network Socket, with asyncio stream manager',
      url='https://gitlab.com/pineiden/gus',
      author='David Pineda Osorio',
      author_email='dpineda@csn.uchile.cl',
      license='GPLv3',
      install_requires=["networktools",
                        "basic_queuetools",
                        "basic_logtools",
                        'chardet'],
      packages=["gnsocket"],      
      include_package_data=True,      
      package_dir={'gnsocket': 'gnsocket'},
      long_description=long_description,
      long_description_content_type='text/markdown',
      zip_safe=False)
