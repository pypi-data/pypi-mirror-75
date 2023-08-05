from setuptools import setup, find_namespace_packages

from FlashBootstrap import Version

with open("README.md", "r") as fd:
    longdescription = fd.read()


setup(
    name=Version.NAME,
    version=Version.VERSION_TEXT + Version.EDITION,
    description='Store Flash messages in session data until they are retrieved. Bootstrap compatibility, sticky messages, and more.',
    url=Version.URL,
    author='Emmanuel Essien',
    author_email='emmaessiensp@gmail.com',
    maintainer='Emmanuel Essien',
    maintainer_email='emmaessiensp@gmail.com',
    include_package_data=True,
    packages=find_namespace_packages(include=['*', '']),
    long_description=longdescription,
    long_description_content_type='text/markdown',
    license=Version.LICENSE,
    keywords=Version.KEYWORDS,
    install_requires=['pytonik'],
    zip_safe=False,
    classifiers=[
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Topic :: Office/Business',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python'
    ],
    python_requires='>=2.7, >=2.7.*, >=3.*',
)
