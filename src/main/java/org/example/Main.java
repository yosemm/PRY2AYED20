package org.example;
import java.util.List;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        RecommendationSystem recommendationSystem = new RecommendationSystem();

        try (Scanner scanner = new Scanner(System.in)) {
            System.out.println("Enter the name of the artist you want to search for:");
            String artistName = scanner.nextLine();

            List<Artist> similarArtists = recommendationSystem.getSimilarArtists(artistName);

            for (Artist artist : similarArtists) {
                System.out.println("Similar artist to " + artistName + ": " + artist.getName());
                System.out.println("Mood: " + artist.getMood());
                System.out.println("Genre: " + artist.getGenre());
            }
        }
    }
}