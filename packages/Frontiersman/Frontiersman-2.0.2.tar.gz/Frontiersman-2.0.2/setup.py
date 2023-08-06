import io

from setuptools import setup, find_packages

setup(
    name="Frontiersman",
    version="2.0.2",
    author="Brian Snow",
    author_email="snowb@ufl.edu",
    description="Network Multiplayer Board Game",
    install_requires=['pygame>=2.0.0.dev10', 'pygame_gui', 'aiohttp', 'asyncio', 'requests'],
    long_description=io.open(
        './README.md', 'r', encoding='utf-8').read(),
    url="https://gitlab.com/csi4930-frontiersman/csi4930-frontiersman",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['*.png', '*.json', '*.ttf', '*.txt'],
    },
    setup_requires=["setuptools_git >= 0.3", ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'FMClient = frontiersman.ClientMain:main',
            'FMServer = frontiersman.server:main'
        ],
    }
)
