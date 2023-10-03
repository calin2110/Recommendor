package ro.ubb.calin.domain

import jakarta.persistence.*
import org.hibernate.Hibernate

@Entity
@Table(name = "recommendations", schema = "migrations")
data class Recommendation(
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY) @Column(name = "id") val id: Long = -1,
    @Column(name = "recommendation_request_id") val recommendationRequestId: Long = -1,
    @ManyToOne @JoinColumn(name = "audio_file_id") val recommendedAudioFile: AudioFile = AudioFile()
) {
    override fun equals(other: Any?): Boolean {
        if (this === other) return true
        if (other == null || Hibernate.getClass(this) != Hibernate.getClass(other)) return false
        other as Recommendation

        return id == other.id
    }

    override fun hashCode(): Int = javaClass.hashCode()

    @Override
    override fun toString(): String {
        return this::class.simpleName + "(id = $id , recommendationRequestId = $recommendationRequestId , recommendedAudioFile = $recommendedAudioFile )"
    }
}