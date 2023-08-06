from setuptools import setup, find_packages

setup(
    name='aiotrivia',
    url='https://github.com/niztg/aiotrivia',
    version='1.2.2',
    license='MIT',
    project_urls={'Discord Server': 'https://discord.com/invite/2fxKxJH'},
    description='Asynchronous API Wrapper for the OpenTDB Api. (https://opentdb.com/)',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['aiohttp'],
    python_requires='>=3.5.3',
    keywords=['trivia', 'api', 'trivia_api', 'opentdb']
)