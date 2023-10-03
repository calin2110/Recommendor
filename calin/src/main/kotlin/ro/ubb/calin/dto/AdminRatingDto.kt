package ro.ubb.calin.dto

data class AdminRatingDto(
    val genre: String,
    val subgenre1: String,
    val subgenre2: String,
    val rating: Int,
    val user: Long
)