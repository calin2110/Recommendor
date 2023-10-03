package ro.ubb.calin.handler

import org.springframework.http.HttpStatus
import org.springframework.http.ResponseEntity
import org.springframework.security.core.userdetails.UsernameNotFoundException
import org.springframework.web.bind.annotation.ControllerAdvice
import org.springframework.web.bind.annotation.ExceptionHandler
import ro.ubb.calin.exception.*

@ControllerAdvice
class ExceptionHandler {

    @ExceptionHandler(*[IllegalDeleteException::class, NoAuthoritiesException::class])
    fun handleIllegalDeleteException(exception: Exception): ResponseEntity<String> {
        return ResponseEntity(exception.message, HttpStatus.FORBIDDEN)
    }

    @ExceptionHandler(*[DuplicateEmailException::class])
    fun handleDuplicateEmailException(exception: Exception): ResponseEntity<String> {
        return ResponseEntity(exception.message, HttpStatus.CONFLICT)
    }

    @ExceptionHandler(*[InvalidEmailException::class, UsernameNotFoundException::class, InvalidPathException::class])
    fun handleUserExceptions(exception: Exception): ResponseEntity<String> {
        return ResponseEntity(exception.message, HttpStatus.NOT_FOUND)
    }
}