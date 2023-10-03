package ro.ubb.calin.controller.api

import org.springframework.http.ResponseEntity
import org.springframework.security.access.prepost.PreAuthorize
import org.springframework.web.bind.annotation.*
import ro.ubb.calin.dto.*

@RequestMapping("/api/admin")
@PreAuthorize("hasRole('ADMIN')")
interface AdminApi {
    @DeleteMapping("/delete/{email}")
    fun deleteUser(@PathVariable email: String): ResponseEntity<Response>

    @PostMapping("/update")
    fun updateUserGenre(@RequestBody updateUserDto: UpdateUserDto): ResponseEntity<Response>

    @GetMapping("/all")
    fun getAllUsers(): ResponseEntity<List<UserDto>>

    @GetMapping("/ratings")
    fun getAllRatings(): ResponseEntity<List<AdminRatingDto>>
}