import numpy as np
import joblib

from sklearn.random_projection import GaussianRandomProjection


class EmbeddingReducer:

    def __init__(self, target_dimension: int = 512):

        self.target_dimension = target_dimension

        self.visual_reducer = GaussianRandomProjection(
            n_components=target_dimension,
            random_state=42,
        )

        self.semantic_reducer = GaussianRandomProjection(
            n_components=target_dimension,
            random_state=42,
        )

    def fit_transform(self, visual_embeddings, semantic_embeddings):

        visual_reduced = self.visual_reducer.fit_transform(
            visual_embeddings
        )

        semantic_reduced = self.semantic_reducer.fit_transform(
            semantic_embeddings
        )

        visual_reduced = self._normalize(visual_reduced)
        semantic_reduced = self._normalize(semantic_reduced)

        hybrid_embeddings = np.concatenate(
            [visual_reduced, semantic_reduced],
            axis=1,
        )

        hybrid_embeddings = self._normalize(hybrid_embeddings)

        return visual_reduced, semantic_reduced, hybrid_embeddings

    def transform(self, visual_embeddings, semantic_embeddings):

        visual_reduced = self.visual_reducer.transform(
            visual_embeddings
        )

        semantic_reduced = self.semantic_reducer.transform(
            semantic_embeddings
        )

        visual_reduced = self._normalize(visual_reduced)
        semantic_reduced = self._normalize(semantic_reduced)

        hybrid_embeddings = np.concatenate(
            [visual_reduced, semantic_reduced],
            axis=1,
        )

        hybrid_embeddings = self._normalize(hybrid_embeddings)

        return visual_reduced, semantic_reduced, hybrid_embeddings

    def save(self, path: str):

        joblib.dump(self, path)

    @staticmethod
    def load(path: str):

        return joblib.load(path)

    @staticmethod
    def _normalize(embeddings):

        norms = np.linalg.norm(
            embeddings,
            axis=1,
            keepdims=True,
        )

        norms[norms == 0] = 1

        return embeddings / norms