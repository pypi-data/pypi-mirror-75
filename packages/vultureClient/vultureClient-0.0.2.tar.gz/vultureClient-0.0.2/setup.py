from setuptools import find_packages, setup

setup(
    name='vultureClient',
    version='0.0.2',
    description='vulture-client: To fetch data from Vulture',
    packages=find_packages(where='.', include=['vulture.libs.fetch_functions']),
    install_requires=[
        "pandas>=1.0.3"
    ],
    zip_safe=True
)
