package org.example;

import java.util.ArrayList;
import java.util.List;
import org.neo4j.driver.*;
import org.neo4j.driver.Record;

import static org.neo4j.driver.Values.parameters;

class Artist {
    String name;
    String location;
    String mood;
    String genre;
    String influencedBy;
    String collaboratedWith;
    String style;
    String decade;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getLocation() {
        return location;
    }

    public void setLocation(String location) {
        this.location = location;
    }

    public String getMood() {
        return mood;
    }

    public void setMood(String mood) {
        this.mood = mood;
    }

    public String getGenre() {
        return genre;
    }

    public void setGenre(String genre) {
        this.genre = genre;
    }

    public String getInfluencedBy() {
        return influencedBy;
    }

    public void setInfluencedBy(String influencedBy) {
        this.influencedBy = influencedBy;
    }

    public String getCollaboratedWith() {
        return collaboratedWith;
    }

    public void setCollaboratedWith(String collaboratedWith) {
        this.collaboratedWith = collaboratedWith;
    }

    public String getStyle() {
        return style;
    }

    public void setStyle(String style) {
        this.style = style;
    }

    public String getDecade() {
        return decade;
    }

    public void setDecade(String decade) {
        this.decade = decade;
    }

}


class RecommendationSystem {
    private static final String NEO4J_URI = "neo4j+s://ad86f838.databases.neo4j.io";
    private static final String NEO4J_USERNAME = "neo4j";
    private static final String NEO4J_PASSWORD = "69W0amO7JsyNTTrsb506RR_6hUBxlzfZTPM-znz-Unw";
    private final Driver driver;

    public RecommendationSystem() {
        this.driver = GraphDatabase.driver(NEO4J_URI, AuthTokens.basic(NEO4J_USERNAME, NEO4J_PASSWORD));
    }

public List<Artist> getSimilarArtists(String artistName) {
    List<Artist> similarArtists = new ArrayList<>();
    try (Session session = driver.session()) {
        String query = "MATCH (a:Artist {name: $name}), (b:Artist) " +
                       "WHERE a.genre = b.genre AND a.mood = b.mood AND a.name <> b.name " +
                       "RETURN b.name as name, b.mood as mood, b.genre as genre LIMIT 3";
        Result result = session.run(query, parameters("name", artistName));
        while (result.hasNext()) {
            Record record = result.next();
            Artist artist = new Artist();
            artist.setName(record.get("name").asString());
            artist.setMood(record.get("mood").asString());
            artist.setGenre(record.get("genre").asString());
            similarArtists.add(artist);
        }
    }
    return similarArtists;
}
}