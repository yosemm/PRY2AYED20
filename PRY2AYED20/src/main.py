from recommendation_system import RecommendationSystem

def main():
    recommendation_system = RecommendationSystem()

    artist_name = input("Enter the name of the artist you want to search for: ")

    similar_artists = recommendation_system.get_similar_artists(artist_name)

    for artist in similar_artists:
        print(f"Similar artist to {artist_name}: {artist.name}")
        print(f"Mood: {artist.mood}")
        print(f"Genre: {artist.genre}")

if __name__ == "__main__":
    main()