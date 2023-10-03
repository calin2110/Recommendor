class SimilarityFilter:
    def __init__(self):
        pass

    def filter(self, similarity: dict[str, float], top: int):
        sorted_vector = sorted(similarity.items(), key=lambda x: x[1], reverse=True)

        max_size = len(sorted_vector) if top > len(sorted_vector) else top
        max_size = max(0, max_size)
        return sorted_vector[:max_size]
