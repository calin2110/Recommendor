package ro.ubb.calin.service.implementations

import org.springframework.beans.factory.annotation.Autowired
import org.springframework.stereotype.Service
import org.springframework.transaction.annotation.Transactional
import ro.ubb.calin.domain.Genre
import ro.ubb.calin.domain.Role
import ro.ubb.calin.dto.AdminRatingDto
import ro.ubb.calin.dto.UserDto
import ro.ubb.calin.exception.IllegalDeleteException
import ro.ubb.calin.exception.InvalidEmailException
import ro.ubb.calin.repository.RatingRepository
import ro.ubb.calin.repository.RecommendationRequestRepository
import ro.ubb.calin.repository.UserRepository
import ro.ubb.calin.service.interfaces.AdminService

@Service
class AdminServiceImpl @Autowired constructor(
    private val userRepository: UserRepository,
    private val ratingRepository: RatingRepository,
    private val recommendationRequestRepository: RecommendationRequestRepository
) : AdminService {

    @Transactional
    override fun deleteUser(email: String) {
        validateUserModification(email)
        userRepository.deleteByEmail(email)
    }

    @Transactional
    override fun updateUserGenre(email: String, genre: String): UserDto {
        validateUserModification(email)
        val user = userRepository.findByEmail(email).get()
        val savedUser = userRepository.save(user.copy(genre = Genre.valueOf(genre)))
        return UserDto(
            firstName = savedUser.firstName,
            lastName = savedUser.lastName,
            email = savedUser.email,
            genre = savedUser.genre?.name,
            canBeDeleted = canUserBeDeleted(savedUser.id),
            ratingsCount = 0
        )
    }

    override fun getAllUsers(): List<UserDto> {
        return userRepository.findAllByRoleNot(Role.ADMIN)
            .map {
                UserDto(
                    firstName = it.firstName,
                    lastName = it.lastName,
                    email = it.email,
                    genre = it.genre?.name,
                    canBeDeleted = canUserBeDeleted(it.id),
                    ratingsCount = ratingRepository.countAllByUserId(it.id)
                )
            }
            .toList()
    }

    override fun getAllRatings(): List<AdminRatingDto> {
        return ratingRepository.findAll()
            .map {
                AdminRatingDto(
                    subgenre1 = it.subgenre1,
                    subgenre2 = it.subgenre2,
                    rating = it.rating,
                    genre = getUserGenreById(it.userId),
                    user = it.userId
                )
            }
            .toList()
    }

    private fun getUserGenreById(id: Long): String {
        return userRepository.findById(id).orElseThrow {
            InvalidEmailException("Cannot find user with id $id")
        }.genre.toString()
    }

    private fun validateUserModification(email: String) {
        val user = userRepository.findByEmail(email).orElseThrow {
            InvalidEmailException("Cannot find username with email $email")
        }
        if (user.role == Role.ADMIN) {
            throw IllegalDeleteException("Cannot modify admin user $email")
        }
        if (ratingRepository.countAllByUserId(user.id) > 0) {
            throw IllegalDeleteException("Cannot modify user $email because it has ratings")
        }
        if (recommendationRequestRepository.countAllByUserId(user.id) > 0) {
            throw IllegalDeleteException("Cannot modify user $email because it has recommendation requests")
        }
    }

    private fun canUserBeDeleted(userId: Long): Boolean {
        return ratingRepository.countAllByUserId(userId) == 0 && recommendationRequestRepository.countAllByUserId(userId) == 0
    }
}