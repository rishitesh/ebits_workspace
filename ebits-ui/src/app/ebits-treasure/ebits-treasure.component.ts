import { Component, OnInit } from '@angular/core';
import { ServiceManagerService } from '../service-manager.service';

@Component({
  selector: 'app-ebits-treasure',
  templateUrl: './ebits-treasure.component.html',
  styleUrls: ['./ebits-treasure.component.scss']
})
export class EbitsTreasureComponent implements OnInit {

  constructor(
    private serviceManager: ServiceManagerService) { }

  movieTreasure: Movie[] = []

  ngOnInit(): void {
    // Treasure Movies
    this.serviceManager.getMovieTreasure().subscribe(data => {
      this.movieTreasure = data.movies;
      console.log("Live movie Treasure : ", this.movieTreasure);
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