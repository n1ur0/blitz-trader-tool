# Blitz Card Trader Tool

This tool aims to ease the trading logistics of your cards 

<img width="1175" alt="image" src="https://github.com/n1ur0/blitz-trader-tool/assets/16278543/01491c7f-dcf1-4fbd-90ad-460464efc0f2">

### Requirements:
Install docker
  https://www.docker.com/products/docker-desktop/

Pre-collect the output of Missing/Duplicates from: https://ergcube.com/blitz.html (Special thanks to **hq3r**!)
![image](https://github.com/n1ur0/blitz-trader-tool/assets/16278543/6b29c68f-ede4-449d-a820-5067b537063a)

### How to install and run the container:
```
  docker build -t blitz-trader .  
  docker run -p 8501:8501 blitz-trader
```
#### Open the link: http://localhost:8501/

### How to stop the container:
```
  docker stop blitz-trader
```
