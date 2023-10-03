package ro.ubb.calin.tcp.strategies

import java.io.InputStream
import java.io.OutputStream
import java.nio.ByteBuffer
import java.nio.ByteOrder

class IntegerCommunicationStrategy: CommunicationStrategy {
    override fun send(data: Any, outputStream: OutputStream) {
        outputStream.write(
            ByteBuffer.allocate(4)
                .order(ByteOrder.BIG_ENDIAN)
                .putInt(data as Int)
                .array()
        )
    }

    override fun receive(inputStream: InputStream): Any {
        val buffer = ByteArray(4)
        inputStream.read(buffer, 0, 4)
        return ByteBuffer.wrap(buffer).order(ByteOrder.BIG_ENDIAN).int
    }
}