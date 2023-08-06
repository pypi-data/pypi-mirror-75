from setuptools import setup

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name="sphinx_fasvg",
    version="0.1.3",
    url="https://procrastinator.nerv-project.eu/nerv-project/sphinx_fasvg",
    license="EUPL 1.2",
    author="Kujiu",
    author_email="kujiu-pypi@kujiu.org",
    description="Use font-awesome icons in SVG form",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    packages=["sphinx_fasvg"],
    package_data={
        "sphinx_fasvg": [
            "*.py",
        ]
    },
    entry_points={"sphinx.html_themes": ["nervproject = sphinx_nervproject_theme"]},
    install_requires=["sphinx>=2.0.0"],
    classifiers=[
        "Framework :: Sphinx",
        "Framework :: Sphinx :: Extension",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "Topic :: Documentation",
        "Topic :: Software Development :: Documentation",
    ],
    keywords="sphinx fontawesome svg",
    project_urls={
        "Source": "https://procrastinator.nerv-project.eu/nerv-project/sphinx_fasvg",
        "Issues": "https://procrastinator.nerv-project.eu/nerv-project/sphinx_fasvg/issues",
    },
)
