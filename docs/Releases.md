Releases
=======================

<!-- vim-markdown-toc GitLab -->

* [Releases](#releases)
  * [Creating A Release](#creating-a-release)
      * [Manual release process](#manual-release-process)
      * [Automated release process](#automated-release-process)
  * [Finishing A Release](#finishing-a-release)
  
<!-- vim-markdown-toc -->  

Releases of the code are following the major/minor/patch pattern for release numbering.

## Creating a release

New releases can be generated manually or by using the 'release' command in the bin directory.

### Manual release process

- update the version number with in the version.txt file
- create a new branch named in the pattern 'release/v`version number`' (e.g. release/v0.0.1)
- push the branch to Github

### Automated release process

- ensure there are no uncommitted changes in your local repository
- call the 'release' command in the bin directory, passing as a parameter either major/minor/patch.

## Finishing a release

Once a release has been signed off and deployed to production, you need to:

- merge the release branch into master and to development.
- tag master with the release number at the point it was merged in.
- delete the release branch