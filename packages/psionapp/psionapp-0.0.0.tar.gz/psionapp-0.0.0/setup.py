from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='psionapp',
    version='0.0.0',
    description='"""A basic application class which other applications can inherit."""',
    # long_description_content_type="text/markdown",
    # long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='jeff watkins',
    author_email='support@bidforgame.com',
    keywords=['Application, User'],
    url='https://github.com/ncthuc/elastictools',
    download_url='https://pypi.org/project/psionapp/'
)

install_requires = [
    'username', 'nose'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)