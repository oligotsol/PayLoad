"""
PayLoad SDK - Autonomous Payment Rails for Machines
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="payload-sdk",
    version="0.1.0",
    author="PayLoad",
    description="Autonomous payment rails for drones and IoT devices. USD1 micropayments on Solana.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/oligotsol/PayLoad",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Office/Business :: Financial :: Payment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.9",
    install_requires=[
        "solana>=0.32.0",
        "solders>=0.20.0",
        "base58>=2.1.1",
    ],
    keywords=[
        "solana",
        "payments",
        "micropayments",
        "iot",
        "drones",
        "autonomous",
        "usd1",
        "stablecoin",
        "m2m",
        "machine-to-machine"
    ],
)
