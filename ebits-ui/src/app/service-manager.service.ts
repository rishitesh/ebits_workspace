import { Inject, Injectable } from '@angular/core';
import { HttpClient, HttpRequest } from '@angular/common/http';
import { HttpHeaders } from '@angular/common/http';
// import { MatSnackBar } from '@angular/material';
import { Observable } from 'rxjs';
// import { Router } from '@angular/router';
import { AppConfig, APP_CONFIG, WebApi } from './commons/AppConfig';
@Injectable({
  providedIn: 'root'
})
export class ServiceManagerService {

  private appConfig!: AppConfig;
  private WEBAPI: { [index: string]: any } = {};

  constructor(
    @Inject(APP_CONFIG) config: AppConfig,
    private httpClient: HttpClient,
    // public snackBar: MatSnackBar,
    // private router: Router
  ) {
    this.appConfig = config;
    if (this.appConfig.mode === "dev") {
      this.WEBAPI = this.appConfig?.webApi_dummy;
    } else {
      this.WEBAPI = this.appConfig?.webApi;
    }
  }

  public getCategories(): Observable<any> {
    return this.httpClient.get(
      this.appConfig.baseURL + this.WEBAPI[WebApi.categories].url);
  }

  public getPlatforms(): Observable<any> {
    return this.httpClient.get(
      this.appConfig.baseURL + this.WEBAPI[WebApi.platforms].url);
  }

  public getLanguages(): Observable<any> {
    return this.httpClient.get(
      this.appConfig.baseURL + this.WEBAPI[WebApi.languages].url);
  }

  public getEthinicities(): Observable<any> {
    return this.httpClient.get(this.WEBAPI[WebApi.ethinicity].url);
  }

  public getCertifications(): Observable<any> {
    return this.httpClient.get(
      this.appConfig.baseURL + this.WEBAPI[WebApi.certificates].url);
  }

  public getCollections(): Observable<any> {
    return this.httpClient.get(this.WEBAPI[WebApi.collections].url);
  }

  public getReports(): Observable<any> {
    return this.httpClient.get(this.WEBAPI[WebApi.reports].url);
  }

  public getMovies(): Observable<any> {
    return this.httpClient.get(this.WEBAPI[WebApi.movies].url);
  }
  
  public getMoviesSimilarByGenre(): Observable<any> {
    return this.httpClient.get("assets/data/movies-similarbygenre.json");
  }

  public getMovieDetails(): Observable<any> {
    return this.httpClient.get("assets/data/movie-details.json");
  }

  public getMovieGeners(): Observable<any> {
    return this.httpClient.get(
      this.appConfig.baseURL + this.WEBAPI[WebApi.genres].url);
  }

  public getMovieMoods(): Observable<any> {
    return this.httpClient.get(
      this.appConfig.baseURL + this.WEBAPI[WebApi.moods].url);
  }

  public getMovieTreasure(): Observable<any> {
    return this.httpClient.get("assets/data/treasure.json");
  }

  public getWhatsNewMovies(): Observable<any> {
    return this.httpClient.get("assets/data/trending-movies.json");
  }

  public getWhatsUpcomingMovies(): Observable<any> {
    return this.httpClient.get("assets/data/treasure.json");
  }

  public getWhatsInSpotMovies(): Observable<any> {
    return this.httpClient.get("assets/data/movies-in-spot.json");
  }

  public getBlogs(): Observable<any> {
    return this.httpClient.get(this.WEBAPI[WebApi.blogs].url);
  }

  /* public requestAPICall(apiKey, urlParams, body, ...args: any[]) {
    var configData = JSON.parse(this.getConfigData())['api'][apiKey]
    var serviceUrl = this.getParsedUrlByJson(configData['url'], urlParams);
    var options = this.getHttpOptions(apiKey)
    if (args.length > 0) {
      for (let argument of args) {
        if (argument['type'] == 'Content-Type') {
          options = this.getHttpOptions(apiKey, argument)
        }
        if (argument['type'] == 'Authorization') {
          options = this.getHttpOptions(apiKey, argument)
        }
      }
    }
    switch (configData['method']) {
      case 'get':
        return this.GetServiceManagerAPI(serviceUrl, options)
      case 'put':
        return this.PutServiceManagerAPI(serviceUrl, body, options)
      case 'post':
        return this.PostServiceManagerAPI(serviceUrl, body, options)
      case 'delete':
        return this.DeleteServiceManagerAPI(serviceUrl, body, options)
      default:
        break;
    }
  } */
}
