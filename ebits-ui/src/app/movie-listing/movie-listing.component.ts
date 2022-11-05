import { Options } from '@angular-slider/ngx-slider';
import { Component, OnInit } from '@angular/core';
import { ServiceManagerService } from '../service-manager.service';

@Component({
  selector: 'app-movie-listing',
  templateUrl: './movie-listing.component.html',
  styleUrls: ['./movie-listing.component.scss']
})
export class MovieListingComponent implements OnInit {

  readonly DISPLAY_VIEW_GRID = "GRID";
  readonly DISPLAY_VIEW_LIST = "LIST";

  constructor(private serviceManager: ServiceManagerService) { }

  /* panelOpenState = false;
  categoryPanelOpenState = true; */

  sortBySelection = 'option1';

  minEbitsRatingValue: number = 2;
  maxEbitsRatingValue: number = 4;
  ebitsRatingOptions: Options = {
    floor: 0,
    ceil: 5,
    animateOnMove: true,
    draggableRange: true
  };
  minCriticsRatingValue: number = 2;
  maxCriticsRatingValue: number = 4;
  criticsRatingOptions: Options = {
    floor: 0,
    ceil: 5,
    animateOnMove: true,
    draggableRange: true
  };

  onEbitsRatingSelectionChange(): void {
    console.log("onEbitsRatingSelectionChange called .. ");
  }
  onCriticsRatingSelectionChange(): void {
    console.log("onCriticsRatingSelectionChange called .. ");
  }

  listViewOptionSelected = this.DISPLAY_VIEW_LIST;
  onGridViewSelection() {
    console.log("onGridViewSelection called .. ");
    this.listViewOptionSelected = this.DISPLAY_VIEW_GRID;
  }
  onListViewSelection() {
    console.log("onListViewSelection called .. ");
    this.listViewOptionSelected = this.DISPLAY_VIEW_LIST;
  }

  categories: Category[] = [];
  genres: string[] = [];
  platforms: Platform[] = [];
  moods: Mood[] = [];
  certifications: Certificate[] = [];
  languages: Language[] = [];
  ethinicities: Ethinicity[] = []

  movies: Movie[] = [];

  ngOnInit(): void {

    // Similar Movies by Genre
    this.serviceManager.getMovies().subscribe(data => {
      this.movies = data.movies;
      console.log("Live MoviesList : " , this.movies);
    });
    // Movie Categories
    this.serviceManager.getCategories().subscribe(data => {
      this.categories = data.categories;
      console.log("Live movie Geners : " , this.categories);
    });
    // Movie Geners
    this.serviceManager.getMovieGeners().subscribe(data => {
      this.genres = data.geners;
      console.log("Live movie Geners : " , this.genres);
    });
    // Moods
    this.serviceManager.getMovieMoods().subscribe(data => {
      this.moods = data.moods;
      console.log("Live movie moods : ", this.moods);
    });
    // Moods
    this.serviceManager.getPlatforms().subscribe(data => {
      this.platforms = data.platforms;
      console.log("Live movie moods : ", this.platforms);
    });
    // Moods
    this.serviceManager.getLanguages().subscribe(data => {
      this.languages = data.languages;
      console.log("Live movie moods : ", this.languages);
    });
    // Moods
    this.serviceManager.getEthinicities().subscribe(data => {
      this.ethinicities = data.ethinicities;
      console.log("Live movie moods : ", this.ethinicities);
    });
    // Moods
    this.serviceManager.getCertifications().subscribe(data => {
      this.certifications = data.certifications;
      console.log("Live movie moods : ", this.certifications);
    });
  }

  /* updateCategoryFilter(){

  } */
}


interface Mood {
  id: number;
  name: string;
  photo: string;
}

interface Category {
  id: number,
  name: string
}

interface Certificate {
  id: number,
  name: string
}

interface Language {
  id: number,
  name: string
}

interface Ethinicity {
  id: number,
  name: string
}

interface Category {
  id: number,
  name: string
}

interface Category {
  id: number,
  name: string
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
  platforms?: Platform[],
  description?: string,
  releaseYear?: number,
  directors?: string,
  casts?: string
}
