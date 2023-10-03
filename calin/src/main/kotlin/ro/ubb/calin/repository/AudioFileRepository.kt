package ro.ubb.calin.repository

import org.springframework.data.jpa.repository.JpaRepository
import ro.ubb.calin.domain.AudioFile
import ro.ubb.calin.domain.Genre
import java.util.*

interface AudioFileRepository: JpaRepository<AudioFile, Long> {
    fun findAllByGenre(genre: Genre): List<AudioFile>
    fun findAllByPath(path: String): Optional<AudioFile>
}