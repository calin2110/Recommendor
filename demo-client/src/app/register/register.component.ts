import { Component, OnInit } from '@angular/core';
import {FormBuilder} from "@angular/forms";
import {AuthService} from "../service/auth.service";
import {CookieService} from "ngx-cookie-service";
import {Router} from "@angular/router";
import {AppRoutingModule} from "../app-routing.module";

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {
  registerForm = this.formBuilder.group({
    firstName: '',
    lastName: '',
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

  register() {
    const email = this.registerForm.get('email')!!.value
    const password = this.registerForm.get('password')!!.value
    const firstName = this.registerForm.get('firstName')!!.value
    const lastName = this.registerForm.get('lastName')!!.value
    this.authService.register(firstName, lastName, email, password).subscribe(
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
      error => {
        if (error.status === 409) {
          this.errorMessage = 'Email already exists!'
          return
        }
        this.errorMessage = 'Something went wrong, please try again!'
      }
    )
  }
}
