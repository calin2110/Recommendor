import {NgModule} from '@angular/core';
import {BrowserModule} from '@angular/platform-browser';

import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';
import {AuthenticateComponent} from './authenticate/authenticate.component';
import {RegisterComponent} from './register/register.component';
import {HttpClientModule} from "@angular/common/http";
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {DemoUserComponent} from './demo-user/demo-user.component';
import {AdminComponent} from './admin/admin.component';
import {TopBarComponent} from './top-bar/top-bar.component';
import {WavPlayerComponent} from './wav-player/wav-player.component';
import {RegularUserRecommendationComponent} from './regular-user/regular-user-recommendation/regular-user-recommendation.component';
import {RegularUserHistoryComponent} from "./regular-user/regular-user-history/regular-user-history.component";
import {RegularUserSearchComponent} from "./regular-user/regular-user-search/regular-user-search.component";

@NgModule({
  declarations: [
    AppComponent,
    AuthenticateComponent,
    RegisterComponent,
    DemoUserComponent,
    AdminComponent,
    TopBarComponent,
    WavPlayerComponent,
    RegularUserHistoryComponent,
    RegularUserSearchComponent,
    RegularUserRecommendationComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    HttpClientModule,
    ReactiveFormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {
}
