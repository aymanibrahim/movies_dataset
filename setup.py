from setuptools import setup, find_packages

setup(
    name='movie-dataset',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
    ],
    entry_points={
        'console_scripts': [
            'movie-dataset = movie_dataset:main',
        ],
    },
)
