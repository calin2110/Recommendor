package ro.ubb.calin.domain

import jakarta.persistence.*
import org.hibernate.Hibernate

@Entity
@Table(name = "recommendation_requests", schema = "migrations")
data class RecommendationRequest(
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY) @Column(name = "id") val id: Long = -1,
    @Column(name = "user_id") val userId: Long = -1,
    @Column(name = "youtube_link") val youtubeLink: String = ""
) {
    override fun equals(other: Any?): Boolean {
        if (this === other) return true
        if (other == null || Hibernate.getClass(this) != Hibernate.getClass(other)) return false
        other as RecommendationRequest

        return id == other.id
    }

    override fun hashCode(): Int = javaClass.hashCode()

    @Override
    override fun toString(): String {
        return this::class.simpleName + "(id = $id , userId = $userId , youtubeLink = $youtubeLink )"
    }
}