import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ServiceManagerService } from '../service-manager.service';

@Component({
  selector: 'app-ott-explorer',
  templateUrl: './ott-explorer.component.html',
  styleUrls: ['./ott-explorer.component.scss']
})
export class OttExplorerComponent implements OnInit {

  constructor(
    private serviceManager: ServiceManagerService) { }

    movieGeners: string[] = [];
    movieGenersSelection: string[] = [];
    movies: Movie[] = [];

  ngOnInit(): void {
    // Movie Geners
    this.serviceManager.getMovieGeners().subscribe(data => {
      this.movieGeners = data.geners;
      console.log("Live movie Geners : " , this.movieGeners);
    });
    // Movies
    this.serviceManager.getMovies().subscribe(data => {
      this.movies = data.movies;
      console.log("Live movies : " , this.movies);
    });
  }

  movieSlideConfig = {
    "slidesToShow": 6.2,
    "slidesToScroll": 1,
    "dots": false,
    "infinite": false
  };

  slickInit(e: any) {
    console.log('slick initialized');
  }

  breakpoint(e: any) {
    console.log('breakpoint');
  }

  afterChange(e: any) {
    console.log('afterChange');
  }

  beforeChange(e: any) {
    console.log('beforeChange');
  }

  updateGenerSelection(gener: string) {
    if (gener == "") {
      return;
    } else {
      if (this.movieGenersSelection.includes(gener)) {
        this.movieGenersSelection.forEach((value, index) => {
          if (value == gener)
            this.movieGenersSelection.splice(index, 1);
        });
      } else {
        this.movieGenersSelection.push(gener);
      }
      console.log("Update gener selection : ", this.movieGenersSelection);
    }
  }

}


interface Movie {
  id:number,
  title: string;
  image: string;
  ebitsRatings: number;
}
