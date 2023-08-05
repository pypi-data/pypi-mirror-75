from setuptools import setup, find_packages

classifiers = [
             'Development Status :: 5 - Production/Stable',
             'Intended Audience :: Education',
             'Operating System :: Microsoft :: Windows :: Windows 10',
             'Programming Language :: Python :: 3'
            ]

setup(
            name='Autoneuro',
            version= '0.0.1',
            description='basic',
            Long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
            url='',
            author='application',
            license='ineuron-ip',
            classifiers=classifiers,
            package=find_packages,
            install_requires=['']
)