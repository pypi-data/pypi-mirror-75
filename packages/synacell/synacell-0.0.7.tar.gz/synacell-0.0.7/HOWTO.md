## Generate distribution packages for a PyPI package

These are archives that are uploaded to the Package Index and can be installed by pip. Make sure you have the latest versions of setuptools and wheel installed:
```
python -m pip install --user --upgrade setuptools wheel
```

Now run this command from the same directory where setup.py is located:
```
python setup.py sdist bdist_wheel
```

This command should output a lot of text and once completed should generate two files in the dist directory:
```
dist/
  example_pkg_YOUR_USERNAME_HERE-0.0.1-py3-none-any.whl
  example_pkg_YOUR_USERNAME_HERE-0.0.1.tar.gz
```

## Testing the package

You can test the package by running `scripts/install.bat` and runnig tests if the package is installed thrpugh PyPI.

## Upload package to PyPI

Install twine.
```
pip install twine
```

Upload package to PyPI.
```
twine upload dist/*
```

## Make Microsoft Visual Studio project from CMakeLists.txt

By running the following command from the folder where CMakeLists.txt lies, you can make a .sln project files and use it in Visual Studio IDE:

```
cmake -G "Visual Studio 15 2017" -A x64
```
