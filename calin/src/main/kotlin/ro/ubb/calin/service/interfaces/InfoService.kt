package ro.ubb.calin.service.interfaces

import ro.ubb.calin.dto.CurrentUserDto

interface InfoService {
    fun getCurrentUser(name: String): CurrentUserDto
}