package ro.ubb.calin

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication

@SpringBootApplication
class CalinApplication

fun main(args: Array<String>) {
	runApplication<CalinApplication>(*args)
}
