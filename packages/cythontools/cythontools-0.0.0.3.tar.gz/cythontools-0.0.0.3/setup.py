from setuptools import setup

setup(
    name='cythontools',
    version='0.0.0.3',
    packages=['cythontools', 'cythontools.command'],
#    url='https://github.com/cacticouncil/herptest',
    license='GPL 3',
    author='Jeremiah Blanchard',
    author_email='jjb@eng.ufl.edu',
    description='Tools for building and testing Cython projects',
    install_requires=[],

#    entry_points =
#    { 'console_scripts':
#        [
#            'elma = herptest.extract_lms_archive:main',
#            'herp = herptest.run_test_suite:main'
#        ]
#    }
)
