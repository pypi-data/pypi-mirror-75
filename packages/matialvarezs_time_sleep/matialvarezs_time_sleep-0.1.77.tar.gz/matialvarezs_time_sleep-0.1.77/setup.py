from distutils.core import setup

setup(
    name='matialvarezs_time_sleep',
    packages=['matialvarezs_time_sleep'],  # this must be the same as the name above
    version='0.1.77',
    install_requires=[
        'matialvarezs-request-handler==0.1.7',
        'matialvarezs-handlers-easy==0.1.50',
        'django-ohm2-handlers-light==0.1.21',
        'paho-mqtt==1.5.0'
    ],
    description='Long time sleep divided into small times',
    author='Matias Alvarez Sabate',
    author_email='matialvarezs@gmail.com',
    # url = 'https://github.com/peterldowns/mypackage', # use the URL to the github repo
    # download_url = 'https://github.com/peterldowns/mypackage/archive/0.1.tar.gz', # I'll explain this in a second
    # keywords = ['testing', 'logging', 'example'], # arbitrary keywords
    classifiers=[],
)
