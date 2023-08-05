from setuptools import setup, find_packages

# with open('README.md') as readme_file:
#     README = readme_file.read()

# with open('HISTORY.md') as history_file:
#     HISTORY = history_file.read()

setup_args = dict(
    name='emailverf',
    version='0.1',
    description='Useful tool to verifiy email addresses and their domains.',
    # long_description_content_type="text/markdown",
    # long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='Siddhartha Sehgal',
    author_email='siddhartha.sehgal94@gmail.com',
    keywords=['email', 'verify', 'verification'],
    url='https://github.com/okaysidd/emailverf',
    download_url='https://pypi.org/project/emailverf/'
)

install_requires = [
	'certifi==2020.6.20',
	'chardet==3.0.4',
	'dnspython==2.0.0',
	'idna==2.10',
	'numpy==1.19.1',
	'pandas==1.0.5',
	'python-dateutil==2.8.1',
	'pytz==2020.1',
	'requests==2.24.0',
	'requests-file==1.5.1',
	'secure-smtplib==0.1.1',
	'six==1.15.0',
	'sockets==1.0.0',
	'tldextract==2.2.2',
	'urllib3==1.25.10'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
