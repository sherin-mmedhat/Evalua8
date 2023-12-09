# EVALU
## go the application folder , open a terminal 
## navigate to docker-compose folder and build and up the container
  docker-compose up --build

## create .env file in the main application folder 

##add the url and user and passwod for neo4j database 
 NEO4J_URI = bolt://my-neo4j-container:7687
 NEO4J_USERNAME = neo4j
 NEO4J_PASSWORD =password
## add the url and port for nosql db 
MONGO_DB_URI=evalu8-mongodb
MONGO_DB_PORT=27017

## to run the migration for profiling database 
 go and run the script in this file data_access/profiling/migration.ipynb

## to run the migration for the kpi collection 
go and run the script in this file data_access/kpi/KPI_migration.ipynb

## to access the neo4j database 
