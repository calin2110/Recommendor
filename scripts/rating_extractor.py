import argparse
import os.path
import pickle
import socket
import warnings
from dataclasses import dataclass

import numpy as np
import pandas as pd
import requests

from shared.CommutativePair import CommutativePair

SUCCESS_CODE = 200


@dataclass
class ConnectionDetails:
    link: str
    email: str
    password: str
    file: str
    stds: float
    port: int
    min_count: int


def get_connection_details() -> ConnectionDetails:
    parser = argparse.ArgumentParser(
        prog='RatingExtractor',
        description='Extracts all ratings given'
    )
    parser.add_argument('--link', type=str, help='Link to which we make the request', required=True)
    parser.add_argument('--email', type=str, help='Email of the admin user', required=True)
    parser.add_argument('--password', type=str, help='Password of the admin user', required=True)
    parser.add_argument('--genres_file', type=str, help='Files with the genre', required=True)
    parser.add_argument('--stds', type=float, help='How many stds away we go', required=True)
    parser.add_argument('--port', type=int, help='What port will connect to the server?', required=True)
    parser.add_argument('--min_count', type=int, help='Minimum count of ratings for a genre', required=True)
    args = parser.parse_args()
    return ConnectionDetails(
        link=args.link,
        email=args.email,
        password=args.password,
        file=args.genres_file,
        stds=args.stds,
        port=args.port,
        min_count=args.min_count
    )


@dataclass
class Rating:
    genre: str
    subgenre1: str
    subgenre2: str
    rating: int
    user: int


@dataclass
class NormalizedRating:
    genre: str
    subgenre1: str
    subgenre2: str
    rating: float


def authenticate(details: ConnectionDetails) -> str:
    data = {'email': details.email, 'password': details.password}
    req = requests.post(f"{details.link}/api/auth/authenticate", json=data, verify=False)
    if req.status_code != SUCCESS_CODE:
        raise Exception('Invalid request for authentication, please try again')
    token = req.json()['token']
    return token


def extract_ratings(details: ConnectionDetails):
    token = authenticate(details)
    headers = {'Authorization': f'Bearer {token}'}
    req = requests.get(f"{details.link}/api/admin/ratings", headers=headers, verify=False)
    if req.status_code != SUCCESS_CODE:
        raise Exception('Invalid request for getting ratings, please try again')
    ratings_json = req.json()
    ratings = []
    for rating in ratings_json:
        ratings.append(Rating(genre=rating['genre'],
                              subgenre1=rating['subgenre1'],
                              subgenre2=rating['subgenre2'],
                              rating=rating['rating'],
                              user=rating['user']))
    return ratings


def group_ratings_by_user(ratings: list[Rating]) -> dict[int, list[Rating]]:
    grouped_ratings = {}
    for rating in ratings:
        if rating.user not in grouped_ratings:
            grouped_ratings[rating.user] = []
        grouped_ratings[rating.user].append(rating)
    return grouped_ratings


def normalize_ratings(grouped_ratings: dict[int, list[Rating]], min_count: int) -> list[NormalizedRating]:
    normalized_ratings = []
    for user, user_ratings in grouped_ratings.items():
        ratings = [rating.rating for rating in user_ratings]

        if len(ratings) < min_count or np.std(ratings) == 0:
            continue
        # if data is already normal
        mean = np.mean(ratings)
        std_dev = np.std(ratings)
        normalized_values = [(value - mean) / std_dev for value in ratings]

        for i, rating in enumerate(user_ratings):
            normalized_rating = NormalizedRating(
                genre=rating.genre,
                subgenre1=rating.subgenre1,
                subgenre2=rating.subgenre2,
                rating=normalized_values[i]
            )
            normalized_ratings.append(normalized_rating)
    return normalized_ratings


def read_subgenres(csv_file) -> dict[str, set[str]]:
    df = pd.read_csv(csv_file)
    rows = df.shape[0]
    subgenres = {}
    for i in range(rows):
        genre = df.iloc[i]['general genre'].upper().replace('-', '_')
        subgenre = df.iloc[i]['specific genre']
        if genre not in subgenres:
            subgenres[genre] = set()
        subgenres[genre].add(subgenre)
    return subgenres


def create_similarity_matrix(subgenres: set[str]) -> dict[CommutativePair, float]:
    matrix = {}
    for subgenre1 in subgenres:
        for subgenre2 in subgenres:
            if subgenre1 <= subgenre2:
                matrix[CommutativePair(subgenre1, subgenre2)] = None
    return matrix


def create_similarity_matrices(subgenres: dict[str, set[str]]) -> dict[str, dict[CommutativePair, float]]:
    matrices = {}
    for genre in subgenres:
        matrices[genre] = create_similarity_matrix(subgenres[genre])
    return matrices


def compute_similarity_indexes(
        matrices: dict[str, dict[CommutativePair, float]],
        subgenres: dict[str, set[str]],
        normalized_ratings: list[NormalizedRating],
        stds: float
):
    grouped_ratings = {}
    for key in subgenres:
        grouped_ratings[key] = {}
        for subgenre1 in subgenres[key]:
            for subgenre2 in subgenres[key]:
                if subgenre1 <= subgenre2:
                    grouped_ratings[key][CommutativePair(subgenre1, subgenre2)] = []

    for rating in normalized_ratings:
        grouped_ratings[rating.genre][CommutativePair(rating.subgenre1, rating.subgenre2)].append(rating.rating)

    for key in matrices:
        for pair in matrices[key]:
            if pair.item1 != pair.item2:
                matrices[key][pair] = -stds if len(grouped_ratings[key][pair]) == 0 else np.mean(
                    grouped_ratings[key][pair])
            else:
                matrices[key][pair] = stds


def save_similarity_matrix(genre: str, similarity_matrix: dict[CommutativePair, float]):
    with open(
            os.path.join('..',
                         os.path.join('services',
                                      os.path.join('matrices', f'{genre}_matrix.fmm')
                                      )), 'wb'
    ) as file:
        pickle.dump(similarity_matrix, file)


def extract():
    details = get_connection_details()
    ratings = extract_ratings(details=details)
    grouped_ratings = group_ratings_by_user(ratings=ratings)
    normalized_ratings = normalize_ratings(grouped_ratings=grouped_ratings, min_count=details.min_count)
    subgenres = read_subgenres(details.file)
    matrices = create_similarity_matrices(subgenres)
    compute_similarity_indexes(matrices, subgenres, normalized_ratings, details.stds)
    for genre in matrices:
        save_similarity_matrix(genre, matrices[genre])
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', details.port))
    sock.send(b'0')
    sock.close()


if __name__ == "__main__":
    extract()
