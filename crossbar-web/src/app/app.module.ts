import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';
import {FormsModule} from '@angular/forms';
import {HttpClientModule} from '@angular/common/http';
import {AppComponent} from './app.component';
import {AuthService} from "./services/auth.service";
import {AutobahnService} from "./services/autobahn.service";


@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    FormsModule,
    BrowserModule,
    HttpClientModule
  ],
  providers: [
    AuthService,
    AutobahnService
  ],
  bootstrap: [AppComponent]
})
export class AppModule {
}
