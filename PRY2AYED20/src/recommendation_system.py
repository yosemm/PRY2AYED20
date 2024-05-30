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

    def add_artist(self, artist_name, style, mood, genre, location, popularSong, influencedBy, collaboratedWith,
                   decade):
        if self.artist_exists_in_database(artist_name):
            print(f"Artist {artist_name} already exists in the database.")
            return
        with self.driver.session() as session:
            query = """
                CREATE (a:Artist {name: $name, style: $style, mood: $mood, genre: $genre, location: $location, popularSong: $popularSong, influencedBy: $influencedBy, collaboratedWith: $collaboratedWith, decade: $decade})
                """
            session.run(query, name=artist_name, style=style, mood=mood, genre=genre, location=location,
                        popularSong=popularSong, influencedBy=influencedBy, collaboratedWith=collaboratedWith,
                        decade=decade)

            # COLLABORATED_WITH relationship
            query = """
                MATCH (a1:Artist {name: $name}), (a2:Artist)
                WHERE a2.name IN a1.collaboratedWith
                CREATE (a1)-[:COLLABORATED_WITH]->(a2)
                CREATE (a2)-[:COLLABORATED_WITH]->(a1)
                """
            session.run(query, name=artist_name)

            # SAME_LOCATION relationship
            query = """
                MATCH (a1:Artist {name: $name}), (a2:Artist)
                WHERE a1.location = a2.location
                CREATE (a1)-[:SAME_LOCATION]->(a2)
                CREATE (a2)-[:SAME_LOCATION]->(a1)
                """
            session.run(query, name=artist_name)

            # INFLUENCED_BY relationship
            query = """
                MATCH (a1:Artist {name: $name}), (a2:Artist)
                WHERE a2.name IN a1.influencedBy
                CREATE (a1)-[:INFLUENCED_BY]->(a2)
                CREATE (a2)-[:INFLUENCED_BY_REVERSE]->(a1)
                """
            session.run(query, name=artist_name)

            # SAME_STYLE relationship
            query = """
                MATCH (a1:Artist {name: $name}), (a2:Artist)
                WHERE a1.style = a2.style
                CREATE (a1)-[:SAME_STYLE]->(a2)
                CREATE (a2)-[:SAME_STYLE]->(a1)
                """
            session.run(query, name=artist_name)

            # SAME_DECADE relationship
            query = """
                MATCH (a1:Artist {name: $name}), (a2:Artist)
                WHERE a1.decade = a2.decade
                CREATE (a1)-[:SAME_DECADE]->(a2)
                CREATE (a2)-[:SAME_DECADE]->(a1)
                """
            session.run(query, name=artist_name)

            # SAME_MOOD relationship
            query = """
                MATCH (a1:Artist {name: $name}), (a2:Artist)
                WHERE a1.mood = a2.mood
                CREATE (a1)-[:SAME_MOOD]->(a2)
                CREATE (a2)-[:SAME_MOOD]->(a1)
                """
            session.run(query, name=artist_name)

            # SAME_GENRE relationship
            query = """
                MATCH (a1:Artist {name: $name}), (a2:Artist)
                WHERE a1.genre = a2.genre
                CREATE (a1)-[:SAME_GENRE]->(a2)
                CREATE (a2)-[:SAME_GENRE]->(a1)
                """
            session.run(query, name=artist_name)

    def delete_artist(self, artist_name):
        if not self.artist_exists_in_database(artist_name):
            print(f"Artist {artist_name} does not exist in the database.")
            return
        with self.driver.session() as session:
            query = """
                    MATCH (a:Artist {name: $name})
                    DETACH DELETE a
                    """
            session.run(query, name=artist_name)

    def modify_artist(self, artist_name, attribute, new_value):
        if not self.artist_exists_in_database(artist_name):
            print(f"Artist {artist_name} does not exist in the database.")
            return
        with self.driver.session() as session:
            # Update the artist's attribute
            query = f"""
                MATCH (a:Artist {{name: $name}})
                SET a.{attribute} = $value
                """
            session.run(query, name=artist_name, value=new_value)

            # Delete the artist's existing relationships
            query = """
                MATCH (a:Artist {name: $name})-[r]->()
                DELETE r
                """
            session.run(query, name=artist_name)

            # Recreate the artist's relationships
            query = """
                MATCH (a:Artist {name: $name})
                WITH a
                CALL {
                    WITH a
                    MATCH (a2:Artist)
                    WHERE a2.name IN a.collaboratedWith
                    CREATE (a)-[:COLLABORATED_WITH]->(a2)
                    CREATE (a2)-[:COLLABORATED_WITH]->(a)
                    RETURN count(*) AS dummy1
                }
                CALL {
                    WITH a
                    MATCH (a2:Artist)
                    WHERE a.location = a2.location
                    CREATE (a)-[:SAME_LOCATION]->(a2)
                    CREATE (a2)-[:SAME_LOCATION]->(a)
                    RETURN count(*) AS dummy2
                }
                CALL {
                    WITH a
                    MATCH (a2:Artist)
                    WHERE a2.name IN a.influencedBy
                    CREATE (a)-[:INFLUENCED_BY]->(a2)
                    CREATE (a2)-[:INFLUENCED_BY_REVERSE]->(a)
                    RETURN count(*) AS dummy3
                }
                CALL {
                    WITH a
                    MATCH (a2:Artist)
                    WHERE a.style = a2.style
                    CREATE (a)-[:SAME_STYLE]->(a2)
                    CREATE (a2)-[:SAME_STYLE]->(a)
                    RETURN count(*) AS dummy4
                }
                CALL {
                    WITH a
                    MATCH (a2:Artist)
                    WHERE a.decade = a2.decade
                    CREATE (a)-[:SAME_DECADE]->(a2)
                    CREATE (a2)-[:SAME_DECADE]->(a)
                    RETURN count(*) AS dummy5
                }
                CALL {
                    WITH a
                    MATCH (a2:Artist)
                    WHERE a.mood = a2.mood
                    CREATE (a)-[:SAME_MOOD]->(a2)
                    CREATE (a2)-[:SAME_MOOD]->(a)
                    RETURN count(*) AS dummy6
                }
                CALL {
                    WITH a
                    MATCH (a2:Artist)
                    WHERE a.genre = a2.genre
                    CREATE (a)-[:SAME_GENRE]->(a2)
                    CREATE (a2)-[:SAME_GENRE]->(a)
                    RETURN count(*) AS dummy7
                }
                RETURN a
                """
            session.run(query, name=artist_name)

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


