package ro.ubb.calin.tcp.strategies

import ro.ubb.calin.tcp.TCPSocket
import java.io.InputStream
import java.io.OutputStream
import java.nio.charset.StandardCharsets

class StringCommunicationStrategy: CommunicationStrategy {
    private val integerCommunicationStrategy = IntegerCommunicationStrategy()

    override fun send(data: Any, outputStream: OutputStream) {
        val value = data as String
        integerCommunicationStrategy.send(value.length, outputStream)
        outputStream.write(value.toByteArray(StandardCharsets.UTF_8))
    }

    override fun receive(inputStream: InputStream): Any {
        val length = integerCommunicationStrategy.receive(inputStream) as Int
        val buffer = ByteArray(length)
        inputStream.read(buffer, 0, length)
        return String(buffer, StandardCharsets.UTF_8)
    }
}