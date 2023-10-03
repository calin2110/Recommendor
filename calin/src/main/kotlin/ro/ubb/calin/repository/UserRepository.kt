package ro.ubb.calin.repository

import org.springframework.data.jpa.repository.JpaRepository
import org.springframework.stereotype.Repository
import ro.ubb.calin.domain.Role
import ro.ubb.calin.domain.User
import java.util.*


interface UserRepository: JpaRepository<User, Long> {
    fun findByEmail(email: String): Optional<User>
    fun deleteByEmail(email: String)
    fun findAllByRoleNot(role: Role): List<User>
}