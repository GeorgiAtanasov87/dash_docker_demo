# Run miniconda with jupyter notebook
## Using Docker 
1. From  /jupyter dir:
``` 
docker build -t jupyter-lab .
```
2. From . (project root dir):
```
docker run -it -p 8888:8888 -v $(pwd):/opt/notebooks localhost/jupyter-lab:latest
```

## Using Docker compose
From project root dir:
``` 
docker compose up jupyter
```