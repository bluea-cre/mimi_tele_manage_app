from setuptools import setup, find_packages

setup(
    name="main",
    version="1.0.0",
    description="A Python GUI application for managing functions and configurations.",
    author="tele_app",
    author_email="tele_app.email@gmail.com",
    packages=find_packages(),
    install_requires=[
        # Add dependencies here if needed
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "main=main.main:main",  # Entry point for the application
        ],
    },
)
