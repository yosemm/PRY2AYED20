from neo4j import GraphDatabase

from PRY2AYED20.src.artist import POPULAR_SONG

class recommendationsystembysong:
    def __init__(self):
        uri = "neo4j+s://ad86f838.databases.neo4j.io"
        username = "neo4j"
        password = "69W0amO7JsyNTTrsb506RR_6hUBxlzfZTPM-znz-Unw"
        self.driver = GraphDatabase.driver(uri, auth=(username, password))

    def get_similar_artists_by_song(self, song_title):
        with self.driver.session() as session:
            query = """
            MATCH (s:POPULAR_SONG {title: $title})-[:POPULAR_SONG_OF]->(a:Artist)
            MATCH (a)-[:HAS_GENRE]->(g:Genre), (a)-[:HAS_MOOD]->(m:Mood)
            MATCH (b:Artist)-[:HAS_GENRE]->(g), (b)-[:HAS_MOOD]->(m)
            WHERE a <> b
            RETURN b.name as name, m.name as mood, g.name as genre LIMIT 3
            """
            result = session.run(query, title=song_title)
            similar_artists = [{"name": record['name'], "mood": record['mood'], "genre": record['genre']} for record in result]
        return similar_artists

