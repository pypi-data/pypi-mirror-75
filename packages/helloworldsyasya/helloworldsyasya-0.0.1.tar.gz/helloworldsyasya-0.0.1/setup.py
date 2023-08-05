from setuptools import setup

with open("readme.md", "r") as fh:
        long_description = fh.read()

setup(
        name='helloworldsyasya',
        version='0.0.1',
        description='Say hello!',
        py_modules=["helloworldsyasya"],
        package_dir={'': 'src'},
        
        classifier=[
                "Programming Language :: Python :: 3",
                "Programming Language :: Python :: 3.6",
                "Programming Language :: Python :: 3.7",
                "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
                "Operating System :: OS Independent",
        ],

        long_description=long_description,
        long_description_content_type="text/markdown",

        install_requires = [
                "blessings ~= 1.7",
        ],

        extra_require = {
                "dev": [
                        "pytest>=3.7",
                ],
        },

        author="Syasya Putri",
        auhor_email="syasyaputri@gmail.com"

)