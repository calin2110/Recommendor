package ro.ubb.calin.service.implementations

import org.springframework.beans.factory.annotation.Autowired
import org.springframework.security.authentication.AuthenticationManager
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken
import org.springframework.security.core.userdetails.UsernameNotFoundException
import org.springframework.security.crypto.password.PasswordEncoder
import org.springframework.stereotype.Service
import org.springframework.transaction.annotation.Transactional
import ro.ubb.calin.configuration.JwtService
import ro.ubb.calin.domain.Role
import ro.ubb.calin.domain.User
import ro.ubb.calin.dto.AuthenticateRequest
import ro.ubb.calin.dto.AuthenticateResponse
import ro.ubb.calin.dto.RegisterRequest
import ro.ubb.calin.exception.DuplicateEmailException
import ro.ubb.calin.repository.UserRepository
import ro.ubb.calin.service.interfaces.AuthenticationService

@Service
class AuthenticationServiceImpl @Autowired constructor(
    private val userRepository: UserRepository,
    private val passwordEncoder: PasswordEncoder,
    private val jwtService: JwtService,
    private val authenticationManager: AuthenticationManager,
) : AuthenticationService {

    override fun authenticate(authenticateRequest: AuthenticateRequest): AuthenticateResponse {
        authenticationManager.authenticate(
            UsernamePasswordAuthenticationToken(
                authenticateRequest.email,
                authenticateRequest.password
            )
        )
        val user = userRepository.findByEmail(authenticateRequest.email)
            .orElseThrow { UsernameNotFoundException("User not found") }
        return generateTokenFromUser(user)
    }

    @Transactional
    override fun register(registerRequest: RegisterRequest, role: Role): AuthenticateResponse {
        userRepository.findByEmail(registerRequest.email)
            .ifPresent {
                throw DuplicateEmailException("Email already exists!")
            }

        val user = User(
            firstName = registerRequest.firstName,
            lastName = registerRequest.lastName,
            email = registerRequest.email,
            password = passwordEncoder.encode(registerRequest.password),
            role = role,
            genre = null
        )
        userRepository.save(user)
        return generateTokenFromUser(user)
    }

    private fun generateTokenFromUser(user: User): AuthenticateResponse {
        val token = jwtService.generateToken(user)
        return AuthenticateResponse(
            token = token
        )
    }
}