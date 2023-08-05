from setuptools import setup, find_packages

classifiers = [
             'Development Status :: 5 - Production/Stable',
             'Intended Audience :: Education',
             'Operating System :: Microsoft :: Windows :: Windows 10',
             'Programming Language :: Python :: 3'
            ]

setup(
            name='mgoelAuto',
            version= '0.0.2',
            description='basic',
            Long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
            url='',
            author='application',
            license='ineuron-ip',
            classifiers=classifiers,
            package=find_packages,
            install_requires=['click', 'six', 'numpy', 'future'],
            setup_requires=['pytest-runner'],
            # pytest-cov needed for coverage only
            tests_require=['pytest', 'pytest-cov'],
            zip_safe=True
)