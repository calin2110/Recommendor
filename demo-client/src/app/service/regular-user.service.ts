import { Injectable } from '@angular/core';
import {environment} from "../../environments/environment";
import {HttpClient} from "@angular/common/http";
import {AuthService} from "./auth.service";
import {RecommendationRequestDto} from "../dto/RecommendationRequestDto";
import {Observable} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class RegularUserService {

  url: string = `${environment.protocol}://${environment.link}:${environment.port}/api/regular`

  constructor(
    private httpClient: HttpClient,
    private authService: AuthService
  ) { }

  getHistory(): Observable<RecommendationRequestDto[]> {
    const headers = this.authService.getHeaders()
    return this.httpClient.get<RecommendationRequestDto[]>(
      `${this.url}/history`,
      {headers: headers}
    )
  }

  createNewRecommendation(searchText: string): Observable<RecommendationRequestDto> {
    const headers = this.authService.getHeaders()
    return this.httpClient.post<RecommendationRequestDto>(
      `${this.url}/recommendation/generate`,
      {'youtubeLink': searchText, 'limit': -1, 'top': 3},
      {headers: headers}
    )
  }

  getRecommendation(id: number): Observable<any> {
    const headers = this.authService.getHeaders()
    return this.httpClient.get(
      `${this.url}/recommendation/get/${id}`,
      {
        headers,
        responseType: 'arraybuffer',
        observe: 'response'
      }
    )
  }
}
