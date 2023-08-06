from setuptools import find_namespace_packages, setup


TEST_REQUIRES = ["pytest>=5.3.5", "responses>=0.10.14", "freezegun>=0.3.15"]


VERSION = "1.0.0"
setup(
    name="panoramic-auth",
    description="Panoramic Authentication SDK",
    url="https://github.com/panoramichq/panoramic-auth-py",
    project_urls={"Source Code": "https://github.com/panoramichq/panoramic-auth-py"},
    author="Panoramic",
    maintainer="Panoramic",
    keywords=["panoramic", "authentication", "sdk"],
    version=VERSION,
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_namespace_packages(where='src', include=["panoramic.*"]),
    package_dir={"": "src"},
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=['requests_oauthlib>=1.3.0'],
    extras_require={"tests": TEST_REQUIRES, "dev": TEST_REQUIRES + ["pre-commit>=2.1.1"]},
    include_package_data=True,
)
