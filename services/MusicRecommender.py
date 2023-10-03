from AudioDownloader import AudioDownloader
from AudioFilesDao import AudioFilesDao
from MusicClassifier import MusicClassifier
from SimilarityCalculator import SimilarityNormalCalculator
from SimilarityFilter import SimilarityFilter

GENRES = ['BLUES', 'CLASSICAL', 'COUNTRY', 'DISCO', 'HIP_HOP', 'JAZZ', 'METAL', 'POP', 'REGGAE', 'ROCK']


class MusicRecommenderFacade:
    def __init__(self):
        pass

    def recommend_songs(self, youtube_link: str, limit: int, top: int) -> list[str]:
        pass


class MusicRecommender(MusicRecommenderFacade):
    def __init__(self,
                 audio_downloader: AudioDownloader,
                 music_classifier: MusicClassifier,
                 similarity_calculator: SimilarityNormalCalculator,
                 similarity_filter: SimilarityFilter,
                 audio_files_dao: AudioFilesDao):
        super().__init__()
        self.audio_downloader = audio_downloader
        self.music_classifier = music_classifier
        self.similarity_calculator = similarity_calculator
        self.similarity_filter = similarity_filter
        self.audio_files_dao = audio_files_dao

    def recommend_songs(self, youtube_link: str, limit: int, top: int) -> list[str]:
        downloaded_link = self.audio_downloader.download(youtube_link)
        pdf = self.music_classifier.get_pdf(limit, downloaded_link)
        similarity = self.similarity_calculator.calculate_similarity(pdf)
        top_similarities = self.similarity_filter.filter(similarity, top)
        files = []
        for item in top_similarities:
            files.append(self.audio_files_dao.get_random_file_of_subgenre(genre=pdf.get_genre(), subgenre=item[0]))
        self.audio_downloader.delete(downloaded_link)
        return files
