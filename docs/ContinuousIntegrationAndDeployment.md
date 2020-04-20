# Continuous Integration and Deployment Pipeline

<!-- vim-markdown-toc GitLab -->

* [Azure Pipelines](#azure-pipelines)
  * [Continuous Integration](#continuous-integration)
    * [CI test](#ci-test)
    * [Development build](#development-build)
    * [Pre prod build](#pre-prod-build)
    * [Production build](#production-build)
  * [Continuous Deployment](#continuous-deployment)
    * [Development deploy](#development-deploy)
    * [Pre prod deploy](#pre-prod-deploy)
    * [Production deploy](#production-deploy)
    
<!-- vim-markdown-toc -->

## Pipeline

This project is being built and deployed using the AWS CodePipelines tooling. The definitions for this pipeline can be found in the `buildspec.yml` file in the root directory of the project.

### Development deploy

This pipeline should run when updates are pushed to the dev branch.

### Pre prod deploy

This pipeline should run when updates are pushed to the preprod branch.

### Production deploy

This pipeline should run when updates are pushed to the master branch.
