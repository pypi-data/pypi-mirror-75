from setuptools import setup, find_packages

setup(
    # 모듈명
    name='auto_digo',
    version='0.0.2',
    author='DiggerWorks',
    author_email='kunka8271@gmail.com',
    description='automatic ml module',
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "auto-digo = auto_digo.main:main"
        ]
    },
    install_requires=['argparse']
)
