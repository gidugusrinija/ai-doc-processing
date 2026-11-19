from pathlib import Path

import torch
from transformers import AutoModel


MODEL_NAME = "google/vit-base-patch16-224"

OUTPUT_DIR = Path("models/onnx")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_PATH = OUTPUT_DIR / "vit_base_patch16.onnx"


class ViTEmbeddingModel(torch.nn.Module):

    def __init__(self):
        super().__init__()
        self.model = AutoModel.from_pretrained(MODEL_NAME)

    def forward(self, pixel_values):
        outputs = self.model(pixel_values=pixel_values)

        # CLS token embedding
        return outputs.last_hidden_state[:, 0, :]


model = ViTEmbeddingModel()
model.eval()

dummy_input = torch.randn(1, 3, 224, 224)

torch.onnx.export(
    model,
    dummy_input,
    str(OUTPUT_PATH),
    input_names=["pixel_values"],
    output_names=["embeddings"],
    dynamic_axes={
        "pixel_values": {0: "batch_size"},
        "embeddings": {0: "batch_size"},
    },
    opset_version=17,
    dynamo=False,
)

print(f"ONNX model exported to: {OUTPUT_PATH}")