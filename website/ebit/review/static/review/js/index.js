
    function fetchMovies(genre, label) {
       var data = {
          genre: genre,
          label: label,
        }
        $.ajax({
          url: '/movie-by-label/',
          type: 'GET',
          dataType: 'json',
          data: data,
          }).done(function(response) {
            movArr = JSON.parse(response.movie_list);
              for (var m in movArr) {
                var image = movArr[m].thumbnail_image
                var name = movArr[m].movie_name
                var ebits_rating = movArr[m].ebits_rating
                var movie = `
                  <li>
                      <a href="">
                            <div class="img-wrap"><img src="${image}" class="img-fluid" alt=""/></div>
                            <div class="details">
                              <div class="name">${name}</div>
                              <div class="stat">
                                <span class="icon"><img src="static/review/img/rating-star.png" alt="" class="img-fluid"></span>
                                <span class="rating">${ebits_rating}</span>
                              </div>
                            </div>
                          </a>
                    </li>
                  `
                  $('.home-explorer-movie-list').append(movie) // append the new item to the <ul> tag
              }
        })

    }

   function loadGenres() {
        // send a GET request to build the list of movie-genres

        $.ajax({
            url: '/movie-genres/',
            type: 'GET',
            dataType: 'json',
          }).done(function(response) {
            genreArr = JSON.parse(response.all_genres);
            for (var g in genreArr) {
                 var gx = genreArr[g].name
                 if (cur_genre === null){
                     cur_genre = gx
                     var genre = `<li class="active" id="top-genre"><a  href="#">${gx}</a></li>`
                 } else {
                    var genre = `<li><a  href="#">${gx}</a></li>`
                 }

                  $('.home-explorer-gener-list').append(genre) // append the new item to the <ul> tag
            }
            fetchMovies(cur_genre, cur_label)
          })
   }



