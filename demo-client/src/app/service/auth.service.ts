import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Observable} from "rxjs";
import {CookieService} from "ngx-cookie-service";
import {CurrentUser} from "../dto/CurrentUser";
import {AuthenticateResponse} from "../dto/AuthenticateResponse";
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  baseUrl: string = `${environment.protocol}://${environment.link}:${environment.port}/api`
  authApi: string = `${this.baseUrl}/auth`
  infoApi: string = `${this.baseUrl}/info`
  tokenName: string = 'recommendor_token'
  currentUser: CurrentUser | null = null

  constructor(
    private httpClient: HttpClient,
    private cookieService: CookieService
  ) { }

  authenticate(username: string, password: string): Observable<AuthenticateResponse> {
    return this.httpClient.post<any>(
      `${this.authApi}/authenticate`,
      {email : username, password: password}
    )
  }

  register(firstName: string, lastName: string, username: string, password: string): Observable<AuthenticateResponse> {
    return this.httpClient.post<any>(
      `${this.authApi}/register/regular`,
      {email: username, password: password, firstName: firstName, lastName: lastName}
    )
  }

  getCurrentUser(): Observable<CurrentUser> {
    return this.httpClient.get<CurrentUser>(
      `${this.infoApi}/user`,
      {headers: this.getHeaders()}
    )
  }

  getHeaders(contentType: string = 'application/json'): HttpHeaders {
    let headers = new HttpHeaders();
    if (!this.cookieService.check(this.tokenName)) {
      return headers;
    }
    const tokenValue = this.cookieService.get(this.tokenName)
    headers = headers.set('Authorization', `Bearer ${tokenValue}`)
    headers = headers.set('Content-Type', contentType)
    return headers;
  }

  logout() {
    this.cookieService.delete(this.tokenName)
    this.currentUser = null
  }
}
