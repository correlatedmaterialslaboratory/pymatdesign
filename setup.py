from setuptools import setup


def open_readme():
    with open("README.md") as f:
        text = f.read()
    return text


setup(
    name = 'pymatdesign',
    version = '0.1',
    description = 'Python Materials Design',
    long_description = open_readme(),
    url = 'http://github.com/correlatedmaterialslaboratory/pymatdesign',
    author = 'Chuck-Hou Yee',
    author_email = 'chuckyee@physics.rutgers.edu',
    license = 'MIT',
    packages = ['pymatdesign'],
    install_requires = ['pymatgen']
    )
