import { Component, OnInit } from '@angular/core';
import { ServiceManagerService } from '../service-manager.service';

@Component({
  selector: 'app-best-in-story',
  templateUrl: './best-in-story.component.html',
  styleUrls: ['./best-in-story.component.scss']
})
export class BestInStoryComponent implements OnInit {

  constructor(
    private serviceManager: ServiceManagerService) { }

  movies: Movie[] = [];

  ngOnInit(): void {
    // Movies
    this.serviceManager.getMovies().subscribe(data => {
      this.movies = data.movies;
      console.log("Live movies : " , this.movies);
    });
  }

  bisSlideConfig = {
    "slidesToShow": 3,
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
  title: string;
  image: string;
  ebitsRatings: number;
}
