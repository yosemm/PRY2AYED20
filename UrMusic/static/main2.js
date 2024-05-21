$(document).ready(function () {
    var artist_name = new URL(window.location.href).searchParams.get('artist');

    $.ajax({
        url: 'http://127.0.0.1:5000/api/recommend',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({artist: artist_name}),
        success: function (data) {
            var recommendationsDiv = $('.card-container');
            recommendationsDiv.empty();

            data.forEach(function (artistName) {
                var artistNameNoSpaces = artistName.replace(" ", "");

                $.ajax({
                    url: 'http://127.0.0.1:5000/search',
                    method: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify({term: artistNameNoSpaces}),
                    success: function (data) {
                        var imageUrl = data.image_url;
                        var genre = data.genre.split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');

                        var cardGroup = $('<div>').addClass('card-group');

                        var card = $('<div>').addClass('card');
                        card.css('background-image', 'url(' + imageUrl + ')');

                        var cardInfo = $('<div>').addClass('card-info');
                        var h2 = $('<h2>').text(artistName);
                        var genreElement = $('<p>').html('<b>Género:</b> ' + genre);
                        cardInfo.append(h2, genreElement);

                        cardGroup.append(card, cardInfo);

                        recommendationsDiv.append(cardGroup);

                        if (data.top_tracks && data.top_tracks_urls) {
                            var top_tracks_list = $('<ul>');
                            data.top_tracks.forEach(function (track, index) {
                                var trackElement = $('<li>').html('<a href="' + data.top_tracks_urls[index] + '" target="_blank">' + track + ' <img src="/static/Icons/spotify-icon.svg" style="height: 16px;" alt="Spotify icon link"></a>');
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