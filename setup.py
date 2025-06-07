from setuptools import setup, find_packages


setup(
    name="studybuddy",
    version="0.0.1",
    packages=find_packages(),
    install_requires=open("requirements.txt").readlines(),
    entry_points={
        'console_scripts': [
            'studybuddy = studybuddy.studybuddy:main',
        ],
    },
    # PyPI metadata
    author="Nellogan",
    description="Optimize Leetcode study sessions by scraping provided URLs to local files with preconfigured "
                "imports/includes and supporting build files. Generates a log header per file and a consolidated "
                "log file in the destination directory.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/nellogan/studybuddy",
    project_urls={
        "Source": "https://github.com/nellogan/studybuddy",
        "Bug Tracker": "https://github.com/nellogan/studybuddy/issues",
        "Documentation": "https://github.com/nellogan/studybuddy#readme",
    },
    license="Apache-2.0",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Operating System :: Linux",
    ],
    python_requires=">=3.13",
    keywords="studybuddy, Selenium, Leetcode, scraping, tool, automation, education",
)
