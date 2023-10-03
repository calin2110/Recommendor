import {Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {AuthService} from "./auth.service";
import {Observable} from "rxjs";
import {CountDto} from "../dto/CountDto";
import {environment} from "../../environments/environment";

@Injectable({
  providedIn: 'root'
})
export class DemoUserService {

  url: string = `${environment.protocol}://${environment.link}:${environment.port}/api/demo`

  constructor(
    private httpClient: HttpClient,
    private authService: AuthService
  ) {
  }

  getAudioFiles(): Observable<any> {
    const headers = this.authService.getHeaders()
    return this.httpClient.get(
      `${this.url}/get`,
      {
        headers,
        responseType: 'arraybuffer',
        observe: 'response'
      }
    )
  }

  getCounter(): Observable<CountDto> {
    const headers = this.authService.getHeaders()
    return this.httpClient.get<CountDto>(
      `${this.url}/count`,
      {headers: headers}
    )
  }

  addRating(path1: string, path2: string, rating: number): Observable<any> {
    const headers = this.authService.getHeaders()
    return this.httpClient.post(
      `${this.url}/add`,
      {'audioFilePath1': path1, 'audioFilePath2': path2, 'rating': rating},
      {headers: headers}
    )
  }
}
