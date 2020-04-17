Code Formatting
=======================

The code in this project is developed to the PyFlakes and pycodestyle coding standards, with the following exceptions:
* line length extended to 120 characters
* rule W605 disabled (invalid escape sequence)
* rule E501 disabled in all test files (line length)

The format is checked using the Python flake8 package.

-----------

The linter  can be run  with the 'lint' command in the bin directory.

_This command can be used when you are running the code using the docker container_ 
