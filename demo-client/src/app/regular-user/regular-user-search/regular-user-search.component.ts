import {Component, OnInit} from '@angular/core';
import {Router} from "@angular/router";
import {RegularUserService} from "../../service/regular-user.service";

@Component({
  selector: 'app-regular-user-search',
  templateUrl: './regular-user-search.component.html',
  styleUrls: ['./regular-user-search.component.css']
})
export class RegularUserSearchComponent implements OnInit {
  errorMessage: string | null = null
  searchText: any
  youtubeLink: string = ''
  isLoading: boolean = false

  constructor(
    private router: Router,
    private regularUserService: RegularUserService
  ) {
  }

  ngOnInit(): void {
  }

  recommend() {
    this.isLoading = true
    this.regularUserService.createNewRecommendation(this.youtubeLink).subscribe(
      (data) => {
        this.isLoading = false
        this.router.navigate(['regular-user/recommendation', data.id])
      },
      (error) => {
        this.isLoading = false
        this.errorMessage = error.error
      }
    )

  }

  goToHistory() {
    this.router.navigate(['regular-user/history'])
  }

}
