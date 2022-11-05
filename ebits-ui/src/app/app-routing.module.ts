import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { BooksComponent } from './books/books.component';
import { GamesComponent } from './games/games.component';
import { MovieDetailsComponent } from './movie-details/movie-details.component';
import { MovieListingComponent } from './movie-listing/movie-listing.component';
import { OttComponent } from './ott/ott.component';
import { PodcastsComponent } from './podcasts/podcasts.component';

const routes: Routes = [
  { path: '', component: OttComponent},
  { path: 'ott', component: OttComponent},
  { path: 'books', component: BooksComponent},
  { path: 'podcasts', component: PodcastsComponent},
  { path: 'games', component: GamesComponent},
  { path: 'details', component: MovieDetailsComponent},
  { path: 'listing', component: MovieListingComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
