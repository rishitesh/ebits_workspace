import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';

import { BrowserModule } from '@angular/platform-browser';
import { HighchartsChartModule } from 'highcharts-angular';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select'; 
import {MatToolbarModule} from '@angular/material/toolbar';
import {MatIconModule} from '@angular/material/icon';
import {MatTabsModule} from '@angular/material/tabs';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { SlickCarouselModule } from 'ngx-slick-carousel';

import { HeaderComponent } from './header/header.component';
import { FooterComponent } from './footer/footer.component';
import { SideNavigationComponent } from './side-navigation/side-navigation.component';
import { OttComponent } from './ott/ott.component';
import { BooksComponent } from './books/books.component';
import { PodcastsComponent } from './podcasts/podcasts.component';
import { GamesComponent } from './games/games.component';
import { OttScrollerComponent } from './ott-scroller/ott-scroller.component';
import { OttExplorerComponent } from './ott-explorer/ott-explorer.component';
import { OttBlogsComponent } from './ott-blogs/ott-blogs.component';
import { BestInStoryComponent } from './best-in-story/best-in-story.component';
import { MoodComponent } from './mood/mood.component';
import { EbitsTreasureComponent } from './ebits-treasure/ebits-treasure.component';
import { WhatsNewComponent } from './whats-new/whats-new.component';
import { WhatsUpcomingComponent } from './whats-upcoming/whats-upcoming.component';
import { WhatsInSpotsComponent } from './whats-in-spots/whats-in-spots.component';
import { MovieDetailsComponent } from './movie-details/movie-details.component';
import { MovieListingComponent } from './movie-listing/movie-listing.component';
import { NgxSliderModule } from '@angular-slider/ngx-slider';

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    FooterComponent,
    SideNavigationComponent,
    OttComponent,
    BooksComponent,
    PodcastsComponent,
    GamesComponent,
    OttScrollerComponent,
    OttExplorerComponent,
    OttBlogsComponent,
    BestInStoryComponent,
    MoodComponent,
    EbitsTreasureComponent,
    WhatsNewComponent,
    WhatsUpcomingComponent,
    WhatsInSpotsComponent,
    MovieDetailsComponent,
    MovieListingComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    AppRoutingModule,
    SlickCarouselModule,
    HighchartsChartModule,
    BrowserAnimationsModule,
    MatExpansionModule,
    MatFormFieldModule,
    MatSelectModule,
    MatToolbarModule,
    MatIconModule,
    MatTabsModule,
    NgxSliderModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
