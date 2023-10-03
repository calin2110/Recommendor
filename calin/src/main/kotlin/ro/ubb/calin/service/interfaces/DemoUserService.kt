package ro.ubb.calin.service.interfaces

import org.springframework.util.MultiValueMap
import ro.ubb.calin.dto.CountDto
import ro.ubb.calin.dto.RatingDto

interface DemoUserService {
    fun getFilesForComparison(email: String): MultiValueMap<String, Any>
    fun addRating(email: String, ratingDto: RatingDto)
    fun countRatings(name: String): CountDto
}