package ro.ubb.calin.service.interfaces

import ro.ubb.calin.domain.Role
import ro.ubb.calin.dto.AuthenticateRequest
import ro.ubb.calin.dto.AuthenticateResponse
import ro.ubb.calin.dto.RegisterRequest

interface AuthenticationService {
    fun authenticate(authenticateRequest: AuthenticateRequest): AuthenticateResponse
    fun register(registerRequest: RegisterRequest, role: Role): AuthenticateResponse
}