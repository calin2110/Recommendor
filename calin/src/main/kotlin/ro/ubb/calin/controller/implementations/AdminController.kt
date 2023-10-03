package ro.ubb.calin.controller.implementations

import org.springframework.beans.factory.annotation.Autowired
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.RestController
import ro.ubb.calin.controller.api.AdminApi
import ro.ubb.calin.dto.*
import ro.ubb.calin.service.interfaces.AdminService

@RestController
class AdminController @Autowired constructor(
    private val adminService: AdminService
) : AdminApi {
    override fun deleteUser(email: String): ResponseEntity<Response> {
        adminService.deleteUser(email)
        return ResponseEntity.ok(Response("User deleted successfully!"))
    }

    override fun updateUserGenre(updateUserDto: UpdateUserDto): ResponseEntity<Response> {
        val changedUser = adminService.updateUserGenre(updateUserDto.email, updateUserDto.genre)
        return ResponseEntity.ok(Response(changedUser.toString()))
    }

    override fun getAllUsers(): ResponseEntity<List<UserDto>> {
        return ResponseEntity.ok(adminService.getAllUsers())
    }

    override fun getAllRatings(): ResponseEntity<List<AdminRatingDto>> {
        return ResponseEntity.ok(adminService.getAllRatings())
    }
}