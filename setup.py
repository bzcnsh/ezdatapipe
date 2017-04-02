from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='ezdatapipe',
    version='0.0.2',
    description='collection of scripts for structured data processing',
    long_description=readme(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities',
    ],
    keywords='structured data pipeline',
    url='https://github.com/bzcnsh/ezdatapipe.git',
    author='Yimin Zheng',
    author_email='bzcnsh@yahoo.com',
    test_suite='nose.collector',
    tests_require=['nose'],

    license='MIT',
    packages=['ezdatapipe'],
    install_requires=[
        'jinja2',
        'pyyaml',
        'toml'
    ],
    zip_safe=False)
