from setuptools import find_packages, setup

setup(
    name='ticket_man',
    version='0.0.1',
    url='https://github.com/IotaSpencer/ticket_man',
    license='MIT',
    author='IotaSpencer',
    author_email='me@iotaspencer.me',
    description='Ticket Manager for IotaSpencer\'s projects',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.10.4",
    install_requires=[
        'asyncclick',
        'py-cord'
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'ticket_man = ticket_man.scripts.main:start'
        ],
    },
)
