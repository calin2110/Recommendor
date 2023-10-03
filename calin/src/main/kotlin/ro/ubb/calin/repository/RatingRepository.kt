package ro.ubb.calin.repository

import org.springframework.data.jpa.repository.JpaRepository
import ro.ubb.calin.domain.UserRating

interface RatingRepository: JpaRepository<UserRating, Long> {
    fun countAllByUserId(userId: Long): Int
}