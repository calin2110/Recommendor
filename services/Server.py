import os
import socket
import threading
from time import sleep

from DownloadException import DownloadException
from MusicRecommender import MusicRecommenderFacade
from SimilarityCalculator import SimilarityNormalCalculator
from SocketUtils import send_int, send_long, send_str, recv_str, recv_int


class Server:
    def __init__(self,
                 music_recommender: MusicRecommenderFacade,
                 similarity_calculator: SimilarityNormalCalculator
                 ):
        self.music_recommender = music_recommender
        self.similarity_calculator = similarity_calculator

        # for key in self.matrices:
        #     for pair in self.matrices[key]:
        #         print(f'{pair} {self.matrices[key][pair]}')

    def run(self):
        print('Breaking the habit tonight')
        thread = threading.Thread(target=self.__handle_listener)
        thread.start()

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('localhost', int(os.getenv('RECOMMENDER_SERVER_COMMUNICATION_PORT'))))
        sock.listen(5)

        while True:
            # for key in self.similarity_calculator.matrices:
            #     for pair in self.similarity_calculator.matrices[key]:
            #         print(f'{pair} {self.similarity_calculator.matrices[key][pair]}')
            # sleep(10)
            try:
                newsock = sock.accept()
                print('Received connection on running thread')
                thread = threading.Thread(target=self.__handle_connection, args=newsock)
                print('Starting new thread...')
                thread.start()
            except Exception as e:
                print(f'Socket exception happened: {e}')

    def __handle_listener(self):
        print('Listening for matrix changes...')
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('localhost', int(os.getenv('RECOMMENDER_EXTRACTOR_COMMUNICATION_PORT'))))
        sock.listen(1)
        while True:
            conn, addr = sock.accept()
            print('Achieved new connection')
            data = conn.recv(1)
            self.similarity_calculator.load()
            conn.close()

    def __handle_connection(self, sock, host):
        limit = recv_int(sock)
        top = recv_int(sock)
        yt_link = recv_str(sock)
        print(f'Handling connection, received limit {limit}, top {top}, yt_link {yt_link}')

        try:
            recommended_songs = self.music_recommender.recommend_songs(yt_link, limit, top)
            send_int(sock, 0)
            send_int(sock, len(recommended_songs))
            for item in recommended_songs:
                send_long(sock, item)
        except DownloadException as de:
            send_int(sock, -1)
            send_str(sock, str(de))
            return
