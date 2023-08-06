from setuptools import setup
import os

exec(open('flagger/version.py').read())

lib_folder = os.path.dirname(os.path.realpath(__file__))
requirement_path = lib_folder + '/requirements-dev.txt'
test_requires = []
if os.path.isfile(requirement_path):
    with open(requirement_path) as f:
        test_requires = f.read().splitlines()

setup(
    name='flagger',
    packages=['flagger'],
    version=__flagger_version__,
    description='An open source Python SDK for feature flagging (feature gating, feature toggles)',
    maintainer='engineering',
    license='MIT',
    maintainer_email='engineering@airdeploy.io',
    long_description='An open source Python SDK for feature flagging (feature gating, feature toggles). \n'
                     'Documentation available at https://docs.airdeploy.io',
    url='https://airdeploy.io',
    include_package_data=True,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    tests_require=test_requires
)
