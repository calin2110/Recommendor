package ro.ubb.calin.tcp

import ro.ubb.calin.tcp.strategies.CommunicationStrategy
import ro.ubb.calin.tcp.strategies.CommunicationStrategyFactory
import java.net.Socket

class TCPSocket(host: String, port: Int) : AutoCloseable {
    private val socket: Socket
    private var communicationStrategy: CommunicationStrategy? = null

    init {
        socket = Socket(host, port)
    }

    fun prepareForCommunication(type: Type): TCPSocket {
        communicationStrategy = CommunicationStrategyFactory.getCommunicationStrategy(type)
        return this
    }

    fun send(value: Any): TCPSocket {
        communicationStrategy!!.send(value, socket.outputStream)
        return this
    }


    fun receive(): Any {
        return communicationStrategy!!.receive(socket.inputStream)
    }

    override fun close() {
        socket.close()
    }

    enum class Type {
        INT,
        STRING,
        LONG
    }
}