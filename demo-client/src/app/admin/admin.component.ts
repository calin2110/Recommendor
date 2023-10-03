import {Component, OnInit} from '@angular/core';
import {UserDto} from "../dto/UserDto";
import {AdminService} from "../service/admin.service";

@Component({
  selector: 'app-admin',
  templateUrl: './admin.component.html',
  styleUrls: ['./admin.component.css']
})
export class AdminComponent implements OnInit {
  genres = ['METAL', 'ROCK', 'POP', 'CLASSICAL', 'JAZZ', 'BLUES', 'HIP_HOP', 'COUNTRY', 'DISCO', 'REGGAE']
  private fetchedUsers: UserDto[] = []
  private changedUsers: Set<string> = new Set<string>()
  users: UserDto[] = []
  mobilePortrait: boolean = false
  filter = ''
  loading = false

  constructor(private adminService: AdminService) {
    this.fetchUsers()
  }

  ngOnInit(): void {
    this.mobilePortrait = window.innerWidth <= 768
    window.onresize = () => {
        this.mobilePortrait = window.innerWidth <= 768
    }
  }

  setSaveOn(user: UserDto) {
    this.changedUsers.add(user.email)
  }

  filterUsers() {
    this.users = this.fetchedUsers.filter(
      user => user.email.toLowerCase().includes(this.filter.toLowerCase())
    )
  }

  isUserChanged(user: UserDto) {
    return this.changedUsers.has(user.email)
  }

  private fetchUsers() {
    this.loading = true
    this.adminService.getUsers().subscribe(
      users => {
        this.filter = ''
        this.fetchedUsers = users
        this.users = users
        this.loading = false
      }
    )
  }

  saveUser(user: UserDto) {
    this.adminService.updateUser(user).subscribe(
      () => {
        this.changedUsers.delete(user.email)
        this.fetchUsers()
      }
    )
  }

  deleteUser(user: UserDto) {
    this.adminService.deleteUser(user).subscribe(
      () => {
        this.changedUsers.delete(user.email)
        this.fetchUsers()
      }
    )
  }
}
