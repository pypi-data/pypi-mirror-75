from setuptools import setup

print("AVISO: Primero instalar ORM_COLLECTOR")

from pathlib import Path

path = Path(__file__).resolve().parent
with open(path/'README.md', encoding='utf-8') as f:
    long_description = f.read()

with open(path/'VERSION') as version_file:
    version = version_file.read().strip()


setup(name='gnss_collector',
      version=version,
      description='Data Collector, for timeseries stations with ip:port address',
      url='http://gitlab.csn.uchile.cl/dpineda/collector',
      author='David Pineda Osorio',
      author_email='dpineda@csn.uchile.cl',
      license='MIT',
      packages=['gnss_collector'],
      keywords = ["collector","gnss", "scheduler", "async", "multiprocess"],
      install_requires=["networktools",
                        "tasktools",
                        "basic_logtools",
                        "basic_queuetools",
                        "datadbs",
                        "data_rdb",
                        "data_geo",
                        "dataprotocols",
                        "gnsocket",
                        "uvloop",
                        "orm_collector"],
      entry_points={
        'console_scripts':["collector = gnss_collector.scripts.run_collector:run_collector",]
        },
      include_package_data=True,
      long_description=long_description,
      long_description_content_type='text/markdown',
      zip_safe=False)
