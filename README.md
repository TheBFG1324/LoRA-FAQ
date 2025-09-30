# LoRA-FAQ Hamilton

LoRA-FAQ Hamilton is a lightweight project that fine-tunes GPT-2 with LoRA on the **Alexander Hamilton** Wikipedia page.  
The model is then exposed as an **MCP server tool**, so you can query it from any MCP-compatible client and get Hamilton quotes on demand.

---

## Features
- Fine-tunes GPT-2 with **LoRA** using Keras/TensorFlow.  
- Uses text extracted from the *Alexander Hamilton* Wikipedia page.  
- Exposes an **MCP tool** called `answer_faq(question)` that returns a related Hamilton quote.  
- Includes a **FastAPI service** for local testing.  

---

## Project Structure
```
lora_faq_hamilton/
  data/               # Wikipedia source and processed quotes dataset
  lora_train/         # Training scripts
  serve/              # FastAPI inference service
  mcp_server/         # MCP server exposing the answer_faq tool
  LICENSES/           # Wikipedia CC BY-SA 4.0 license
  README.md
```

---

## Setup

```bash
git clone https://github.com/yourname/lora_faq_hamilton.git
cd lora_faq_hamilton
python -m venv .venv && source .venv/bin/activate

# Install dependencies
pip install "tensorflow==2.16.*" "tensorflow-text==2.16.*" \
            "keras>=3.3,<3.6" "keras-hub[nlp]>=0.16" \
            fastapi uvicorn "pydantic<3" httpx mcp
```

For Apple Silicon (M1/M2/M3):
```bash
pip install tensorflow-macos tensorflow-metal "tensorflow-text==2.16.*"
```

---

## Training

1. Download and clean the Hamilton Wikipedia page:
```bash
python lora_train/build_dataset.py
```

2. Fine-tune GPT-2 with LoRA:
```bash
python lora_train/train_lora_gpt2.py
```

Artifacts will be saved to `artifacts/lora_gpt2_savedmodel/`.

---

## Running the FastAPI Service

```bash
uvicorn serve.app:app --reload --port 8008
```

Test with curl:
```bash
curl -X POST localhost:8008/answer \
     -H 'content-type: application/json' \
     -d '{"question":"national bank"}'
```

---

## Running the MCP Server

```bash
python mcp_server/server.py
```

This exposes a tool:
- `answer_faq(question: str) -> str`

Configure your MCP-compatible client (e.g., Claude Desktop, Cursor) to connect to this server.

---

## Example Usage

**Input:**  
```
Give me a quote about George Washington
```

**Output:**  
```
"Hamilton served as George Washington's aide-de-camp..." — (Alexander Hamilton, Wikipedia)
Source: Wikipedia “Alexander Hamilton” (CC BY-SA 4.0).
```

---

## License & Attribution

- This project includes text from the [Alexander Hamilton Wikipedia article](https://en.wikipedia.org/wiki/Alexander_Hamilton).  
- Content is licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).  
- A copy of the license is included in `LICENSES/WIKIPEDIA_CC_BY_SA_4.0.txt`.  

---

 
