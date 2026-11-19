import json
import numpy as np
from openai import OpenAI


class SemanticEmbeddingGenerator:

    def __init__(self, model: str = "text-embedding-3-small"):
        self.client = OpenAI()
        self.model = model

    def generate_embedding(self, annotation: dict) -> np.ndarray:

        text = json.dumps(
            annotation,
            ensure_ascii=False,
            indent=2,
        )

        response = self.client.embeddings.create(
            model=self.model,
            input=text,
        )

        embedding = np.array(
            response.data[0].embedding,
            dtype=np.float32,
        )

        # L2 normalization
        norm = np.linalg.norm(embedding)

        if norm > 0:
            embedding = embedding / norm

        return embedding