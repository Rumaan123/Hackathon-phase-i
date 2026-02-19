from setuptools import setup, find_packages

setup(
    name="todo-app",
    version="1.0.0",
    description="A basic console-based todo application",
    author="Hackathon Team",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    python_requires='>=3.10',
    entry_points={
        'console_scripts': [
            'todo-app=main:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)