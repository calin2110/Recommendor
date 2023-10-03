package ro.ubb.calin.tcp.strategies

import ro.ubb.calin.tcp.TCPSocket

class CommunicationStrategyFactory {
    companion object {
        fun getCommunicationStrategy(type: TCPSocket.Type): CommunicationStrategy {
            return when (type) {
                TCPSocket.Type.INT -> IntegerCommunicationStrategy()
                TCPSocket.Type.LONG -> LongCommunicationStrategy()
                TCPSocket.Type.STRING -> StringCommunicationStrategy()
            }
        }
    }
}