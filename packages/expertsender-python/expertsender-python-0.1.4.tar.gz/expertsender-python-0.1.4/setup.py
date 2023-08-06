from distutils.core import setup
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='expertsender-python',
    packages=['expertsender'],
    version='0.1.4',
    license='MIT',
    description='An unofficial API wrapper for Expertsender',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Karsten Eckhardt',
    author_email='karsten.eckhardt@gmail.com',
    url='https://github.com/r4h4/Expertsender-Python',
    download_url='https://github.com/r4h4/Expertsender-Python/archive/v0.1.4.tar.gz',
    keywords=['expertsender', 'email', 'marketing', 'api'],
    install_requires=[
          'requests',
          'lxml'
      ],
    classifiers=[
        'Development Status :: 4 - Beta',  # "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    python_requires='>=3.6'
)