def main():
    rs = RecommendationSystem()

    while True:
        print("1. Agregar un artista")
        print("2. Eliminar un artista")
        print("3. Salir")
        print("4. Modificar atributos de un artista")
        choice = input("Selecciona una opcion: ")

        if choice == "1":
            artist_name = input("Ingrese el nombre del artista:")
            style = input("Ingrese el estilo del artista:")
            mood = input("Ingrese el mood del artista:")
            genre = input("Ingrese el genero del artista")
            location = input("Ingrese la locacion del artista:")
            popularSong = input("Ingrese la cancion mas popular del artista:")
            influencedBy = input("Ingrese las influencias del artista:")
            collaboratedWith = input("Ingrese los artistas con los que ha colaborado:")
            decade = input("Ingrese la decada en la que estuvo activo el artista:")
            rs.add_artist(artist_name, style, mood, genre, location, popularSong, influencedBy, collaboratedWith,
                          decade)
        elif choice == "2":
            artist_name = input("Ingrese el nombre del artista a eliminar:")
            rs.delete_artist(artist_name)
        elif choice == "3":
            break
        elif choice == "4":
            artist_name = input("Ingrese el nombre del artista a modificar:  ")
            print("1. Style")
            print("2. Mood")
            print("3. Genre")
            print("4. Location")
            print("5. Popular Song")
            print("6. Influenced By")
            print("7. Collaborated With")
            print("8. Decade")
            attribute_choice = input("Selecciona el atributo a cambiar: ")
            attribute_map = {"1": "style", "2": "mood", "3": "genre", "4": "location", "5": "popularSong",
                             "6": "influencedBy", "7": "collaboratedWith", "8": "decade"}
            attribute = attribute_map.get(attribute_choice, "")
            if not attribute:
                print("Invalid attribute choice. Please try again.")
                continue
            new_value = input("Ingresa el nuevo valor para el atributo: ")
            rs.modify_artist(artist_name, attribute, new_value)
        else:
            print("Opcion invalida. Intenta de nuevo.")


if __name__ == "__main__":
    main()
