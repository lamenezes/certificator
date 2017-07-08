from setuptools import setup, find_packages

setup(
    name='certificator',
    version='0.0.1',
    description='Certificate Generator for Python',
    url='https://github.com/lamenezes/certificator',
    author='Luiz Menezes',
    author_email='luiz.menezesf@gmail.com',
    long_description=open('README.rst').read(),
    packages=find_packages(exclude=['tests*']),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
)
