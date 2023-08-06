""" Unit provisioning tool
--------------------------
The tool that helps to provision units to the Aos cloud
"""

from setuptools import setup, find_packages
from aos_provisioning import __version__


def _get_required_packages():
    with open('requirements.txt') as f:
        return f.read().splitlines()


setup(
    name="aos-provisioning",
    version=__version__,
    license="Apache License 2.0",
    author="EPAM Systems",
    author_email="support@aoscloud.io",
    description="Aos provisioning tool",
    long_description=__doc__,
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=_get_required_packages(),
    platforms="any",
    entry_points={
        'console_scripts': [
            'aos-provisioning=aos_provisioning.main:main'
        ]
    },
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3"
    ]
)
