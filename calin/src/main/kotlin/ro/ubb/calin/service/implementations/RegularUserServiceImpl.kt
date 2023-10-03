package ro.ubb.calin.service.implementations

import jakarta.transaction.Transactional
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.stereotype.Service
import org.springframework.util.MultiValueMap
import ro.ubb.calin.domain.AudioFile
import ro.ubb.calin.domain.Recommendation
import ro.ubb.calin.domain.RecommendationRequest
import ro.ubb.calin.dto.AudioFileDtoBuilder
import ro.ubb.calin.dto.RecommendationRequestDto
import ro.ubb.calin.exception.InvalidPathException
import ro.ubb.calin.repository.RecommendationRepository
import ro.ubb.calin.repository.RecommendationRequestRepository
import ro.ubb.calin.repository.UserRepository
import ro.ubb.calin.service.interfaces.RegularUserService
import ro.ubb.calin.tcp.TCPSocket

@Service
class RegularUserServiceImpl @Autowired constructor(
    private val recommendationRequestRepository: RecommendationRequestRepository,
    private val recommendationRepository: RecommendationRepository,
    private val userRepository: UserRepository
) : RegularUserService {

    @Transactional
    override fun getRecommendation(
        email: String,
        youtubeLink: String,
        limit: Int,
        top: Int
    ): RecommendationRequestDto {
        val user = userRepository.findByEmail(email).orElseThrow {
            throw InvalidPathException("Cannot find user with email $email")
        }

        val host = "localhost"
//        val portStr = System.getenv("RECOMMENDER_SERVER_COMMUNICATION_PORT")
        val port = 1337

        TCPSocket(host, port).use { socket ->

            socket.prepareForCommunication(TCPSocket.Type.INT)
                .send(limit)
                .send(top)
            socket.prepareForCommunication(TCPSocket.Type.STRING)
                .send(youtubeLink)

            val result = socket.prepareForCommunication(TCPSocket.Type.INT)
                .receive() as Int
            if (result == -1) {
                val errorMessage = socket.prepareForCommunication(TCPSocket.Type.STRING)
                    .receive() as String
                throw InvalidPathException(errorMessage)
            }

            val savedRecommendationRequest = recommendationRequestRepository.save(
                RecommendationRequest(
                    youtubeLink = youtubeLink,
                    userId = user.id
                )
            )

            val obtainedLimit = socket.prepareForCommunication(TCPSocket.Type.INT).receive() as Int
            socket.prepareForCommunication(TCPSocket.Type.LONG)
            for (i in 0 until obtainedLimit) {
                val pathId = socket.receive() as Long
                recommendationRepository.save(
                    Recommendation(
                        recommendedAudioFile = AudioFile(id = pathId),
                        recommendationRequestId = savedRecommendationRequest.id
                    )
                )
            }

            return RecommendationRequestDto(
                id = savedRecommendationRequest.id,
                youtubeLink = savedRecommendationRequest.youtubeLink
            )
        }
    }

    override fun getRecommendation(recommendationRequestId: Long): MultiValueMap<String, Any> {
        var builder = AudioFileDtoBuilder()
        recommendationRepository.getAllByRecommendationRequestId(recommendationRequestId).forEach {
            builder = builder.addAudioFile(it.recommendedAudioFile.path)
        }
        return builder.build()
    }

    override fun getHistoryOfRecommendations(email: String): List<RecommendationRequestDto> {
        val user = userRepository.findByEmail(email).orElseThrow {
            throw InvalidPathException("Cannot find user with email $email")
        }
        return recommendationRequestRepository.getAllByUserId(user.id).map {
            RecommendationRequestDto(
                id = it.id,
                youtubeLink = it.youtubeLink,
            )
        }
    }
}