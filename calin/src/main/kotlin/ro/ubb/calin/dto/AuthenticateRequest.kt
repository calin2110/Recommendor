package ro.ubb.calin.dto

data class AuthenticateRequest(
    val email: String = "",
    val password: String = ""
)