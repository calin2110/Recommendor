package ro.ubb.calin.dto

data class RecommendationRequest(
    val youtubeLink: String,
    val limit: Int,
    val top: Int
)