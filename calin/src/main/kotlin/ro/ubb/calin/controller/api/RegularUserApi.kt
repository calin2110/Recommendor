package ro.ubb.calin.controller.api

import org.springframework.http.ResponseEntity
import org.springframework.security.access.prepost.PreAuthorize
import org.springframework.util.MultiValueMap
import org.springframework.web.bind.annotation.*
import ro.ubb.calin.dto.RecommendationRequest
import ro.ubb.calin.dto.RecommendationRequestDto
import java.security.Principal

@RequestMapping("/api/regular")
@PreAuthorize("hasRole('REGULAR_USER')")
interface RegularUserApi {
    @PostMapping("/recommendation/generate")
    fun getRecommendation(
        principal: Principal,
        @RequestBody recommendationRequest: RecommendationRequest
    ): ResponseEntity<RecommendationRequestDto>

    @GetMapping("/history")
    fun getHistoryOfRecommendations(principal: Principal): ResponseEntity<List<RecommendationRequestDto>>

    @GetMapping("/recommendation/get/{recommendationRequestId}")
    fun getRecommendation(@PathVariable recommendationRequestId: Long): ResponseEntity<MultiValueMap<String, Any>>
}