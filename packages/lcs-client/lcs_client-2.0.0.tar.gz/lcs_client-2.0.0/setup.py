import pathlib

from setuptools import setup

CURR_DIR = pathlib.Path(__file__).parent
README = (CURR_DIR / "README.md").read_text()

setup(
        name='lcs_client',
        version='2.0.0',
        packages=['lcs_client'],

        install_requires=['requests>=2.0'],

        description='Client for interacting with LCS, the HackRU backend',
        long_description=README,
        long_description_content_type='text/markdown',
        url='https://github.com/HackRU/python-lcs-client',
        author='HackRU RnD',
        author_email='rnd@hackru.org',
        license='MIT',
        classifiers=[
            'Development Status :: 4 - Beta',
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: MIT License'
        ],

        include_package_data=True,
        extras_require={
            'dev': [
                'pytest~=6.0', 'pytest-mock~=3.2', 'pydoc-markdown~=3.3'
            ],
            'build': [
                'wheel~=0.34', 'twine~=3.2'
            ]
        },
)
