from distutils.spawn import find_executable
import os
from setuptools.command.test import test as TestCommand

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

# Inspired by the example at https://pytest.org/latest/goodpractises.html
class NoseTestCommand(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # Run nose ensuring that argv simulates running nosetests directly
        import nose
        nose.run_exit(argv=['nosetests'])

class ApiDocCommand(TestCommand):
    def run(self):
        if find_executable('apidoc') is not None:
            os.system("apidoc -i RemoteDslrApi/ -o docs/api/ --verbose")
            print("api documentation generated in docs/api/")
        else:
            print("apidoc is not installed, please run `npm install apidoc -g`")

setup(
    description='control your DSLR Camera over HTTP',
    long_description=read('README.md'),
    include_package_data=True,
    author='Tobias Scheck',
    url='http://www.scheck-media.de',
    download_url='Where to download it.',
    author_email='tobias@scheck-media.de',
    version='0.1',
    install_requires=['nose', 'gphoto2', 'flask', 'pillow', 'zeroconf'],
    packages=['RemoteDslrApi'],
    tests_require=['Mock'],
    scripts=[],
    name='RemoteDslrApi',
    setup_requires=['nose>=1.3'],
    cmdclass={'test': NoseTestCommand, 'apidoc': ApiDocCommand }
)
