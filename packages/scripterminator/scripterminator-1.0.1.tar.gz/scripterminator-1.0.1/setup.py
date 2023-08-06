from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='scripterminator',
    version='1.0.1',
    description='Useful tool to terminate any Python script just using file path and name',
    long_description_content_type="text/markdown",
    long_description=README,
    license='MIT',
    packages=find_packages(),
    author='Shahmin Rahman Rinkey',
    author_email='shahminrinkey02@gmail.com',
    keywords=['process', 'psutil', 'pid', 'terminate', 'system', 'utility', 'os'],
    url='https://github.com/shahminrinkey/scripterminator',
    download_url='https://pypi.org/project/scripterminator/'
)

install_requires = [
    'psutil',
    'subprocess',
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)