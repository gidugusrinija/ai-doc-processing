
import json
from pathlib import Path


def load_few_shot_examples(base_dir="data/few_shots"):

    base_dir = Path(base_dir)

    examples = []

    for example_dir in sorted(base_dir.iterdir()):

        if not example_dir.is_dir():
            continue

        image_path = example_dir / "image.png"
        json_path = example_dir / "output.json"

        if not image_path.exists() or not json_path.exists():
            print(f"Skipping incomplete example: {example_dir}")
            continue

        with open(json_path, "r", encoding="utf-8") as file:
            expected_output = json.load(file)

        examples.append({
            "id": example_dir.name,
            "image_path": str(image_path),
            "expected_output": expected_output
        })

    return examples


if __name__ == "__main__":

    examples = load_few_shot_examples()

    print(f"Loaded {len(examples)} few-shot examples")

    for example in examples:
        print(example["id"])
        print(example["image_path"])
        print(example["expected_output"])
