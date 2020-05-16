# Solution

## Overview
We are using a docker-compose setup, to run three docker containers, namely nginx, flask and redis. 
Nginx is acting the frontend web server which is being used to handle the ssl termination. 
It proxies the request to the uswgi-flask server. 
The flask server connects to redis to store and retrieve the words for the apis.

## Pre-requisites
The setup has been tested on centos7, with following version of docker-ce(19.03) and docker-compose(1.18.0). 
The docker compose version has been set to 3.2 so any docker-ce version above 17.04.0+ should work.

## Setup
Commands are relative to the place the README.md file is present

### Docker container setup

 1. $ cd app
 2. $ docker-compose build
 3. $ docker-compose up -d

### Example API Usage

 1. Add words to redis database
    ```
	  curl -X POST -k https://localhost/add_word/word=foosball
    ```
    Above api will add the word foosball to redis
     
 2. Query words for autocompletion
    ```
    curl -X GET -k https://localhost/autocomplete/query=foo
    ```
    Above api will return list of all words in redis having foo as prefix
    
## Environment Variables

### Flask
For flask we are using 5 environment variables, majorly for configuring the connection to redis and the log level

  1. REDIS_HOST: redis host to connect to, defaults to localhost
  2. REDIS_PORT: redis port to connect to, defaults to 6379
  3. REDIS_DATABASE: redis database being used, defaults to 0
  4. REDIS_ZSET: redis zset name being used to store all the words
  5. REDIS_PASS: redis password for connecting to redis, mandatory
  
Note: REDIS_PASS has been included as plain text in the docker compose file. This is not best practice,
and has been done for ease of execution as docker-compose doesen't support docker secrets only docker swarm does.
In ideal production environments the REDIS_PASS environment variable should be populated through a secret
 
### Redis
For redis we are using only 1 environment variable, for setting the redis password

  1. REDIS_PASSWORD: redis password for connecting to redis
  
Note: REDIS_PASSWORD has been included as plain text in the docker compose file. This is not best practice,
and has been done for ease of execution as docker-compose doesen't support docker secrets only docker swarm does.
In ideal production environments the REDIS_PASSWORD environment variable should be populated through a secret