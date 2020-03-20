Testing
=======================

<!-- vim-markdown-toc GitLab -->

* [Strategy](#strategy)
  * [Coverage](#coverage)
* [Testing Commands](#testing-commands)

<!-- vim-markdown-toc -->

_This documentation is for the Methods Wagtail base repository and should be replaced with project specific documentation_

## Strategy

The project is developed using the TDD approach, using the unittest module for writing unit tests.

### Coverage

The target coverage level for the project is:

- &gt;80% coverage for unit testing
- Feature tests for each user feature, covering all probable scenarios.


## Testing Commands
_These commands can be used when you are running the code using the docker container_ 

The unit tests can be run with the 'test' command in the bin directory, or can be run with a coverage report using the 'coverage' command in the bin directory. The generated coverage report can then be viewed by opening the 'index.html' file in the 'htmlcov' directory.