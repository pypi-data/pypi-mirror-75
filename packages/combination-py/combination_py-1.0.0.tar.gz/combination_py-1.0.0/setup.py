import setuptools


def main():
    with open('README.md', 'r') as fp:
        readme = fp.read()

    setuptools.setup(
        name='combination_py',
        version='1.0.0',
        description='Python package for combination calculation',
        long_description=readme,
        long_description_content_type='text/markdown',
        url='https://github.com/m-star18/combination_py',
        license='Apache Software License 2.0',
        author='Ryusei Ito',
        author_email='31807@toyota.kosen-ac.jp',
        packages=['combination'],
        python_requires='>=3.6, <3.9'
    )


main()
