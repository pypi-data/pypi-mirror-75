import setuptools
import RandomWordGenerator


with open("README.md", "r") as fh:
    long_description = fh.read()


classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Natural Language :: English"
              ]

SHORT_DESC = "This is a random word generator module"

setuptools.setup(
                 name='Random-Word-Generator',
                 version=RandomWordGenerator.__version__,
                 author=RandomWordGenerator.__author__,
                 author_email="abhishek.c.salian@gmail.com",
                 description=SHORT_DESC,
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 url="https://github.com/AbhishekSalian/Random-Word-Generator",
                 packages=setuptools.find_packages(exclude=["*tests*",
                                                            "*image*"]),
                 package=["RandomWordGenerator"],
                 package_data={'': ['LICENSE', 'README.md']},
                 classifiers=classifiers,
                 python_requires=">=3",
                 zip_false=False
                )
