package ro.ubb.calin.repository

import org.springframework.data.jpa.repository.JpaRepository
import ro.ubb.calin.domain.RecommendationRequest

interface RecommendationRequestRepository: JpaRepository<RecommendationRequest, Long> {
    fun getAllByUserId(userId: Long): List<RecommendationRequest>
    fun countAllByUserId(id: Long): Int
}