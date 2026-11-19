import json
import numpy as np
import faiss

from pathlib import Path


class FAISSRetriever:

    def __init__(self, embeddings_dir: str):

        embeddings_dir = Path(embeddings_dir)

        self.embeddings = np.load(
            embeddings_dir / "hybrid_embeddings.npy"
        ).astype(np.float32)

        with open(
            embeddings_dir / "visual_metadata.json",
            "r",
            encoding="utf-8",
        ) as file:
            self.metadata = json.load(file)

        dimension = self.embeddings.shape[1]

        # Inner product index
        self.index = faiss.IndexFlatIP(dimension)

        self.index.add(self.embeddings)

        print(f"FAISS index created.")
        print(f"Number of vectors: {self.index.ntotal}")
        print(f"Embedding dimension: {dimension}")

    def retrieve(
        self,
        query_embedding: np.ndarray,
        top_k: int = 3,
    ):

        query_embedding = np.asarray(
            query_embedding,
            dtype=np.float32,
        )

        query_embedding = query_embedding.reshape(1, -1)

        scores, indices = self.index.search(
            query_embedding,
            top_k,
        )

        results = []

        for score, index in zip(
            scores[0],
            indices[0],
        ):

            if index == -1:
                continue

            result = {
                **self.metadata[index],
                "similarity_score": float(score),
            }

            results.append(result)

        return results