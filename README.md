# Dash and Jupyter in containers 

This is a demo created for DEV.bg showcasing python Dash application development.
It contains a containerized Dash and a separate container with Jupyter lab that can
be used as development environment for the dash application.

The dash app is a simple data visualisation tool that reads DAM energy prices for the Balkans region.
All data is from Entsoe transpaarency portal: https://transparency.entsoe.eu/transmission-domain/r2/dayAheadPrices/show![image](https://user-images.githubusercontent.com/16559858/230373892-a3c0ae4e-7a34-4c54-8785-d9912c2605e3.png)

To demo the app:
1. Clone this repo
```
git clone https://github.com/GeorgiAtanasov87/dash_docker_demo.git
```
2. Build and run the containers:
```
cd dash_docker_demo
docker-compose build
docker-compose up
```

3. To stop & remove all deployed containers:
```
docker-compose down
```
