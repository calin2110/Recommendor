package ro.ubb.calin.service.implementations

import org.springframework.beans.factory.annotation.Autowired
import org.springframework.stereotype.Service
import ro.ubb.calin.domain.User
import ro.ubb.calin.dto.CurrentUserDto
import ro.ubb.calin.exception.InvalidEmailException
import ro.ubb.calin.repository.UserRepository
import ro.ubb.calin.service.interfaces.InfoService

@Service
class InfoServiceImpl @Autowired constructor(
    private val userRepository: UserRepository
) : InfoService {
    override fun getCurrentUser(name: String): CurrentUserDto {
        return getUserOrThrow(name).let {
            CurrentUserDto(
                role = it.role.name,
                genre = it.genre?.name
            )
        }
    }

    private fun getUserOrThrow(email: String): User {
        return userRepository.findByEmail(email).orElseThrow {
            throw InvalidEmailException("Cannot find user with email $email")
        }
    }
}