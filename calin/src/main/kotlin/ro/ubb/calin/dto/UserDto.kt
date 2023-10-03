package ro.ubb.calin.dto

data class UserDto(
    val firstName: String,
    val lastName: String,
    val email: String,
    val genre: String?,
    val canBeDeleted: Boolean,
    val ratingsCount: Int
)