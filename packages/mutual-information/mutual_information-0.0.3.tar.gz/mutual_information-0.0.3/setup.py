from setuptools import setup


with open('./README.md', 'r') as f:
    long_description = f.read()


setup(
    name='mutual_information',
    version='0.0.3',
    description='mutual information-based synergy between variables for one response',
    py_modules=["mf"],
    package_dir={'': 'src/python'},
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        "numpy ~= 1.7",
        "pandas ~= 0.24",
        "networkx ~= 2.2",
        "treelib ~= 1.5.5"

    ],
    extras_require={
        "dev" : [
            "pytest >= 3.7",
            "check-manifest==0.42"
        ]
    },
    url='https://github.com/kingmanzhang/mutual-information',
    author='Xingmin A Zhang',
    author_email='kingmanzhang@gmail.com',
)