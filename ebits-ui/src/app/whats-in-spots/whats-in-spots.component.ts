import { Component, OnInit } from '@angular/core';
import { ServiceManagerService } from '../service-manager.service';

@Component({
  selector: 'app-whats-in-spots',
  templateUrl: './whats-in-spots.component.html',
  styleUrls: ['./whats-in-spots.component.scss']
})
export class WhatsInSpotsComponent implements OnInit {

  constructor(
    private serviceManager: ServiceManagerService) { }

   whatsInSpotMovies: Movie[] = []

  ngOnInit(): void {
    // Treasure Movies
    this.serviceManager.getWhatsInSpotMovies().subscribe(data => {
      this.whatsInSpotMovies = data.movies;
      console.log("Live movie getWhatsInSpotMovies : ", this.whatsInSpotMovies);
    });
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
  genres: string[]
}