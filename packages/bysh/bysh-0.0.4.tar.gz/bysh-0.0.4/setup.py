import setuptools
import bysh

with open('README.md', 'r') as f:
    long_description = f.read()

with open('requirements.txt', 'r') as f:
    requirements = list(f.readlines())

setuptools.setup(
    name='bysh',
    version=bysh.__version__,
    author='haytek',
    author_email='haytek34@gmail.com',
    description='The unstable bash',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/haytek/bysh',
    packages=setuptools.find_packages(exclude=('tests', 'tests.*')),
    classifiers=[
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'bysh = bysh.__main__:console_run'
        ]
    }

)
