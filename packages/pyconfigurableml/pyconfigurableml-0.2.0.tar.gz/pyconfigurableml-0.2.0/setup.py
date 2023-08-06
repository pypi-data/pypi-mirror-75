import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / 'README.md').read_text()

setup(
    name='pyconfigurableml',
    version='0.2.0',
    description='Configurable ML in Python',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/dkmiller/pyconfigurableml',
    author='Daniel Miller',
    author_email='daniel.keegan.miller@gmail.com',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    packages=['pyconfigurableml'],
    include_package_data=True,
    install_requires=['typeguard>=2.9.1', 'pyyaml>=5.3.1'],
    # https://setuptools.readthedocs.io/en/latest/setuptools.html#declaring-extras-optional-features-with-their-own-dependencies
    extra_requires={
        'azure': ['azure-identity>=1.3.1', 'azure-keyvault-secrets>=4.1.0'],
        'munch': ['munch>=2.5.0']
    },
    # https://stackoverflow.com/a/48777286
    python_requires='~=3.6',
)
