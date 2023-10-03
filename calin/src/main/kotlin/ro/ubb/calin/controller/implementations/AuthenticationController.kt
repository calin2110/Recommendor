package ro.ubb.calin.controller.implementations

import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.RestController
import ro.ubb.calin.controller.api.AuthenticationApi
import ro.ubb.calin.domain.Role
import ro.ubb.calin.dto.AuthenticateRequest
import ro.ubb.calin.dto.AuthenticateResponse
import ro.ubb.calin.dto.RegisterRequest
import ro.ubb.calin.service.interfaces.AuthenticationService

@RestController
class AuthenticationController(
    private val authenticationService: AuthenticationService
) : AuthenticationApi {

    override fun authenticate(@RequestBody authenticateRequest: AuthenticateRequest): ResponseEntity<AuthenticateResponse> {
        return ResponseEntity.ok(authenticationService.authenticate(authenticateRequest))
    }

    override fun registerDemoUser(@RequestBody registerRequest: RegisterRequest): ResponseEntity<AuthenticateResponse> {
        return ResponseEntity.ok(authenticationService.register(registerRequest, Role.DEMO_USER))
    }

    override fun registerRegularUser(@RequestBody registerRequest: RegisterRequest): ResponseEntity<AuthenticateResponse> {
        return ResponseEntity.ok(authenticationService.register(registerRequest, Role.REGULAR_USER))
    }
}