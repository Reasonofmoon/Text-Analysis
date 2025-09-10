"""Setup script for English Text Analyzer package."""

from setuptools import setup, find_packages
import os

# Read README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "English Text Analyzer - A comprehensive tool for analyzing English texts using langextract."

# Read requirements
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

setup(
    name="english-text-analyzer",
    version="0.1.0",
    author="English Text Analysis Team",
    author_email="team@englishanalyzer.com",
    description="A comprehensive tool for analyzing English texts using langextract",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/english-text-analyzer",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
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
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
        "viz": [
            "matplotlib>=3.5.0",
            "seaborn>=0.11.0",
            "plotly>=5.0.0",
        ],
        "pdf": [
            "reportlab>=3.6.0",
            "weasyprint>=56.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "english-text-analyzer=english_text_analyzer.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "english_text_analyzer": [
            "config/*.yaml",
            "templates/*.html",
            "static/*",
        ],
    },
    zip_safe=False,
)