## Build container

```sh 
docker build --tag cogent3workshop -f .\DockerFile .
```

## Run container

```sh
docker run -it -p 8888:8888 -v .\workspace\:/workspace cogent3workshop
```