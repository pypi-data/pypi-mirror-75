from setuptools import setup
from setuptools import find_packages

setup(name='rura',
      version='0.2.1',
      packages=find_packages(),
      license='MIT',
      description='Pipelines for machine learning',
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      author='Filip Dabek',
      url='https://github.com/fdabek1/rura',
      download_url='https://github.com/fdabek1/rura/archive/0.2.1.tar.gz',
      keywords=['machine learning', 'pipeline', 'etl'],
      install_requires=[
          'mlflow',
          'numpy>=1.9.1',
          'scipy>=0.14',
          'six>=1.9.0',
          'pyyaml',
          'h5py',
          'python-dotenv',
      ],
      extras_require={
          'tests': ['pytest',
                    'pytest-pep8',
                    'pytest-xdist',
                    'flaky',
                    'pytest-cov',
                    'pandas',
                    'requests',
                    'markdown'],
      },
      classifiers=[  # Optional
          # How mature is this project? Common values are
          #   3 - Alpha
          #   4 - Beta
          #   5 - Production/Stable
          'Development Status :: 3 - Alpha',

          # Indicate who your project is intended for
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Build Tools',

          # Pick your license as you wish
          'License :: OSI Approved :: MIT License',

          # Specify the Python versions you support here. In particular, ensure
          # that you indicate whether you support Python 2, Python 3 or both.
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.8',
      ])
