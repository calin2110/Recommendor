import {Component, OnInit} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {CookieService} from "ngx-cookie-service";
import {Router} from "@angular/router";
import {AuthService} from "./service/auth.service";
import {AppRoutingModule} from "./app-routing.module";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  constructor(
    private router: Router,
    private cookieService: CookieService,
    private authService: AuthService
  ) { }

  ngOnInit() {
    if (this.authService.currentUser != null) {
      this.router.navigate([AppRoutingModule.getRouteForRole(this.authService.currentUser.role)])
      return;
    }

    if (this.cookieService.check(this.authService.tokenName)) {
      this.authService.getCurrentUser()
        .subscribe(
          data => {
            this.authService.currentUser = data
            this.router.navigate([AppRoutingModule.getRouteForRole(this.authService.currentUser.role)])
          },
          _ => {
            this.cookieService.delete(this.authService.tokenName)
            this.authService.currentUser = null
            this.router.navigate(['/authenticate'])
          }
        )
      return;
    }
  }
}
