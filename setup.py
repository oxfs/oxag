from setuptools import setup, find_packages

setup(
    name='oxag',
    version='0.0.1',
    author='RainMark',
    author_email='rain.by.zhou@gmail.com',
    description='Oxfs Agent Server',
    url='https://github.com/RainMark/oxag',
    classifiers=[
        'Operating System :: Unix',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: MIT License',
    ],

    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires = [
        'flask-restplus >= 0.12.1',
    ],

    entry_points={
        'console_scripts':[
            'oxag = oxag:main'
        ]
    },
)
