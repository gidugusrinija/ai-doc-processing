import json
from pathlib import Path


def load_few_shot_examples(dataset_dir: str) -> list[dict]:

    dataset_dir = Path(dataset_dir)

    examples = []

    example_dirs = sorted(
        [
            directory
            for directory in dataset_dir.iterdir()
            if directory.is_dir()
        ]
    )

    for example_dir in example_dirs:

        image_path = example_dir / "image.jpg"
        annotation_path = example_dir / "output.json"

        if not image_path.exists():
            image_path = example_dir / "image.png"
            if not image_path.exists():
                raise FileNotFoundError(
                    f"Image few shots missing: {image_path}"
                )

        if not annotation_path.exists():
            raise FileNotFoundError(
                f"Sample output json few shots missing: {annotation_path}"
            )

        with open(annotation_path, "r", encoding="utf-8") as file:
            annotation = json.load(file)

        examples.append({
            "example_id": example_dir.name,
            "image_path": str(image_path.resolve()),
            "annotation_path": str(annotation_path.resolve()),
            "annotation": annotation,
        })

    print(f"Loaded {len(examples)} few-shot examples.")

    return examples