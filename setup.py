from setuptools import setup, find_packages

setup(
    name="backtest",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "sqlalchemy",
        "python-dotenv",
        "pydantic"
    ],
) 