from neo4j import GraphDatabase

from PRY2AYED20.src.artist import Artist


class RecommendationSystem:
    def __init__(self):
        uri = "neo4j+s://ad86f838.databases.neo4j.io"
        username = "neo4j"
        password = "69W0amO7JsyNTTrsb506RR_6hUBxlzfZTPM-znz-Unw"
        self.driver = GraphDatabase.driver(uri, auth=(username, password))

    def get_similar_artists(self, artist_name):
        with self.driver.session() as session:
            query = """
            MATCH (a:Artist {name: $name}), (b:Artist) 
            WHERE a.genre = b.genre AND a.mood = b.mood AND a.name <> b.name 
            RETURN b.name as name, b.mood as mood, b.genre as genre LIMIT 3
            """
            result = session.run(query, name=artist_name)
            similar_artists = [Artist(record['name'], record['mood'], record['genre']) for record in result]
        return similar_artists