from setuptools import setup

setup(name='pyatm',
      version='0.2',
      
      description='ATM (Automatic Teller machine) testing library and tools',
      long_description=open('README.rst').read(),
      
      classifiers=[
        'License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)',
        'Operating System :: OS Independent',
        
        'Programming Language :: Python :: 3',
        
        'Topic :: Communications',
        'Intended Audience :: Developers',
      ],
      
      keywords='ATM banking financial',
      
      url='https://github.com/timgabets/pyatm',
      author='Tim Gabets',
      author_email='tim@gabets.ru',
      
      license='LGPLv2',
      packages=['pyatm'],
      install_requires=['tracetools'],
      zip_safe=True)