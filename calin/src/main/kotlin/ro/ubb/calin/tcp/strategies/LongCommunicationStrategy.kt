package ro.ubb.calin.tcp.strategies

import java.io.InputStream
import java.io.OutputStream
import java.nio.ByteBuffer
import java.nio.ByteOrder

class LongCommunicationStrategy: CommunicationStrategy {
    override fun send(data: Any, outputStream: OutputStream) {
        outputStream.write(
            ByteBuffer.allocate(8)
                .order(ByteOrder.BIG_ENDIAN)
                .putLong(data as Long)
                .array()
        )
    }

    override fun receive(inputStream: InputStream): Any {
        val buffer = ByteArray(8)
        inputStream.read(buffer, 0, 8)
        return ByteBuffer.wrap(buffer).order(ByteOrder.BIG_ENDIAN).long
    }
}