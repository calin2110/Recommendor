package ro.ubb.calin.controller.api

import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RequestMapping
import ro.ubb.calin.dto.CurrentUserDto
import java.security.Principal

@RequestMapping("/api/info")
interface InfoApi {
    @GetMapping("/user")
    fun getCurrentUser(principal: Principal): ResponseEntity<CurrentUserDto>
}