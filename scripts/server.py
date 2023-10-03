import os
import pickle
import socket
import threading
from time import sleep
from rating_extractor import CommutativePair

PORT = 4205

def load_similarity_matrices(genres):
    matrices = {}
    for genre in genres:
        with open(os.path.join('matrices', f'{genre}_matrix.fmm'), 'rb') as file:
            matrices[genre] = pickle.load(file)
    return matrices


class SimilarityMatrices:
    GENRES = ['BLUES', 'CLASSICAL', 'COUNTRY', 'DISCO', 'HIP_HOP', 'JAZZ', 'METAL', 'POP', 'REGGAE', 'ROCK']

    def __init__(self):
        self.matrices = {}
        self.reload()

    def reload(self):
        self.matrices = load_similarity_matrices(self.GENRES)


def thread_worker(matrices: SimilarityMatrices):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', PORT))
    sock.listen(1)
    while True:
        conn, addr = sock.accept()
        data = conn.recv(1)
        conn.close()
        matrices.reload()


def main():
    matrices = SimilarityMatrices()
    thread = threading.Thread(target=thread_worker, args=(matrices, ))
    thread.start()

    for i in range(1000):
        for key in matrices.matrices:
            for pair in matrices.matrices[key]:
                print(f'{pair} {matrices.matrices[key][pair]}')
        sleep(1)
    # do server stuff
    thread.join()


if __name__ == "__main__":
    main()