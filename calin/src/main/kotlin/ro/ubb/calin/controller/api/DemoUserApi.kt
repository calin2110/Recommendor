package ro.ubb.calin.controller.api

import org.springframework.http.ResponseEntity
import org.springframework.security.access.prepost.PreAuthorize
import org.springframework.util.MultiValueMap
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.RequestMapping
import ro.ubb.calin.dto.CountDto
import ro.ubb.calin.dto.RatingDto
import ro.ubb.calin.dto.Response
import java.security.Principal

@RequestMapping("/api/demo")
@PreAuthorize("hasRole('DEMO_USER')")
interface DemoUserApi {
    @GetMapping("/get")
    fun getFilesForComparison(principal: Principal): ResponseEntity<MultiValueMap<String, Any>>

    @PostMapping("/add")
    fun addRating(principal: Principal, @RequestBody ratingDto: RatingDto): ResponseEntity<Response>

    @GetMapping("/count")
    fun countRatings(principal: Principal): ResponseEntity<CountDto>
}