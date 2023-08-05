import setuptools
from subprocess import check_output


with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    requirements = fh.read().split("\n")
    requirements = [r for r in requirements if r != "" ]

def git_tag():
    try:
       tag = check_output(['git','describe','--tags'])
       tag = tag.decode('ascii')[:-1]
    except:
       tag = 'v0.0.0'
    print("Getting git tag: " + tag)
    return tag
    
setuptools.setup(
    name="evalgraph", # Replace with your own username
    version=git_tag()[1:],
    author="Joel Horowitz",
    author_email="joelhoro@gmail.com",
    description="Graph based evaluator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/joelhoro/graph",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
