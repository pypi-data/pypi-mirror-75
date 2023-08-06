from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).resolve().parent

with open(this_directory/'README.md', encoding='utf-8') as f:
    readme = f.read()

with open(this_directory/'VERSION') as version_file:
    version = version_file.read().strip()

setup(name='datawork',
      version=version,
      description='Data Work system gather all data from a database to make analysis and charts',
      url='http://gitlab.csn.uchile.cl/dpineda/datawork',
      author='David Pineda Osorio',
      author_email='dpineda@csn.uchile.cl',
      license='GPLv3',
      packages=['datawork'],
      keywords=["collector", "gnss", "scheduler", "async", "multiprocess"],
      install_requires=["networktools",
                        "tasktools",
                        "basic_logtools",
                        "basic_queuetools",
                        "data_rdb",
                        "data_geo",
                        "data_amqp",
                        "gnsocket",
                        "uvloop",
                        "click",
                        "numpy",
                        "ujson"],
      entry_points={
          'console_scripts': ["datawork = datawork.scripts.run_datawork:run_datawork", ]
      },
      include_package_data=True,
      long_description=readme,
      long_description_content_type='text/markdown',
      zip_safe=False)
