import { Component, OnInit } from '@angular/core';
import {AuthService} from "../service/auth.service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-top-bar',
  templateUrl: './top-bar.component.html',
  styleUrls: ['./top-bar.component.css']
})
export class TopBarComponent implements OnInit {

  constructor(
    private authService: AuthService,
    private router: Router
  ) { }

  logout() {
    this.authService.logout()
    this.router.navigate(['/'])
  }

  ngOnInit(): void {
  }

  isLoggedIn(): boolean {
    return this.authService.currentUser != null
  }

  getTopBarText(): string {
    if (!this.isLoggedIn()) {
      return 'Logged Out'
    }
    switch (this.authService.currentUser?.role) {
      case 'ADMIN':
        return 'Admin'
      case 'DEMO_USER':
        return 'Demo User'
      case 'REGULAR_USER':
        return 'Regular User'
      default:
        return ''
    }
  }

  getButtonText() {
    if (this.isLoggedIn()) {
      return 'Logout'
    }
    return 'Login'
  }

  buttonClick() {
    if (this.isLoggedIn()) {
      this.logout()
    }
    this.router.navigate(['/authenticate'])
  }

  getMiddleText() {
    return this.authService.currentUser?.genre ?? ''
  }
}
