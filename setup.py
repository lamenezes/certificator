from setuptools import setup, find_packages

with open('requirements.txt') as f:
    install_requires = f.readlines()

setup(
    name='certificator',
    version='0.1.0',
    description='Certificate Generator Tool and Library',
    url='https://github.com/lamenezes/certificator',
    author='Luiz Menezes',
    author_email='luiz.menezesf@gmail.com',
    long_description=open('README.rst').read(),

    packages=find_packages(exclude=['tests*']),
    install_requires=install_requires,
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'certificator=certificator.__main__:main',
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
)
