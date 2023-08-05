from setuptools import setup, find_packages
  
with open('requirements.txt') as f: 
    requirements = f.readlines() 

setup(name='kishor-dl',
      version='0.1',
      description='Download 150+ Kishorekantha PDF in one command!',
      url='http://github.com/nahid18/kishor-dl',
      author='Abdullah Al Nahid',
      author_email='nahidpatwary1@gmail.com',
      license='MIT',
      packages=find_packages(),
      entry_points = {
        'console_scripts': ['kishor_dl=kishor_dl.download:kishor'],
      },
      zip_safe=False, install_requires=['requests', 'beautifulsoup4'])