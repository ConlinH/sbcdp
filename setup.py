"""
SBCDP setup.py
传统安装方式支持
"""

from setuptools import setup, find_packages
import os


# 读取版本信息
def get_version():
    version_file = os.path.join(os.path.dirname(__file__), 'sbcdp', '__version__.py')
    with open(version_file, 'r', encoding='utf-8') as f:
        exec(f.read())
    return locals()['__version__']


# 读取README
def get_long_description():
    readme_file = os.path.join(os.path.dirname(__file__), 'README.md')
    with open(readme_file, 'r', encoding='utf-8') as f:
        return f.read()


# 读取requirements
def get_requirements():
    requirements_file = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(requirements_file):
        with open(requirements_file, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return [
        "requests",
        "loguru",
        "mycdp>=1.0.0",
        "cssselect>=1.3.0",
        "fasteners>=0.19",
        "colorama>=0.4.6",
        "websockets>=11.0.3",
    ]


setup(
    name="sbcdp",
    version=get_version(),
    description="SBCDP - Pure CDP (Chrome DevTools Protocol) Automation Framework",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="conlin",
    author_email="995018884@qq.com",
    url="https://github.com/ConlinH/sbcdp",
    project_urls={
        "Homepage": "https://github.com/ConlinH/sbcdp",
        "Source": "https://github.com/ConlinH/sbcdp",
        "Repository": "https://github.com/ConlinH/sbcdp",
        "Bug Tracker": "https://github.com/ConlinH/sbcdp/issues",
        "Documentation": "https://github.com/ConlinH/sbcdp#readme",
    },
    packages=find_packages(exclude=["tests", "tests.*"]),
    package_data={
        "sbcdp": ["*.txt", "*.md"],
    },
    include_package_data=True,
    install_requires=get_requirements(),
    extras_require={
        "test": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.0.0",
        ],
    },
    python_requires=">=3.8",
    keywords=[
        "automation",
        "cdp", 
        "chrome",
        "devtools",
        "browser",
        "scraping",
        "testing",
        "async",
        "sync"
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Framework :: Pytest",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Internet",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Testing :: Acceptance",
        "Topic :: Software Development :: Testing :: Traffic Generation",
        "Topic :: Utilities",
    ],
    license="MIT",
    zip_safe=False,
)
