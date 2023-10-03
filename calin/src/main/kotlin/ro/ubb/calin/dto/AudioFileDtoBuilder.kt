package ro.ubb.calin.dto

import org.springframework.core.io.FileSystemResource
import org.springframework.util.LinkedMultiValueMap
import org.springframework.util.MultiValueMap
import java.nio.file.Path

class AudioFileDtoBuilder {
    private val count: Int
    private val multiMap: MultiValueMap<String, Any>

    constructor() {
        this.count = 1
        this.multiMap = LinkedMultiValueMap()
    }

    constructor(count: Int, multiValueMap: MultiValueMap<String, Any>) {
        this.count = count
        this.multiMap = multiValueMap
    }

    fun addAudioFile(path: String): AudioFileDtoBuilder {
        val resource = FileSystemResource(Path.of(path).toFile())

        val multiMapCopy = (multiMap as LinkedMultiValueMap).deepCopy()
        multiMapCopy.add("file$count", resource)
        multiMapCopy.add("path$count", path)
        return AudioFileDtoBuilder(count + 1, multiMapCopy)
    }

    fun build(): MultiValueMap<String, Any> {
        return multiMap
    }
}