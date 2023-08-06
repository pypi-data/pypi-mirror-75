from setuptools import setup
from setuptools import find_packages

REQUIRED_PACKAGES = [
    'pandas-gbq>=0.13.2',
    'pathlib',
    'google-cloud-datastore','google-cloud-bigquery','google-cloud-storage','tqdm','google-cloud-bigquery-storage',
    'pyarrow'
]

setup(name='humailib',
      version='1.0.2',
      description='HUMAI framework package',
      url='',
      author='HUMAI',
      author_email='willem@humai.nl',
      license='',
      install_requires=REQUIRED_PACKAGES,
      packages=find_packages(),
      zip_safe=False)