import { Component, OnInit } from '@angular/core';
import { ServiceManagerService } from '../service-manager.service';

@Component({
  selector: 'app-whats-new',
  templateUrl: './whats-new.component.html',
  styleUrls: ['./whats-new.component.scss']
})
export class WhatsNewComponent implements OnInit {

  constructor(
    private serviceManager: ServiceManagerService) { }

  newMovies: Movie[] = []

  ngOnInit(): void {
    // Trending Movies
    this.serviceManager.getWhatsNewMovies().subscribe(data => {
      this.newMovies = data.movies;
      console.log("Live New Movies Trending : ", this.newMovies);
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

}

interface Movie {
  id: number,
  title: string,
  description: string,
  image: string,
  releaseYear: number,
  length: number,
  ebitsRatings: number,
  criticRatings: number,
  directors: string,
  casts: string,
  genres: string[],
  trending: number
}