import argparse
import os
from dataclasses import dataclass

import pandas as pd
import psycopg2

FILE_TEMPLATE = 'out_genres.csv'
GENRES = ["blues", "classical", "country", "disco", "hip-hop", "jazz", "metal", "pop", "reggae", "rock"]


@dataclass
class AudioFile:
    genre: str
    subgenre: str
    path: str


@dataclass
class ConnectionDetails:
    host: str
    database: str
    username: str
    password: str
    schema: str


def get_connection_details() -> ConnectionDetails:
    parser = argparse.ArgumentParser(
        prog='MigrationCreator',
        description='Adds the audio files to the database'
    )
    parser.add_argument('--host', type=str, help='Host of the database', required=True)
    parser.add_argument('--database', type=str, help='The actual database', required=True)
    parser.add_argument('--username', type=str, help='Username of the user', required=True)
    parser.add_argument('--password', type=str, help='Password of the user', required=True)
    parser.add_argument('--schema', type=str, help='Schema to connect to')
    args = parser.parse_args()
    return ConnectionDetails(
        host=args.host,
        database=args.database,
        username=args.username,
        password=args.password,
        schema=args.schema
    )


def connect_to_database():
    details = get_connection_details()
    if details.schema is None:
        return psycopg2.connect(
            host=details.host,
            database=details.database,
            user=details.username,
            password=details.password
        )
    return psycopg2.connect(
        host=details.host,
        database=details.database,
        user=details.username,
        password=details.password,
        options=f'-c search_path={details.schema}'
    )


def search_for_subgenre(df, name: str):
    for _, row in df.iterrows():
        if row.get('filename') == name:
            return row.get('specific genre')
    raise Exception('File not found.')


def get_audio_file_objects(main_df, dfs) -> list[AudioFile]:
    audio_files = []
    for _, row in main_df.iterrows():
        filename = row.get('filename')
        general_genre = row.get('general genre')
        specific_genre = search_for_subgenre(dfs[general_genre], filename)
        path = os.path.abspath(os.path.join('..', 'data', filename))
        audio_files.append(AudioFile(path=path, genre=general_genre.upper(), subgenre=specific_genre))
    return audio_files


def insert_audio_files_to_db(connection, audio_files: list[AudioFile]):
    rows = [(file.path, file.genre, file.subgenre) for file in audio_files]
    cursor = connection.cursor()
    cursor.executemany(
        'INSERT INTO audio_files (path, genre, subgenre) VALUES (%s, %s, %s)', rows
    )
    connection.commit()
    cursor.close()


def execute_main():
    tags_path = os.path.join('..', 'tags')
    main_df = pd.read_csv(os.path.join(tags_path, FILE_TEMPLATE))
    dfs = {}
    for genre in GENRES:
        df = pd.read_csv(os.path.join(tags_path, f'{genre}_{FILE_TEMPLATE}'))
        dfs[genre] = df

    audio_files = get_audio_file_objects(main_df=main_df, dfs=dfs)

    connection = connect_to_database()
    insert_audio_files_to_db(connection, audio_files)
    connection.close()


if __name__ == "__main__":
    execute_main()
