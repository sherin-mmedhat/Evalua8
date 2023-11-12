# Evalua8
## go the application folder , open a terminal 
## navigate to docker-compose folder and build and up the container
  docker-compose up --build

## create .env file in the main application folder 

##add the url and user and passwod for neo4j database 
 NEO4J_URI = bolt://my-neo4j-container:7687
 NEO4J_USERNAME = neo4j
 NEO4J_PASSWORD =password

## to run the migration for profiling database 
 go and run the script in this file data_access/profiling/migration.ipynb
