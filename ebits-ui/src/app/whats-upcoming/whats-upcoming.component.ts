import { Component, OnInit } from '@angular/core';
import { ServiceManagerService } from '../service-manager.service';

@Component({
  selector: 'app-whats-upcoming',
  templateUrl: './whats-upcoming.component.html',
  styleUrls: ['./whats-upcoming.component.scss']
})
export class WhatsUpcomingComponent implements OnInit {

  constructor(
    private serviceManager: ServiceManagerService) { }

  upcomigMovies: Movie[] = [];
  selectedMovie: Movie = <Movie> { };

  ngOnInit(): void {
    // upcoming Movies
    this.serviceManager.getWhatsNewMovies().subscribe(data => {
      this.upcomigMovies = data.movies;
      this.selectedMovie = this.upcomigMovies[0];
      console.log("Live Upcoming Movies  : ", this.upcomigMovies);
    });
  }

}

interface Movie {
  id: number,
  title: string,
  description: string,
  image: string,
  releaseYear: number,
  releaseDate: string,
  length: number,
  ebitsRatings: number,
  criticRatings: number,
  directors: string,
  casts: string,
  genres: string[],
  trending: number
}