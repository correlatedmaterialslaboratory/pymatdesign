from setuptools import setup

setup(
    name = 'pymatdesign',
    version = '0.1',
    description = 'Python Materials Design',
    url = 'http://github.com/correlatedmaterialslaboratory/pymatdesign',
    author = 'Chuck-Hou Yee',
    author_email = 'chuckyee@physics.rutgers.edu',
    license = 'MIT',
    packages = ['pymatdesign'],
    install_requires = ['pymatgen']
    )
