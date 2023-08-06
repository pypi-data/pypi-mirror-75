import setuptools

setuptools.setup(
    name="col",
    version="0.0.1",
    author="Daan Klijn",
    author_email="daanklijn0@gmail.com",
    description="Collections for Python",
    url="https://github.com/daanklijn/col",
    packages=setuptools.find_packages(exclude=['tests']),
    python_requires='>=3.6',
)
