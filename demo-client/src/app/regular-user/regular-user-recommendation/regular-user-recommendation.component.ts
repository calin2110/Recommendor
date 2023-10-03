import { Component, OnInit } from '@angular/core';
import {ActivatedRoute, Router} from "@angular/router";
import {RegularUserService} from "../../service/regular-user.service";
import {HttpResponse} from "@angular/common/http";
import {MultipartResponseInterpreterService} from "../../service/multipart-response-interpreter.service";

@Component({
  selector: 'app-regular-user-recommendation',
  templateUrl: './regular-user-recommendation.component.html',
  styleUrls: ['./regular-user-recommendation.component.css']
})
export class RegularUserRecommendationComponent implements OnInit {
  id: number
  audioFilesBytes: ArrayBuffer[] = []
  isLoading: boolean = false

  constructor(
    private activatedRoute: ActivatedRoute,
    private regularUserService: RegularUserService,
    private multipartResponseInterpreter: MultipartResponseInterpreterService,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.isLoading = true
    this.activatedRoute.params.subscribe(
      params => {
        this.id = params['id']
        this.regularUserService.getRecommendation(this.id).subscribe(
          (response: HttpResponse<ArrayBuffer>) => {
              this.audioFilesBytes = []
              const parts = this.multipartResponseInterpreter.parseMultipartResponse(response)
              const size = parts.size / 2
              for (let i = 1; i <= size; i++) {
                this.audioFilesBytes.push(parts.get(`file${i}`))
              }
              this.isLoading = false
          }
        )
      }
    )
  }

  goBackToSearch() {
    this.router.navigate(['regular-user/search'])
  }
}
