import setuptools

with open("holger/README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="holger-utils",
    version="0.5.0",
    author="Mohammad Hosein Shamsaei",
    author_email="holgerco.dev@gmail.com",
    description="utils for developing web application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/football-fantasy/holger-utils",
    install_requires=[
        'requests',
        'djangorestframework',
        'elasticsearch[async]',
        'celery',
        'sentry-sdk',
        'python-dateutil',
        'firebase-admin',
        'google-api-python-client'
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        'Environment :: Web Environment',
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: MIT License',
        "Operating System :: OS Independent",
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
    ],
    python_requires='>=3.6',
)

# py setup.py sdist bdist_wheel
# twine upload dist/*
