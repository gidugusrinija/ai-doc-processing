import json

from app.retrieval.faiss_retriever import FAISSRetriever


class FewShotRetrieval:

    def __init__(self, embeddings_dir: str):
        self.retriever = FAISSRetriever(embeddings_dir)

    def retrieve_examples(self, query_embedding, top_k=3):

        results = self.retriever.retrieve(
            query_embedding=query_embedding,
            top_k=top_k,
        )

        examples = []

        for result in results:

            with open(result["annotation_path"], "r", encoding="utf-8") as file:
                annotation = json.load(file)

            examples.append({
                "example_id": result["example_id"],
                "similarity_score": result["similarity_score"],
                "image_path": result["image_path"],
                "annotation": annotation,
            })

        return examples