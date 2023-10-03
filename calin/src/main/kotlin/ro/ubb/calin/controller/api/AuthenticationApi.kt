package ro.ubb.calin.controller.api

import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestMapping
import ro.ubb.calin.dto.AuthenticateRequest
import ro.ubb.calin.dto.AuthenticateResponse
import ro.ubb.calin.dto.RegisterRequest

@RequestMapping("/api/auth")
interface AuthenticationApi {
    @PostMapping("/authenticate")
    fun authenticate(authenticateRequest: AuthenticateRequest): ResponseEntity<AuthenticateResponse>

    @PostMapping("/register/demo")
    fun registerDemoUser(registerRequest: RegisterRequest): ResponseEntity<AuthenticateResponse>

    @PostMapping("/register/regular")
    fun registerRegularUser(registerRequest: RegisterRequest): ResponseEntity<AuthenticateResponse>
}