import numpy as np
import onnxruntime as ort

from PIL import Image
from transformers import AutoImageProcessor


class VisualEmbeddingGenerator:

    def __init__(self, model_path: str):

        self.session = ort.InferenceSession(
            model_path,
            providers=["CPUExecutionProvider"],
        )

        self.image_processor = AutoImageProcessor.from_pretrained(
            "google/vit-base-patch16-224"
        )

        self.input_name = self.session.get_inputs()[0].name

    def generate_embedding(self, image_path: str) -> np.ndarray:

        image = Image.open(image_path).convert("RGB")

        inputs = self.image_processor(
            images=image,
            return_tensors="np",
        )

        pixel_values = inputs["pixel_values"]

        outputs = self.session.run(
            None,
            {
                self.input_name: pixel_values,
            },
        )

        embedding = outputs[0][0]

        # L2 normalization
        norm = np.linalg.norm(embedding)

        if norm > 0:
            embedding = embedding / norm

        return embedding.astype(np.float32)