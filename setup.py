"""Setup script for English Text Analyzer."""

from setuptools import setup, find_packages
import os

# Read version from package
def get_version():
    version_file = os.path.join('english_text_analyzer', '__init__.py')
    with open(version_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('__version__'):
                return line.split('=')[1].strip().strip('"\'')
    return '1.0.0'

# Read long description from README
def get_long_description():
    if os.path.exists('README.md'):
        with open('README.md', 'r', encoding='utf-8') as f:
            return f.read()
    return "Comprehensive English text analysis tool for educational purposes."

setup(
    name="english-text-analyzer",
    version=get_version(),
    author="English Text Analysis Team",
    author_email="team@englishanalyzer.com",
    description="Comprehensive English text analysis tool for educational purposes",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/english-text-analyzer",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Education",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=[
        "langextract>=0.1.0",
        "pyyaml>=6.0",
        "numpy>=1.20.0",
        "reportlab>=3.6.0",  # For PDF generation
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
        "web": [
            "flask>=2.0.0",
            "jinja2>=3.0.0",
        ],
        "all": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
            "flask>=2.0.0",
            "jinja2>=3.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "eta=english_text_analyzer.cli.main:main",
            "english-text-analyzer=english_text_analyzer.cli.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "english_text_analyzer": [
            "templates/*.html",
            "static/*.css",
            "static/*.js",
            "config/*.yaml",
            "config/*.json",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/your-org/english-text-analyzer/issues",
        "Source": "https://github.com/your-org/english-text-analyzer",
        "Documentation": "https://english-text-analyzer.readthedocs.io/",
    },
)