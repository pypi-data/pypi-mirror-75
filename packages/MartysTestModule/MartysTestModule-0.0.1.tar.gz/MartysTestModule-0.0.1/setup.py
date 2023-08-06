from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='MartysTestModule',
    version='0.0.1',
    description='Test Take 2',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='Marty DeWitt',
    author_email='martydewitt2015@gmail.com'
    #keywords=['Elastic', 'ElasticSearch', 'ElasticStack'],
    #url='https://github.com/ncthuc/elastictools'
    #download_url='https://pypi.org/project/elastictools/'
)


if __name__ == '__main__':
    setup(**setup_args)#, install_requires=install_requires)