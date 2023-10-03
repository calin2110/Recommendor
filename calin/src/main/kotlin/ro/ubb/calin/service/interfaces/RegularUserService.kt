package ro.ubb.calin.service.interfaces

import org.springframework.util.MultiValueMap
import ro.ubb.calin.dto.RecommendationRequestDto

interface RegularUserService {
    fun getRecommendation(email: String, youtubeLink: String, limit: Int, top: Int): RecommendationRequestDto
    fun getHistoryOfRecommendations(email: String): List<RecommendationRequestDto>
    fun getRecommendation(recommendationRequestId: Long): MultiValueMap<String, Any>
}