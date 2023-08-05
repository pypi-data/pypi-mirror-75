import pathlib
import setuptools

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setuptools.setup(
    name="testoy",
    version="0.0.1",
    description="Test your code with countless toys!",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/pricelesscode/testoy",
    author="Matt Lee",
    author_email="poream3387@gmail.com",
    license="MIT",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    
    python_requires='>=3.6.4',
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=["pytest"],
)

print(__file__)
