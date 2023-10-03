package ro.ubb.calin.controller.implementations

import org.springframework.beans.factory.annotation.Autowired
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.RestController
import ro.ubb.calin.controller.api.InfoApi
import ro.ubb.calin.dto.CurrentUserDto
import ro.ubb.calin.service.interfaces.InfoService
import java.security.Principal

@RestController
class InfoController @Autowired constructor(
    private val infoService: InfoService
) : InfoApi {
    override fun getCurrentUser(principal: Principal): ResponseEntity<CurrentUserDto> {
        return ResponseEntity.ok(infoService.getCurrentUser(principal.name))
    }
}