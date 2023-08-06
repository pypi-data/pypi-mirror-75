from setuptools import setup, find_packages


with open("README.md", "r") as file:
    long_description = file.read()

setup(
    name='git-prune',
    packages=find_packages(exclude="tests"),
    license="MIT",
    version='0.0.1',
    description='Clean up your local git branches with one command',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Richard Soper',
    author_email='',
    url='https://github.com/rsoper/git-prune',
    install_requires=[],
    package_data={},
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'git-prune=git_prune_src.main:main'
        ]
    },
)