Contributing guidelines
=======================

<!-- vim-markdown-toc GitLab -->

* [Pull requests](#pull-requests)

<!-- vim-markdown-toc -->

## Pull Requests

Once development on a branch is complete, the branch should be pushed to the Github repository and a pull request should be opened against the develop branch.

The pull request must be reviewed by at least one of the other developers on the project team. In order for the request to be accepted:
- the branch should contain logical atomic commits before sending a pull request - follow the [alphagov Git styleguide](https://github.com/alphagov/styleguides/blob/master/git.md)
- there must contain a succinct, clear summary of what the user need is driving this feature change
- there must be unit tests in place for the new code in the feature
- the CI pipeline must have passed
- the new code must pass a code quality review.

You may rebase your branch after feedback if it's to include relevant updates from the develop branch. It is preferable to rebase here then a merge commit as a clean and straight history on develop with discrete merge commits for features is preferred


## Branching strategy

See [the Branching documentation](BranchingStrategy.md) for details.


## Code format

See [the Code format documentation](CodeFormat.md) for details.


## Testing strategy

See [the Testing documentation](TestingStrategy.md) for details.
