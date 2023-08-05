from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='pair_learning',
    version='0.1.1',
    description='The easiest way to use deep metric learning for pair data. Written in PyTorch.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/rikiyasuzuki/pair_learning',
    author='Rikiya Suzuki',
    author_email='rikiyasuzuki1112@gmail.com',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    keywords='metric_learning, torch',
    packages=find_packages(exclude=['tests*']),
    python_requires='>=3.0',
    install_requires=[
        'numpy',
        'torch'
    ]
)