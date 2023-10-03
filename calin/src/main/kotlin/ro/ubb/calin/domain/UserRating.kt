package ro.ubb.calin.domain

import jakarta.persistence.*
import org.hibernate.Hibernate

@Entity
@Table(name = "user_ratings", schema = "migrations")
data class UserRating(
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY) @Column(name = "id") val id: Long = -1,
    @Column(name = "user_id") val userId: Long = -1,
    @Column(name = "subgenre1") val subgenre1: String = "",
    @Column(name = "subgenre2") val subgenre2: String = "",
    @Column(name = "rating") val rating: Int = 0
) {
    override fun equals(other: Any?): Boolean {
        if (this === other) return true
        if (other == null || Hibernate.getClass(this) != Hibernate.getClass(other)) return false
        other as UserRating

        return id == other.id
    }

    override fun hashCode(): Int = javaClass.hashCode()

    @Override
    override fun toString(): String {
        return this::class.simpleName + "(id = $id , userId = $userId , subgenre1 = $subgenre1 , subgenre2 = $subgenre2 , rating = $rating )"
    }
}