from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='fsdkapi',
    version='0.0.3',
    author='Islomferg',
    packages=['fsdk'],
    description='Fsdk project API',
    zip_safe=False,
    author_email='usfvouhd@gmail.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',
    python_requires='>=3.8',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)