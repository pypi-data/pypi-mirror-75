from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()


setup_args = dict(
    name='legaltechtools',
    version='1.0.1',
    description='Legal Technology scraping and data analysis library',
    long_description_content_type="text/markdown",
    long_description=README,
    license='MIT',
    packages=find_packages(),
    author='Neel Kandlikar, Neeraj Rattehalli, David Fletcher',
    author_email='neelkandlikar@gmail.com',
    keywords=['LegalTech', 'LegalTechTools'],
    url='https://github.com/neelkandlikar/legaltechtools',
    download_url='https://pypi.org/project/legaltechtools/'
)

install_requires = [
    'bs4',
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
