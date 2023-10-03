package ro.ubb.calin.controller.implementations

import org.springframework.beans.factory.annotation.Autowired
import org.springframework.http.HttpHeaders
import org.springframework.http.MediaType
import org.springframework.http.ResponseEntity
import org.springframework.util.MultiValueMap
import org.springframework.web.bind.annotation.RestController
import ro.ubb.calin.controller.api.RegularUserApi
import ro.ubb.calin.dto.RecommendationRequest
import ro.ubb.calin.dto.RecommendationRequestDto
import ro.ubb.calin.service.interfaces.RegularUserService
import java.security.Principal

@RestController
class RegularUserController @Autowired constructor(
    private val regularUserService: RegularUserService
) : RegularUserApi {

    override fun getRecommendation(
        principal: Principal,
        recommendationRequest: RecommendationRequest
    ): ResponseEntity<RecommendationRequestDto> {
        return ResponseEntity.ok(
            regularUserService.getRecommendation(
                principal.name,
                recommendationRequest.youtubeLink,
                recommendationRequest.limit,
                recommendationRequest.top
            )
        )
    }

    override fun getRecommendation(recommendationRequestId: Long): ResponseEntity<MultiValueMap<String, Any>> {
        val headers = HttpHeaders()
        headers.contentType = MediaType.MULTIPART_FORM_DATA
        headers.setContentDispositionFormData("files", "files")
        return ResponseEntity.ok().headers(headers).body(regularUserService.getRecommendation(recommendationRequestId))
    }

    override fun getHistoryOfRecommendations(principal: Principal): ResponseEntity<List<RecommendationRequestDto>> {
        return ResponseEntity.ok(regularUserService.getHistoryOfRecommendations(principal.name))
    }
}