import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {AuthService} from "./auth.service";
import {Observable} from "rxjs";
import {UserDto} from "../dto/UserDto";
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AdminService {
  url: string = `${environment.protocol}://${environment.link}:${environment.port}/api/admin`

  constructor(
    private httpClient: HttpClient,
    private authService: AuthService
  ) { }

  getUsers(): Observable<UserDto[]> {
    return this.httpClient.get<UserDto[]>(
      `${this.url}/all`,
      {headers: this.authService.getHeaders()}
    )
  }

  deleteUser(user: UserDto): Observable<string> {
    return this.httpClient.delete<string>(
      `${this.url}/delete/${user.email}`,
      {headers: this.authService.getHeaders()}
    )
  }

  updateUser(user: UserDto): Observable<string> {
    return this.httpClient.post<string>(
      `${this.url}/update`,
      {email: user.email, genre: user.genre},
      {headers: this.authService.getHeaders()
      }
    )
  }
}
