import { Component, OnInit } from '@angular/core';
import { ServiceManagerService } from '../service-manager.service';

@Component({
  selector: 'app-mood',
  templateUrl: './mood.component.html',
  styleUrls: ['./mood.component.scss']
})
export class MoodComponent implements OnInit {

  constructor(
    private serviceManager: ServiceManagerService) { }

  movieMoods: Mood[] = []

  ngOnInit(): void {
    // Moods
    this.serviceManager.getMovieMoods().subscribe(data => {
      this.movieMoods = data.moods;
      console.log("Live movie moods : ", this.movieMoods);
    });
  }

  moodsSlideConfig = {
    "slidesToShow": 7.1,
    "slidesToScroll": 1,
    "dots": true,
    "infinite": false
  };

  moodsMainSlideConfig = {
    "slidesToShow": 5,
    "slidesToScroll": 1,
    "dots": true,
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

interface Mood {
  id: number;
  name: string;
  photo: string;
}
