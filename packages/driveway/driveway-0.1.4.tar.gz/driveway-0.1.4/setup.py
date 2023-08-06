import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="driveway",  # Replace with your own username
    version="0.1.4",
    author="Andres Canas, Henry Parker, Dylan Fay, Zack Saadioui",
    description="Driveways Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/henryparker/drivewaynew",
    packages=['drive', 'userface', 'sample_app', ],
    py_modules=["manage"],
    include_package_data=True,
    install_requires=['asgiref', 'astroid', 'certifi', 'Django', 'django-crispy-forms', 'django-leaflet',
                      'geographiclib', 'geopy', 'idna', 'psycopg2-binary', 'pytz', 'requests>=2.24.0', 'six',
                      'sqlparse', 'toml', 'urllib3', 'wrapt', 'Pillow', 'geoip2'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',

    entry_points=

    {'console_scripts':

        [

            'runmyserver = sample_app.run:main',

        ]

    },
)
