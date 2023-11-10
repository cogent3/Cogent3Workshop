# Cogent3 workshop Devcontainer

This folder contains a Docker configuration file for setting up the workshop environment for working with Cogent3 in a docker container, and a `devcontainer.json` configuration so that VS Code can manage the container.  The container installs the latest shipping version of cogent3, and runs a jupyter server that you can use from the host environment by browsing to [localhost:8888](localhost:8888).  It also prepopulates VS code extensions for jupiter notebooks and python.

For instructions for building this docker image into a container to run the workshop, see the [Computer setup instructions](https://github.com/cogent3/Cogent3Workshop/wiki/Computer-Setup).