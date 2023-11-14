from neo4j import GraphDatabase
from decouple import config

class Neo4jConnector:
    def __init__(self):
        self._uri = config('NEO4J_URI')
        self._user = config('NEO4J_USERNAME')
        self._password = config('NEO4J_PASSWORD')
        self._driver = None

    def connect(self):
        self._driver = GraphDatabase.driver(self._uri, auth=(self._user, self._password))
    
    def close(self):
        if self._driver is not None:
            self._driver.close()
    
    def find_by(self, query, parameters=None):
        with self._driver.session() as session:
            response = session.run(query, parameters)
            if response:
                result =response.single()
                if result: 
                    return result.data()
            
            return None
    def find_all(self, query, parameters=None):
        with self._driver.session() as session:
            response = session.run(query, parameters)
            if response:
                return  [record.data() for record in response]          
            return None        
