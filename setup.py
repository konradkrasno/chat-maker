from setuptools import find_packages, setup

setup(
    name="chat_maker",
    version="0.1",
    package_dir={"": "."},
    packages=find_packages(where="."),
    python_requires=">=3.6",
    install_requires=["marshmallow", "boto3"],
    entry_points={"console_scripts": ["chatmaker = chat_maker.main:main"]},
)
