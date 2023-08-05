from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()


setup(name='deepak_test_mypackage',
      version='0.0.2',
      description='demo package',
      long_description=readme(),
      long_description_content_type='text/markdown',    
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
      ],
      keywords='core package',
      url='http://github.com/deepakkochhar11/mypackage',
      download_url='https://github.com/deepakkochhar11/mypackage/archive/0.0.2.tar.gz',
      author='Deepak Kochhar',
      author_email='deepakkochhar11@gmail.com',
      license='MIT',
      packages=['mypackage'],
      install_requires=[],
      include_package_data=True,
      zip_safe=False)