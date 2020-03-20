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

## Azure Pipelines

The repository contains definitions for pipelines using the Azure Devops tooling.

### Continuous Integration

The continuous integration pipelines for the project are defined in yml files in the `pipelines/azure_devops` directory.

There are 4 pipelines defined in the project.

#### CI test
_Defined in 'azure-pipelines.yml'_

This pipeline should run on every push to Github from feature, bug and refactor branches. All this pipeline does is run the tests to regression check the new code.
The trigger for the pipeline is tied to branches starting with `feature/`, `refactor/` or `bug/`. If you are using a different branch naming strategy this will need to be updated to reflect that.

#### Development build
_Defined in 'dev-azure-pipelines.yml'_

This pipeline should run on every push to Github on the develop branch. This pipeline runs the tests and, if they pass, builds a docker container and pushes it to the dev container registry.

The trigger for the pipeline is tied to the branch develop. If you are using a different branch naming strategy this will need to be updated to reflect that.

The pipeline also assumes the use of Azure Container Registry for published container images, it requires 2 environment variables to run successfully:
* dockerId - the name of the container registry 
* dockerPassword - the generated password for logging in to the registry from the command line.

#### Pre prod build
_Defined in 'pre-prod-azure-pipelines.yml'_

This pipeline should run on every push to Github from a release branch. This pipeline runs the tests and, if they pass, builds a docker container and pushes it to the pre-prod container registry.

The trigger for the pipeline is tied to branches starting with `release/`. If you are using a different branch naming strategy this will need to be updated to reflect that.

The pipeline also assumes the use of Azure Container Registry for published container images, it requires 2 environment variables to run successfully:
* dockerId - the name of the container registry 
* dockerPassword - the generated password for logging in to the registry from the command line.

#### Production build

_Defined in 'prod-azure-pipelines.yml'_

This pipeline should run on every push to Github on the master branch. This pipeline runs the tests and, if they pass, builds a docker container and pushes it to the prod container registry.

The trigger for the pipeline is tied to the branch master. If you are using a different branch naming strategy this will need to be updated to reflect that.

The pipeline also assumes the use of Azure Container Registry for published container images, it requires 2 environment variables to run successfully:
* dockerId - the name of the container registry 
* dockerPassword - the generated password for logging in to the registry from the command line.

### Continuous Deployment

Azure Devops does not currently support yml definitions for deployment pipelines, so these will need to be defined through the Azure DevOps pipeline UI.

There should be one for three environments.

#### Development deploy

This pipeline should run when the Development CI pipeline passes.

#### Pre prod deploy

This pipeline should run when the Pre-Production CI pipeline passes.

#### Production deploy

This pipeline should run when the Production CI pipeline passes.
