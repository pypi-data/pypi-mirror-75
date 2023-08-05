import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="glagolitic-transliter",
    version="1.0",
    author="IlhomBahoraliev",
    author_email="bahoralievdev@yandex.com",
    description="Простой транслитератор кириллицы в глаголицу.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IlhomBahoraliev/glagolitic-translit",
    packages=["gltransliter"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
