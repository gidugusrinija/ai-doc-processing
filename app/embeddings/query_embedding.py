import numpy as np
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class QueryEmbeddingGenerator:

    def __init__(
        self,
        model: str = "text-embedding-3-small",
    ):

        self.client = OpenAI()
        self.model = model

    def generate_embedding(self, text: str) -> np.ndarray:

        if not text.strip():
            raise ValueError(
                "Cannot generate embedding from empty text."
            )

        response = self.client.embeddings.create(
            model=self.model,
            input=text,
        )

        embedding = np.array(
            response.data[0].embedding,
            dtype=np.float32,
        )

        norm = np.linalg.norm(embedding)

        if norm > 0:
            embedding = embedding / norm

        return embedding