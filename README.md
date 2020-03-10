# Vector.ai Backend Test
## Problem Statement
Problem statement can be found in the repository itself

## Tasks
### Writer
#### Database Layer
* ~~Database schema design~~
* ~~DB SQL write ups~~
* ~~Database layer accessor module~~
* ~~Database input validation module~~
* ~~Add more validation logic to check state of db remains consisitent with successful operations, otherwise fail the operations~~
#### StorageInterface Layer
* ~~Service Layer on Top of db and validator modules~~
#### Service Layer
* ~~Service Layer on Top of storageinterface~~
#### Middleware Layer
* ~~Kafka Module to read from topic and send back response~~
### Client
#### Middleware Layer
* ~~[SIMILAR TO WRITER]Middleware Kafka Layer to send request to writer and read back response~~
#### Service Layer
* ~~Service layer on top of that to act as an interface~~
### Miscellaneous
#### Logging Module
* ~~Logging module to write logs using ELK module~~
#### Docker/Packaging
* First make a giant docker file to have all dependencies and module for client, writer components
* Split the large file into database, kafka, service, logging and connec them using docker-compose
#### Deployment
* Deploy the corresponding docker images to aws and host the application there
