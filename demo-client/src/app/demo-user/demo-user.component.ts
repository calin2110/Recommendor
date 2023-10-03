import {Component, OnInit} from '@angular/core';
import {DemoUserService} from "../service/demo-user.service";
import {MultipartResponseInterpreterService} from "../service/multipart-response-interpreter.service";
import {AuthService} from "../service/auth.service";
import {HttpResponse} from "@angular/common/http";

@Component({
  selector: 'app-demo-user',
  templateUrl: './demo-user.component.html',
  styleUrls: ['./demo-user.component.css']
})
export class DemoUserComponent implements OnInit {
  file1: string
  content1: ArrayBuffer

  file2: string
  content2: ArrayBuffer

  isLoading: boolean
  counter: number
  inputValue: number
  errorMessage: string = ""

  constructor(
    private demoUserService: DemoUserService,
    public authService: AuthService,
    private multipartResponseInterpreter: MultipartResponseInterpreterService
  ) {
  }

  ngOnInit(): void {
    if (this.authService.currentUser?.genre != null) {
      this.fetch()
    }

    this.demoUserService.getCounter()
      .subscribe(
        counterDto => this.counter = counterDto.count
      )
  }

  private fetch() {
    this.isLoading = true
    this.demoUserService.getAudioFiles()
      .subscribe(
        (response: HttpResponse<ArrayBuffer>) => {
          const decoder = new TextDecoder()
          const parts = this.multipartResponseInterpreter.parseMultipartResponse(response)
          this.file1 = decoder.decode(parts.get('path1'))
          this.content1 = parts.get('file1')
          this.file2 = decoder.decode(parts.get('path2'))
          this.content2 = parts.get('file2')
          this.isLoading = false
        }
      )
  }

  handleInput() {
    if (this.inputValue == null) {
      this.errorMessage = "Please enter a rating!"
      return
    }
    if (!Number.isInteger(this.inputValue)) {
      this.errorMessage = "Only integer numbers are allowed!"
      return
    }
    if (this.inputValue < 0 || this.inputValue > 100) {
      this.errorMessage = "Only ratings between 0 and 100 are allowed!"
      return
    }
    this.errorMessage = ""
  }

  send() {
    if (this.errorMessage != "") {
      return
    }

    this.demoUserService.addRating(this.file1, this.file2, this.inputValue)
      .subscribe(
        () => {
          this.counter !! += 1
          this.inputValue = null
          this.fetch()
        },
        _ => {
          this.errorMessage = "Something went wrong!"
        }
      )

  }
}
