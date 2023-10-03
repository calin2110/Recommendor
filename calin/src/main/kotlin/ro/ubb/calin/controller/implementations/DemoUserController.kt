package ro.ubb.calin.controller.implementations

import org.springframework.beans.factory.annotation.Autowired
import org.springframework.http.HttpHeaders
import org.springframework.http.MediaType
import org.springframework.http.ResponseEntity
import org.springframework.security.core.Authentication
import org.springframework.security.core.annotation.AuthenticationPrincipal
import org.springframework.security.core.userdetails.User
import org.springframework.security.core.userdetails.UserDetails
import org.springframework.security.core.userdetails.UserDetailsService
import org.springframework.util.MultiValueMap
import org.springframework.web.bind.annotation.RestController
import ro.ubb.calin.controller.api.DemoUserApi
import ro.ubb.calin.dto.CountDto
import ro.ubb.calin.dto.RatingDto
import ro.ubb.calin.dto.Response
import ro.ubb.calin.service.interfaces.DemoUserService
import java.security.Principal

@RestController
class DemoUserController @Autowired constructor(
    private val demoUserService: DemoUserService
) : DemoUserApi {

    override fun getFilesForComparison(principal: Principal): ResponseEntity<MultiValueMap<String, Any>> {
        val body = demoUserService.getFilesForComparison(principal.name)
        val headers = HttpHeaders()
        headers.contentType = MediaType.MULTIPART_FORM_DATA
        headers.setContentDispositionFormData("files", "files")
        return ResponseEntity.ok().headers(headers).body(body)
    }

    override fun addRating(principal: Principal, ratingDto: RatingDto): ResponseEntity<Response> {
        demoUserService.addRating(principal.name, ratingDto)
        return ResponseEntity.ok(Response("Rating added successfully!"))
    }

    override fun countRatings(principal: Principal): ResponseEntity<CountDto> {
        return ResponseEntity.ok(demoUserService.countRatings(principal.name))
    }

}