from pathlib import Path

from setuptools import setup

readme = Path("README.md").read_text()

setup(
    name="voidpop",
    version="0.1.0",
    author="Colin Chan",
    author_email="colinchan@lumeh.org",
    description="Dummy POP3 server that accepts any login and never has any messages",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/kalgynirae/voidpop",
    py_modules=["voidpop"],
    python_requires=">=3.8",
    install_requires=["trio"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    entry_points={"console_scripts": ["voidpop=voidpop:main"]},
)
