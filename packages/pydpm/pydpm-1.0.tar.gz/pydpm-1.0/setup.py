from setuptools import setup

setup(
    name='pydpm',
    version='1.0',
    license = "Apache License Version 2.0",
    url = "https://github.com/BoChenGroup/pydpm/",
    author = "Jiawen Wu, Chaojie Wang ",
    author_email = "wjw19960807@163.com, xd_silly@163.com",
    packages=['pydpm', 'pydpm.layer', 'pydpm.utils', 'pydpm.distribution', 'pydpm.model','pydpm.example'],
    description='A probabilistic model package based on pycuda',
    install_requires=['numpy','scipy','pycuda'],
    package_data ={"pydpm.utils":['*.so','*.dll']}
)
