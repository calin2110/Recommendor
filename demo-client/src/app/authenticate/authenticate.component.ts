import { Component, OnInit } from '@angular/core';
import {FormBuilder} from "@angular/forms";
import {AuthService} from "../service/auth.service";
import {CookieService} from "ngx-cookie-service";
import {Router} from "@angular/router";
import {AppRoutingModule} from "../app-routing.module";

@Component({
  selector: 'app-authenticate',
  templateUrl: './authenticate.component.html',
  styleUrls: ['./authenticate.component.css']
})
export class AuthenticateComponent implements OnInit {

  authenticateForm = this.formBuilder.group({
    email: '',
    password: '',
  })
  errorMessage: string | null = null

  constructor(private formBuilder: FormBuilder,
              private authService: AuthService,
              private cookieService: CookieService,
              private router: Router
  ) { }

  ngOnInit(): void {
  }

  authenticate() {
      const email = this.authenticateForm.get('email')!!.value
      const password = this.authenticateForm.get('password')!!.value
      this.authService.authenticate(email, password).subscribe(
          response => {
              this.authService.currentUser = {role: '', genre: null}
              this.cookieService.set(this.authService.tokenName, response.token, {expires: 2})
              this.authService.getCurrentUser()
                .subscribe(
                  data => {
                    this.authService.currentUser = data
                    this.router.navigate([AppRoutingModule.getRouteForRole(this.authService.currentUser.role)])
                  }
                )
              this.errorMessage = null
          },
          _ => {
              this.errorMessage = 'Invalid credentials, try again!'
          }
      )
  }

  goToRegister() {
    this.router.navigate(['/register'])
  }
}
