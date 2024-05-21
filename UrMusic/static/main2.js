$(document).ready(function () {
    var artist_name = new URL(window.location.href).searchParams.get('artist');

    $.ajax({
        url: 'http://127.0.0.1:5000/api/recommend',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({artist: artist_name}),
        success: function (data) {
            // data is an array of similar artist names
            // Use the data to populate the recommendations on the page
            var recommendationsDiv = $('.card-container'); // Replace with the actual class of your recommendations div
            recommendationsDiv.empty(); // Clear the existing recommendations

            data.forEach(function (artistName) {
                var artistNameNoSpaces = artistName.replace(" ", "");

                $.ajax({
                    url: 'http://127.0.0.1:5000/search',
                    method: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify({term: artistNameNoSpaces}),
                    success: function (data) {
                        // Spotify API returns images in an array, so we get the URL of the first image
                        var imageUrl = data.image_url;

                        // Spotify API returns genres in an array, so we join them into a string
                        var genre = data.genre.split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');

                        // Create a new card group
                        var cardGroup = $('<div>').addClass('card-group');

                        // Create a new card
                        var card = $('<div>').addClass('card');
                        card.css('background-image', 'url(' + imageUrl + ')');

                        // Create a new card info
                        var cardInfo = $('<div>').addClass('card-info');
                        var h2 = $('<h2>').text(artistName);
                        var genreElement = $('<p>').html('<b>Género:</b> ' + genre);
                        cardInfo.append(h2, genreElement);

                        // Add the card and card info to the card group
                        cardGroup.append(card, cardInfo);

                        // Add the card group to the recommendations div
                        recommendationsDiv.append(cardGroup);

                        // Populate top tracks
                        if (data.top_tracks && data.top_tracks_urls) {
                            var top_tracks_list = $('<ul>');
                            data.top_tracks.forEach(function (track, index) {
                                var trackElement = $('<li>').html('<a href="' + data.top_tracks_urls[index] + '" target="_blank">○ ' + track + ' <img src="/static/Icons/spotify-icon.svg" style="height: 16px;" alt="Spotify icon link"></a>');
                                top_tracks_list.append(trackElement);
                            });
                            cardInfo.append('<p><b>Canciones destacadas:</b></p>', top_tracks_list);
                        }
                    }
                });
            });
        }
    });
});