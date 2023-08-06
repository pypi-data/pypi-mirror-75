import setuptools

with open('README.md', 'r') as rm:
    long_description = rm.read()

setuptools.setup(
    name='multiranges',
    version='0.0.2',
    author='Enzo Conejero',
    author_email='enzoconejero0@gmail.com',
    description='MultiRanges',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/enzoconejero/multiranges.git',
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.6',
)
