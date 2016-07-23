from setuptools import setup, find_packages

setup(
    name = 'gotchatwitter',
    version = '0.0.28',
    keywords = ('twitter', 'python', 'crawler', 'web-scraping'),
    description = 'Crawling twitter in Python',
    license = 'MIT License',
    install_requires = ['bs4', 'tqdm', 'requestsplus', 'lxml'],
    include_package_data=True,
    zip_safe=True,

    author = 'cchen224',
    author_email = 'phantomkidding@gmail.com',

    url = 'https://github.com/PhantomKidding/GotchaTwitter',

    packages = find_packages(),
    platforms = 'any',
)