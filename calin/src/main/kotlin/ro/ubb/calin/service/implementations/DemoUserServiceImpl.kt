package ro.ubb.calin.service.implementations

import org.springframework.beans.factory.annotation.Autowired
import org.springframework.core.io.FileSystemResource
import org.springframework.stereotype.Service
import org.springframework.util.LinkedMultiValueMap
import org.springframework.util.MultiValueMap
import ro.ubb.calin.domain.UserRating
import ro.ubb.calin.dto.AudioFileDtoBuilder
import ro.ubb.calin.dto.CountDto
import ro.ubb.calin.dto.RatingDto
import ro.ubb.calin.exception.InvalidEmailException
import ro.ubb.calin.exception.InvalidPathException
import ro.ubb.calin.repository.AudioFileRepository
import ro.ubb.calin.repository.RatingRepository
import ro.ubb.calin.repository.UserRepository
import ro.ubb.calin.service.interfaces.DemoUserService
import java.nio.file.Path

@Service
class DemoUserServiceImpl @Autowired constructor(
    private val audioFileRepository: AudioFileRepository,
    private val userRepository: UserRepository,
    private val ratingRepository: RatingRepository
) : DemoUserService {

    override fun getFilesForComparison(email: String): MultiValueMap<String, Any> {
        val genre = userRepository.findByEmail(email).orElseThrow {
            InvalidEmailException("Email does not exist")
        }.genre
        val audioFiles = audioFileRepository.findAllByGenre(genre!!)

        val firstAudioFile = audioFiles.random()
        val secondAudioFile = audioFiles.filter { it.subgenre != firstAudioFile.subgenre }.random()

        return AudioFileDtoBuilder().addAudioFile(firstAudioFile.path).addAudioFile(secondAudioFile.path).build()
    }

    override fun addRating(email: String, ratingDto: RatingDto) {
        val user = userRepository.findByEmail(email).orElseThrow { InvalidEmailException("Email does not exist") }
        ratingRepository.save(
            UserRating(
                userId = user.id,
                subgenre1 = getSubgenreOfPath(ratingDto.audioFilePath1),
                subgenre2 = getSubgenreOfPath(ratingDto.audioFilePath2),
                rating = ratingDto.rating
            )
        )
    }

    override fun countRatings(name: String): CountDto {
        val user = userRepository.findByEmail(name).orElseThrow { InvalidEmailException("Email does not exist") }
        return CountDto(ratingRepository.countAllByUserId(user.id))
    }

    private fun getSubgenreOfPath(path: String): String {
        return audioFileRepository.findAllByPath(path).orElseThrow {
            InvalidPathException("Path does not exist")
        }.subgenre
    }
}