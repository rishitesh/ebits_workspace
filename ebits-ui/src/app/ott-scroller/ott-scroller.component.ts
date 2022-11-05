import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import * as Highcharts from 'highcharts';
import { ServiceManagerService } from '../service-manager.service';

declare var $: any;

@Component({
  selector: 'app-ott-scroller',
  templateUrl: './ott-scroller.component.html',
  styleUrls: ['./ott-scroller.component.scss']
})
export class OttScrollerComponent implements OnInit {

  constructor(
    private httpClient: HttpClient,
    private serviceManager: ServiceManagerService) { }

  highcharts = Highcharts;
  chartOptions: Highcharts.Options = { }; 

  collections: Collection[] = [];
  selectedCollection: Collection | undefined = undefined;
  reports: Report[] = [];

  ngOnInit(): void {
    // Gcollections
    this.serviceManager.getCollections().subscribe(data => {
      this.collections = data.collections;
      console.log("Live collections" , this.collections);
      
    });
    // Reports
    this.serviceManager.getReports().subscribe(data => {
      this.reports = data.reports;
      console.log("Live reports" , this.reports);
    });
  }

  collectionSlideConfig = {
    "slidesToShow": 3.2,
    "slidesToScroll": 1,
    "dots": false,
    "infinite": false
  };

  reportSlideConfig = {
    "slidesToShow": 1.1,
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

  collectionsDrawerHeight = "0%";
  openCollectionDrawer(collectionId: number) {
    console.log('openCollectionDrawer');
    this.selectedCollection = this.collections.find((collection) => {
      return collection.id === collectionId;
    } );
    console.log(this.collections[0].entries.length);
    this.collectionsDrawerHeight = "1100px";
  }

  closeCollectionDrawer() {
    console.log('closeCollectionDrawer');
    // document.getElementById("collectionsDrawer").style.height = "0%";
    this.collectionsDrawerHeight = "0%";
  }

}

interface Collection {
  id: number;
  name: string;
  bgImage: string;
  entries: CollectionEntry[];
}

interface CollectionEntry {
  id: number;
  name: string;
  ebitsRatings: number;
  image: string;
}

interface Report {
  title: string;
  summary: string;
  chartImage: string;
  chart: {
    highchartOptions: Object
  }
}
