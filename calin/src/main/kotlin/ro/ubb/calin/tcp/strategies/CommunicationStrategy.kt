package ro.ubb.calin.tcp.strategies

import java.io.InputStream
import java.io.OutputStream

interface CommunicationStrategy {
    fun send(data: Any, outputStream: OutputStream)
    fun receive(inputStream: InputStream): Any
}