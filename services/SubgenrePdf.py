class SubgenrePdf:
    def __init__(self, genre: str, pdf: dict[str, float]):
        self.__genre = genre
        self.__pdf = pdf

    def get_value(self, key):
        return self.__pdf[key]

    def get_keys(self):
        return self.__pdf.keys()

    def get_genre(self):
        return self.__genre

    def get_items(self):
        return self.__pdf.items()
