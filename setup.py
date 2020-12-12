import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='holiday_api',
    version='0.0.1',
    author='isaz-co',
    author_email='ivan.sylkin.k@gmail.com',
    description='API for getting holiday information',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/isaz-co/holiday-api',
    packages_dir={'': 'holiday_api'},
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.8',
)
