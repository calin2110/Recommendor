import random

import psycopg2


class AudioFilesDao:
    def __init__(self):
        self.connection = psycopg2.connect(
            host='localhost',
            database='Recommendor',
            user='postgres',
            password='postgres',
            options=f'-c search_path=migrations'
        )

    def __get_audio_files_of_subgenre(self, genre, subgenre):
        cursor = self.connection.cursor()
        my_condition = "genre = %s AND subgenre = %s"
        params = (genre, subgenre, )
        statement = f'SELECT id FROM migrations.audio_files WHERE {my_condition}'
        cursor.execute(statement, params)
        results = cursor.fetchall()
        return [result[0] for result in results]

    def get_random_file_of_subgenre(self, genre, subgenre):
        files = self.__get_audio_files_of_subgenre(genre, subgenre)
        return random.choice(files)

    def __del__(self):
        self.connection.close()


