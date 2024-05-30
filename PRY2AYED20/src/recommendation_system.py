import itertools

from neo4j import GraphDatabase


def jaccard_similarity(set1, set2):
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return len(intersection) / len(union) if union else 0


def calculate_similarity(a, b):
    style_sim = jaccard_similarity(set(a['a_style']), set(b['b_style']))
    mood_sim = jaccard_similarity(set(a['a_mood']), set(b['b_mood']))
    genre_sim = jaccard_similarity(set(a['a_genre']), set(b['b_genre']))
    location_sim = jaccard_similarity(set(a['a_location']), set(b['b_location']))
    popularSong_sim = jaccard_similarity(set(a['a_popularSong']), set(b['b_popularSong']))
    influencedBy_sim = jaccard_similarity(set(a['a_influencedBy']), set(b['b_influencedBy']))
    collaboratedWith_sim = jaccard_similarity(set(a['a_collaboratedWith']), set(b['b_collaboratedWith']))
    decade_sim = jaccard_similarity(set(a['a_decade']), set(b['b_decade']))
    relationship_sim = 1 if a['relationship_type'] == b['relationship_type'] else 0

    total_sim = 0.1 * style_sim + 0.1 * mood_sim + 0.1 * genre_sim + 0.1 * location_sim + 0.1 * popularSong_sim + 0.1 * influencedBy_sim + 0.1 * collaboratedWith_sim + 0.1 * decade_sim + 0.2 * relationship_sim
    return total_sim


class RecommendationSystem:
    def __init__(self):
        uri = "neo4j+s://ad86f838.databases.neo4j.io"
        username = "neo4j"
        password = "69W0amO7JsyNTTrsb506RR_6hUBxlzfZTPM-znz-Unw"
        self.driver = GraphDatabase.driver(uri, auth=(username, password))

    def artist_exists_in_database(self, artist_name):
        with self.driver.session() as session:
            query = """
                MATCH (a:Artist {name: $name})
                RETURN a.name AS name
                """
            result = session.run(query, name=artist_name)
            return result.single() is not None

    def get_similar_artists(self, artist_name):
        with self.driver.session() as session:
            query = """
    MATCH (a:Artist {name: $name})-[r]->(b:Artist)
    WHERE a.name <> b.name
    RETURN a.name AS a_name, a.style AS a_style, a.mood AS a_mood, a.genre AS a_genre, a.location AS a_location, a.popularSong AS a_popularSong, a.influencedBy AS a_influencedBy, a.collaboratedWith AS a_collaboratedWith, a.decade AS a_decade,
           b.name AS b_name, b.style AS b_style, b.mood AS b_mood, b.genre AS b_genre, b.location AS b_location, b.popularSong AS b_popularSong, b.influencedBy AS b_influencedBy, b.collaboratedWith AS b_collaboratedWith, b.decade AS b_decade,
           type(r) AS relationship_type
    """
            result = session.run(query, name=artist_name)
            artists = [record for record in result]
            similar_artists = []
            # Sets para llevar un control de los que ya han sido comparados.
            compared_pairs = set()
            artist_names = set()
            for a, b in itertools.combinations(artists, 2):
                pair = frozenset([a['a_name'], b['b_name']])
                if pair not in compared_pairs:
                    similarity = calculate_similarity(a, b)
                    if similarity > 0 and b[
                        'b_name'] not in artist_names:  # Chequear que la similitud sea mayor a 0 y que el artista no
                        # haya sido ya agregado
                        similar_artists.append((b['b_name'], similarity))
                        artist_names.add(b['b_name'])
                    compared_pairs.add(pair)  # Agregar el par a los que ya han sido comparados

            similar_artists.sort(key=lambda x: x[1], reverse=True)
            return [artist for artist, _ in similar_artists[:3]]
