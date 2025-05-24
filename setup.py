from setuptools import setup, find_packages

setup(
    name="Skintils",
    version="1.0.0",
    url="https://github.com/coaltars/skintils",
    
    packages=find_packages(),
    install_requires=["Pillow","PyInstaller"],
    python_requires=">=3.6",
    entry_points={
        "gui_scripts": [
            "skintils=run",
        ],
    },
    
    include_package_data=True,
    zip_safe=False,
)