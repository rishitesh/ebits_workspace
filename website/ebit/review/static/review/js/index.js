
    function fetchMovies(genre, label) {
       var data = {
          genre: genre,
          label: label,
        }
        $.ajax({
          url: '/movie-by-label-genre/',
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

    function renderBestInStories(label) {
       var data = {
          label: label,
        }
        $.ajax({
          url: '/movie-by-label/',
          type: 'GET',
          dataType: 'json',
          data: data,
          }).done(function(response) {
            movArr = JSON.parse(response.movie_list);
              var firstEntry = true
              for (var m in movArr) {
                var image = movArr[m].thumbnail_image
                var name = movArr[m].movie_name

                var ebits_rating = movArr[m].ebits_rating
                if (firstEntry) {
                    firstEntry = false
                    var movie = `
                        <div class="first-entry">
                            <div class="img-wrap"><img src="${image}" alt="" class="img-fluid"></div>
                            <div class="content-wrap">
                            <div class="rating-wrap">
                              <div class="rating-star">
                                <span class="icon"><img src="static/review/img/rating-star.png" alt="" class="img-fluid"></span>
                              </div>
                              <div class="rating-value">${ebits_rating}</div>
                            </div>
                            <div class="title">${name}</div>
                            <div class="sub-heading">Action | Thriller | Drama</div>
                            <div class="btn-wrap">
                              <a href="" class="btn btn--red"><span class="icon"><img src="static/review/img/details-play-trailer.png" alt="" class="img-fluid"></span>Play Trailer</a>
                              <a href="" class="btn btn--glass">View Details</a>
                            </div>
                    </div>`

                  $('.selected-best-story__wrap').append(movie)
                } else {
                    alert(name)
                    var movie = `<div class="best-in-story-slider-item"><img src="${image}" alt="" class="img-fluid"></div>`
                    $('.best-in-story-slider__inner').append(movie)
                }
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



