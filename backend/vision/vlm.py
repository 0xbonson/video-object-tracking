import json
from pathlib import Path

from ollama import Client


class VisionLanguageModel:
    """
    Wrapper untuk berkomunikasi dengan Ollama Vision.
    """

    def __init__(
        self,
        model: str = "qwen2.5vl:3b",
        host: str = "http://localhost:11434",
    ):
        self.client = Client(host=host)
        self.model = model

    def describe(self, image_path: str | Path) -> dict:
        """
        Mengirim gambar ke Vision Language Model
        dan mengembalikan hasil sebagai Python dict.
        """

        prompt = """
You are an AI vision system.

Analyze the uploaded image.

Return ONLY valid JSON.

Schema:

{
  "object": "",
  "shirt_color": "",
  "shirt_type": "",
  "pants_color": "",
  "pants_type": "",
  "gender": "",
  "confidence": "high | medium | low"
}

Rules:
- Do not explain.
- Do not use markdown.
- Do not wrap JSON with ```json.
- Return JSON only.
"""

        response = self.client.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                    "images": [str(image_path)],
                }
            ],
        )

        text = response["message"]["content"].strip()

        if text.startswith("```"):
            text = text.replace("```json", "")
            text = text.replace("```", "")
            text = text.strip()

        start = text.find("{")
        end = text.rfind("}")

        if start == -1 or end == -1:
            raise RuntimeError(
                f"VLM tidak mengembalikan JSON.\n\n{text}"
            )

        text = text[start:end + 1]

        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                f"Gagal parsing JSON dari VLM.\n\n{text}"
            ) from exc


vlm = VisionLanguageModel()