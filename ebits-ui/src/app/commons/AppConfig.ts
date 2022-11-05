import { InjectionToken } from "@angular/core";

export interface AppConfig {
  product_name: string;
  host: string;
  port: number;
  baseURL: string;
  mode: string;
  webApi: { [index: string]: any };
  webApi_dummy: { [index: string]: any };
}

export let APP_CONFIG = new InjectionToken<AppConfig>('APP_CONFIG');

export class WebApi {

  public static readonly platforms: string = "platforms";
  public static readonly languages: string = "languages";
  public static readonly certificates: string = "certificates";
  public static readonly ethinicity: string = "ethinicity";
  public static readonly moods: string = "moods";
  public static readonly genres: string = "genres"
  public static readonly categories: string = "categories";
  public static readonly collection: string = "collection";
  public static readonly collections: string = "collections";
  public static readonly reports: string = "reports";
  public static readonly movies: string = "movies";
  public static readonly blogs: string = "blogs";

}
