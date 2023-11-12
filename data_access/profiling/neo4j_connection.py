from neo4j import GraphDatabase
from decouple import config

def connect_to_neo4j():
    uri = config('NEO4J_URI')
    user = config('NEO4J_USERNAME')
    password = config('NEO4J_PASSWORD')
    
    driver = GraphDatabase.driver(uri, auth=(user, password))
    return driver

def execute_cypher_query(query,parameters=None):
    with connect_to_neo4j() as driver:
        with driver.session() as session:
            result = session.run(query,parameters)
            return result
