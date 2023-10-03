package ro.ubb.calin.service.interfaces

import ro.ubb.calin.dto.AdminRatingDto
import ro.ubb.calin.dto.UserDto

interface AdminService {
    fun deleteUser(email: String)
    fun updateUserGenre(email: String, genre: String): UserDto
    fun getAllUsers(): List<UserDto>
    fun getAllRatings(): List<AdminRatingDto>
}