package ro.ubb.calin.repository

import org.springframework.data.jpa.repository.JpaRepository
import ro.ubb.calin.domain.Recommendation

interface RecommendationRepository: JpaRepository<Recommendation, Long> {
    fun getAllByRecommendationRequestId(userRecommendationRequestId: Long): List<Recommendation>
}