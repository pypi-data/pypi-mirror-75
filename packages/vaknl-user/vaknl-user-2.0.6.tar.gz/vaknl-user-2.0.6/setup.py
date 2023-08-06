from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

REQUIRED_PACKAGES = [
    'google-auth==1.18.0',
    # 'firebase-admin==4.3.0',
    'google-cloud-firestore==1.8.1',
    'typing-extensions==3.7.4.2',
    'dacite==1.5.1',
]

REQUIRED_PACKAGES_SETUP = [
    'setuptools',
    'wheel',
]

setup(
    name='vaknl-user',
    description='User class that defines a user based on clickstream data.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    version='2.0.6',
    url='https://github.com/vakantiesnl/vaknl-PyPi.git',
    author='Merijn van Es',
    author_email='merijn.vanes@vakanties.nl',
    keywords=['vaknl', 'pip'],
    packages=find_packages(exclude=['tests*']),
    python_requires='>=3.7',
    install_requires=REQUIRED_PACKAGES,
    setup_requires=REQUIRED_PACKAGES_SETUP,
)
