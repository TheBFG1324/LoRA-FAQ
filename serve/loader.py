import os
import keras

os.environ["KERAS_BACKEND"] = "tensorflow"

_MODEL = None

def get_model():
    global _MODEL
    if _MODEL is None:
        _MODEL = keras.models.load_model("artifacts/lora_gpt2.keras")
    return _MODEL

def answer(question: str, max_len: int = 160):
    m = get_model()
    prompt = f"User: Give a quote about {question}.\nAssistant: "
    out = m.generate(
        prompt,
        max_length=max_len,
        strip_prompt=True
    )
    return f'{out}\n\nSource: Wikipedia “Alexander Hamilton” (CC BY-SA 4.0).'

if __name__ == "__main__":
    print(answer("Alexander, Hamilton, Abolition"))
