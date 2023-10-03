import { Component, OnInit } from '@angular/core';
import {RecommendationRequestDto} from "../../dto/RecommendationRequestDto";
import {RegularUserService} from "../../service/regular-user.service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-regular-user-history',
  templateUrl: './regular-user-history.component.html',
  styleUrls: ['./regular-user-history.component.css']
})
export class RegularUserHistoryComponent implements OnInit {
  isLoading: boolean = false
  recommendationRequests: RecommendationRequestDto[]

  constructor(
    private regularUserService: RegularUserService,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.isLoading = true
    this.regularUserService.getHistory().subscribe(
      (data: RecommendationRequestDto[]) => {
        this.recommendationRequests = data
        this.isLoading = false
      }
    )
  }

  seeDetails(id: number) {
    this.router.navigate([`regular-user/recommendation/${id}`])
  }

  goBackToSearch() {
    this.router.navigate(['regular-user/search'])
  }
}
