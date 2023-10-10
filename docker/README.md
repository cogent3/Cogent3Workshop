# Cogent3 workshop Docker Container

This folder contains Docker configuration files for setting up the workshop environment for working with Cogent3 in a docker container.  The container installs the latest shipping version of cogent3, and runs a jupyter server that you can use from the host environment by browsing to [localhost:8888](localhost:8888).

## Screen cast: "How to set up a machine for a cogent3 workshop"

<a href="/docker/images/setup_machine.mp4" title="How to set up a machine for a cogent3 workshop"><img src="/docker/images/video_screenshot.jpg" alt="How to set up a machine for a cogent3 workshop" /></a>

## Prerequisites

Docker must be installed on your system. You can download Docker Desktop from [here](https://www.docker.com/products/docker-desktop).  Alternatively, on macOS, you can use Colima. See the section below for instructions on installing Colima.

## Installing Colima on macOS

Colima is a tool that provides a lightweight Docker-compatible environment on macOS without the need for a hypervisor. It is an alternative to Docker Desktop.

1. Install Colima using Homebrew:

    ```sh
    brew install colima
    ```

2. Initialize Colima with the Docker runtime:

    ```sh
    colima start --runtime docker
    ```

3. Verify that Colima is running:

    ```sh
    colima status
    ```

Now you can use Docker commands as you normally would, and Colima will handle the container runtime on macOS.

## Docker Image Contents

This container downloads and installs the following dependencies:

- Python3 (latest shipping version)
- Cogent3 (latest shipping version)
- ZSH (a more descriptive linux shell)
- OhMyZSH (a framework for managing ZSH configuration)

The container also makes a directory `/workspace`` for all files that you will be working on (that will persist between container sessions) and starts a jupyter server in that directory.

Note the container also sets up a virtual environment `c3workshop` that will give you an isolated python environment, and the .vscode directory contains `settings,json` to ensure that VS code uses only virtual environments to interpret jupyter notebooks. 

## Building the Docker Image

To build the Docker image, navigate to the root of the repository and run the following command to build a docker image named `cogent3workshop` using the Dockerfile in the `docker` directory:

`docker build --tag cogent3workshop -f docker\DockerFile .`

It should take around 90s to build the image.  You can check that the image was built successfully by running the following command:

`docker images cogent3workshop`

## Running the Docker Container

To start a Docker container using the image you just built, run the following command in a linux terminal (egf: from the terminal in VS Code):

`docker run -it --rm -p 8888:8888 -v ${PWD}:/workspace cogent3workshop`

You can also run this natively in your OS if you use an absolute path for the workspace directory.  For example, on Windows, you could use the following command:

`docker run -it --rm -p 8888:8888 -v C:\Users\username\Documents\cogent3workshop\:/workspace cogent3workshop`

on a Mac, you could use the following command:

`docker run -it --rm -p 8888:8888 -v /Users/username/Documents/cogent3workshop/:/workspace cogent3workshop`

This command does the following:

- `run`: Runs a jupyter server in a new container
- `-it`: Allocates an interactive terminal.  If you stop the jupyter server with ctrl-c, the container will exit.
- `--rm`: Automatically removes the container when it exits.
- `-p 8888:8888`: Maps port 8888 on the host to port 8888 in the container to allow access to the jupyter server from your host OS.
- `-v ${PWD}docker\workspace\:/workspace`: Mounts the root of your current directory on the host to `/workspace` in the container
- `cogent3workshop`: The name of the image we just built

## Connecting to the jupyter server from the host OS

You can connect to the jupyter server from your host OS by browsing to [localhost:8888](localhost:8888).  You will need to enter the token displayed in the terminal when you started the container.

It will be in a line that looks like this
`http://127.0.0.1:8888/tree?token=c9f817e64deb48b776ae74e6df6caede88a1a6e714448a23`

## Creating a test notebook

You can create a test notebook in the container by clicking the `New` button in the top right corner of the jupyter server page and selecting `Python 3`.  This will create a new notebook in the `/workspace` directory in the container.  You can then test that you can connect to cogent3 and quesy it's version using the commands below:

```python
import cogent3
cogent3.__version__
```

![Jupyter Notebook from the browser](/docker/images/browser.jpg)

## Stopping the container 

To stop the container, press ctrl-c in the terminal where you started the container.  If you no longer have the terminal open, you can stop the container using the following commands:

Find the container ID using the following command:

`docker ps -all`

This will list all running/stopped containers.  Find the container ID for the container you want to stop.  

Then, run the following command to stop the container:

`docker stop <container_id>`

## Restarting the container 

To restart the container if you have stopped it, run the following command:

`docker start <container_id>`


## Connecting to a running container using VS Code 

### Prerequisites

1. [Install VS Code](https://code.visualstudio.com/download) on your host OS if you don't already have it installed.
    - Windows: Run the installer and follow the on-screen instructions.
    - macOS: Drag the Visual Studio Code application into the Applications folder.
    - Linux: Depending on your distribution, use dpkg, rpm, or snap to install the downloaded package.
2. Open VS Code
3. Add the extension [Remote - Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) to VS Code.
4. Add the extension [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) to VS Code.
5. Add the extension [Jupyter](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter) to VS Code.
6. Open up a terminal in VS Code using the command ctrl-`
7. Ensure the docker daemon is running on your host OS.
`docker info`
8. Build the docker image as described above.
9. run the docker container as described above.

### Attaching to a running container

2. Click the button in the bottom left corner of the VS Code window that says `><` and select `Remote-Containers: Attach to Running Container...` 
![Attach to running container](/docker/images/attach.jpg)

3. Select the container you want to attach to from the list of running containers.
4. VS Code will open a new window with the container attached.  You can now edit files in the container using VS Code.

### Editing a jupyter notebook in the container

1. In the attached VS Code instance, you can either create a new Jupyter notebook by right-clicking in the Explorer, selecting New File, and giving it a .ipynb extension, or you can open an existing .ipynb file from the /workspace directory
![Editing a notebook in a container](/docker/images/container_notebook.jpg)
2. Note: your default directory will be the /workspace directory in the container, which will be mounted to the current director (when you ran the docker run command) in your host OS.  Any files you create in the container will persist between container sessions.
2. The Jupyter extension in VS Code provides an interactive interface similar to the classic Jupyter web interface. You can add cells, run code, visualize outputs, and more.

### using the ZSH shell in VS Code's terminal

ZSH is a more descriptive shell for working with the terminal.  To use it in VS Code, open a terminal in VS Code using the command ctrl-` and then type `zsh` and press enter.  You can then use the terminal as you normally would.

You can also choose a new ZSH shell in the terminal drop down.

You can also tell VS Code that you want to default to ZSH shells when you open a new terminal by clicking on the preferences cog icon, selecting settings and modifying the `Terminal > Integrated > Default Profile: Linux` setting to `zsh`.

![ZSH shell in VS Code](/docker/images/default_zsh.jpg)

## Naming continers

By default containers are given random names, like `condescending_tesla`.  To explicitly name a container, add the following argument to the `docker run` command:

`--name <container_name>`

when referring to a container using docker command, you can use either the container ID or the container name.

## Running a file in the container

To run a file in the container, add the command and it's arguments to the end of the `docker run` command:

`docker run  <command> <arguments>`

eg: To run a python script you created in your workspace directory in the container and then exit the container:

`docker run cogent3workshop python3 --rm -m example.phy`

to run the container as an immediate terminal session that uses zsh as a shell and removes the container once the session is exited:

`docker run -it --rm cogent3workshop /usr/bin/zsh`

## Inside the Docker Container

Once inside the Docker container, you will be in the `/workspace` directory containing all the files that are in the directory in your host OS you were currently in when you ran the docker run command.  You can use the `cd` command to navigate to other directories in the container.  Note the workspace directory is mounted to your host OS's directory so any files you create there in the container will persist between container sessions.

## Cleaning Up

To remove the Docker image you created, first find the image ID using:

`docker images`

Then, remove the image using:

`docker rmi <image_id>`

Replace `<IMAGE_ID>` with the ID of the image you want to remove.

## References

- [Docker Documentation](https://docs.docker.com/)
- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)
- [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)