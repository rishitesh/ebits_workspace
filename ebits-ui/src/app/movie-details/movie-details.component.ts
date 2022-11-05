import { Component, OnInit } from '@angular/core';
import { ServiceManagerService } from '../service-manager.service';

@Component({
  selector: 'app-movie-details',
  templateUrl: './movie-details.component.html',
  styleUrls: ['./movie-details.component.scss']
})
export class MovieDetailsComponent implements OnInit {

  constructor(
    private serviceManager: ServiceManagerService) { }

  movieDetails: Movie = {};
  movieGenres: string[] = [];
  movieCasts: Cast[] = [];
  movieAwards: Award[] = [];
  moviesSimilarByGenre: Movie[] = [];
  moviesRecommended: Movie[] = [];

  criticReviews: Review[] = [];
  userReviews: Review[] = [];

  trailers: Trailer[] = [];
  moviePhotos: string[] = [];

  ngOnInit(): void {

    // Movie Details
    this.serviceManager.getMovieDetails().subscribe(data => {
      this.movieDetails = data;
      this.movieGenres = data.genre;
      this.movieCasts = data.overview.casts;
      this.movieAwards = data.overview.awards;
      this.criticReviews = data.criticReviews;
      this.userReviews = data.userReviews;
      this.trailers = data.gallery.trailers;
      this.moviePhotos = data.gallery.photos;
      console.log("Live movieDetails : " , this.movieDetails);
    });
    // Similar Movies by Genre
    this.serviceManager.getMoviesSimilarByGenre().subscribe(data => {
      this.moviesSimilarByGenre = data.movies;
      console.log("Live similarMoviesList : " , this.moviesSimilarByGenre);
    });
    // Similar Movies by Genre
    this.serviceManager.getMoviesSimilarByGenre().subscribe(data => {
      this.moviesRecommended = data.movies;
      console.log("Live similarMoviesList : " , this.moviesRecommended);
    });
  }

  getTrailerIFrame(iFrameSrc: string): string {
    let iFrameStr = '\'<iframe width="560" height="315" src="' + iFrameSrc
        + '" title="YouTube video player" frameborder="0" autoplay="1" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>\'';
    return iFrameStr;
  }

}

interface Review {
  autherName: string,
  publication: string,
  ratings: number,
  title: string,
  review: string,
  dateTime: string,
  image: string
}

interface Award {
  awardFor: string,
  awardName: string 
}

interface Sentimeter {
  positive: number,
  negative: number,
  mixed: number
}

interface Ratings {
  story: number,
  direction: number,
  performance: number,
  music: number,
  overall: number,
  count: number,
  review: string
}

interface Cast {
  name: string,
  roleName: string,
  image: string
}

interface MovieOverview {
  realeaseDate: Date,
  language: string,
  genre: string[],
  awards: Award[],
  certifications: string[],
  storyLine: string,
  directors: string[]
  casts: Cast[] 
}

interface Trailer {
  trailerUrl: string,
  imageUrl: string,
  length: string
}

interface MovieGallery {
  trailers: Trailer[],
  photos: string[]
}

interface Platform {
  name: string;
  image: string;
}

interface Movie {
  id?: number,
  title?: string,
  length?: number,
  genre?: string[],
  image?: string,
  sentimeter?: Sentimeter,
  ebitsRatings?: Ratings,
  criticRatings?: Ratings,
  userRatings?: Ratings,
  overview?: MovieOverview,
  userReviews?: Review [],
  criticReviews?: Review [],
  gallery?: MovieGallery,
  platforms?: Platform[]
}
