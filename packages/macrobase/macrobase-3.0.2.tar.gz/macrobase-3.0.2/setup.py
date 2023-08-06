from setuptools import setup, find_packages

requirements = [
    'macrobase-driver>=2.0.0,<3.0.0',
    'structlog==19.2.0',
]

test_requirements = [
    'pytest==5.4.3',
    'pytest-cov==2.10.0',
    'pytest-cov==2.10.0',
    'pytest-timeout==1.4.1',
    'pytest-mock==3.1.1',
    'pytest-mock==3.2.0',
]

dev_requirements = test_requirements + [
    'flake8==3.8.3',
    'flake8-import-order==0.18.1'
]


setup(
    name='macrobase',
    version='3.0.2',
    packages=find_packages(),
    url='https://github.com/mbcores/macrobase',
    license='MIT',
    author='Alexey Shagaleev',
    author_email='alexey.shagaleev@yandex.ru',
    description='Macrobase framework for build mAcroservices',
    install_requires=requirements,
    extras_require={
        'dev': dev_requirements,
        'test': test_requirements,
    }
)
