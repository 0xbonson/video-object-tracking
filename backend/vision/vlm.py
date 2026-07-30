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
        Mengirim crop ke Vision Language Model
        dan mengembalikan atribut visual dengan suhu (temperature) 0.0 agar presisi.
        """

        prompt = """
You are an expert visual analyst. Analyze the cropped image of the person provided.
Pay extremely close attention to their clothing, patterns (like batik), and physical appearance.

Extract the following attributes with high accuracy:
1. "gender": Must be either "male" or "female". Look closely at facial features, body shape, and hair.
2. "shirt_color": The dominant color of their top clothing (e.g., black, white, red, blue).
3. "shirt_type": The style of the top (e.g., t-shirt, blouse, jacket, shirt).
4. "pants_color": The dominant color of their bottom clothing.
5. "pants_type": The style of the bottom. If they are wearing a skirt, specifically mention "skirt" or "batik skirt" if patterned.
6. "confidence": "high", "medium", or "low".

You MUST return ONLY a valid JSON object. Do not include markdown formatting, explanations, or any other text.
Format strictly like this:
{
  "shirt_color": "black",
  "shirt_type": "blouse",
  "pants_color": "brown",
  "pants_type": "batik skirt",
  "gender": "female",
  "confidence": "high"
}
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
            options={
                "temperature": 0.0
            }
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

        text = text[start : end + 1]

        try:
            return json.loads(text)

        except json.JSONDecodeError as exc:
            raise RuntimeError(
                f"Gagal parsing JSON dari VLM.\n\n{text}"
            ) from exc


vlm = VisionLanguageModel()
