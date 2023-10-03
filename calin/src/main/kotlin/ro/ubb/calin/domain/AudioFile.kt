package ro.ubb.calin.domain

import jakarta.persistence.*
import org.hibernate.Hibernate

@Entity
@Table(name = "audio_files", schema = "migrations")
data class AudioFile(
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY) @Column(name = "id")  val id: Long = -1,
    @Column(name = "path") val path: String = "",
    @Column(name = "genre") @Enumerated(value = EnumType.STRING) val genre: Genre = Genre.POP,
    @Column(name = "subgenre") val subgenre: String = ""
) {
    override fun equals(other: Any?): Boolean {
        if (this === other) return true
        if (other == null || Hibernate.getClass(this) != Hibernate.getClass(other)) return false
        other as AudioFile

        return id == other.id
    }

    override fun hashCode(): Int = javaClass.hashCode()

    @Override
    override fun toString(): String {
        return this::class.simpleName + "(id = $id , path = $path , genre = $genre , subgenre = $subgenre )"
    }
}
