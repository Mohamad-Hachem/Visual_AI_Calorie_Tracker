# Visual AI Calorie Tracker

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.55-FF4B4B?logo=streamlit&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-412991?logo=openai&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

A web application that estimates the nutritional content of any food from a single photo. Upload or drag-and-drop an image and receive an instant breakdown of calories, fat, and protein — powered by OpenAI's GPT-4o vision model.

---

## Demo

![App Screenshot](application_screenshots/Screenshot%202026-03-25%20104602.png)

> Pepperoni pizza detected: **298 kcal · 12 g fat · 13 g protein** with High confidence.

---

## Features

- **Drag-and-drop image upload** — no file path typing required
- **Instant nutritional analysis** — calories, fat, protein, and serving size
- **Confidence scoring** — High / Medium / Low indicator per result
- **Supports multiple formats** — JPEG, PNG, WebP, BMP
- **Zero database** — fully stateless; each request is independent

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Streamlit Frontend                      │
│                                                             │
│   [ Drag & Drop Uploader ]  →  [ Image Preview ]           │
│           │                                                 │
│           ▼                                                 │
│   ┌───────────────────┐                                     │
│   │  image_preparation│  encode_image_to_base64()           │
│   │  .py              │  (file path  OR  PIL Image)         │
│   └────────┬──────────┘                                     │
│            │  base64 string                                  │
│            ▼                                                 │
│   ┌───────────────────┐     ┌──────────────────────────┐   │
│   │  query_openai_    │────▶│  OpenAI GPT-4o Vision API │   │
│   │  vision_functions │     │  (chat.completions.create)│   │
│   │  .py              │◀────│                           │   │
│   └────────┬──────────┘     └──────────────────────────┘   │
│            │  raw JSON string                               │
│            ▼                                                 │
│   ┌───────────────────┐                                     │
│   │  prompt.py        │  DEFAULT_PROMPT enforces strict     │
│   │  (system prompt)  │  JSON-only response schema          │
│   └────────┬──────────┘                                     │
│            │                                                 │
│            ▼                                                 │
│   [ Metrics Display ]  Calories · Fat · Protein · Confidence│
└─────────────────────────────────────────────────────────────┘
```

### Data flow

1. User uploads an image via the Streamlit UI
2. `image_preparation.py` converts it to a base64-encoded string
3. `query_openai_vision_functions.py` packages the base64 image + system prompt into an OpenAI chat message and calls the API
4. GPT-4o returns a strict JSON object (enforced by `prompt.py`)
5. The app parses the JSON and renders the nutritional metrics

### Response schema

```json
{
  "food_name":           "string",
  "serving_description": "string",
  "calories":            "float | null",
  "fat_grams":           "float | null",
  "protein_grams":       "float | null",
  "confidence_level":    "High | Medium | Low | null"
}
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| UI | [Streamlit](https://streamlit.io) |
| Vision AI | [OpenAI GPT-4o](https://platform.openai.com/docs/models/gpt-4o) |
| Image processing | [Pillow](https://python-pillow.org/) |
| Environment config | [python-dotenv](https://pypi.org/project/python-dotenv/) |
| Runtime | Python 3.11 |

---

## Prerequisites

- Python 3.11+
- An [OpenAI API key](https://platform.openai.com/api-keys) with access to `gpt-4o`

---

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/Mohamad-Hachem/Visual_AI_Calorie_Tracker.git
cd Visual_AI_Calorie_Tracker

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/Scripts/activate      # Windows (bash)
# source .venv/bin/activate         # macOS / Linux

# 3. Install dependencies
pip install openai pillow python-dotenv streamlit
```

---

## Configuration

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=sk-...your-key-here...
```

> `.env` is listed in `.gitignore` and will never be committed.

---

## Usage

```bash
streamlit run main.py
```

Then open `http://localhost:8501` in your browser.

1. Drag and drop (or browse for) a food image
2. Wait ~2–4 seconds for the model to respond
3. View the nutritional breakdown and confidence score

---

## Project Structure

```
Visual_AI_Calorie_Tracker/
├── main.py                         # Streamlit app entry point
├── image_preparation.py            # Base64 encoding utility
├── query_openai_vision_functions.py # OpenAI API wrapper
├── prompt.py                       # System prompt / response schema
├── .env                            # API key (not committed)
├── application_screenshots/        # UI screenshots
└── .venv/                          # Virtual environment (not committed)
```

---

## Pros & Cons

### Pros

| | |
|---|---|
| **Zero setup friction** | No database, no backend server, no authentication required |
| **Model flexibility** | Model name is a parameter — swap to `gpt-4o-mini` to cut costs |
| **Dual input support** | Accepts both file paths and PIL Image objects for easy testing |
| **Strict output contract** | Prompt enforces JSON-only responses, making parsing reliable |
| **Portable** | Runs entirely from a single virtualenv; no Docker or cloud infra needed |

### Cons / Limitations

| | |
|---|---|
| **Estimation only** | Calorie figures are model estimates, not lab-measured values — accuracy varies |
| **No portion awareness** | The model cannot infer actual portion weight from an image alone |
| **Single-item focus** | Mixed plates or multi-item meals may reduce accuracy |
| **API cost** | Every upload triggers a GPT-4o call; high-volume usage accumulates cost |
| **No history** | Results are not persisted; refreshing the page loses previous analyses |
| **JPEG assumption** | Images are encoded with a hardcoded `image/jpeg` MIME type regardless of original format |

---

## Roadmap

- [ ] Carbohydrate tracking field
- [ ] Multi-item meal detection (multiple bounding boxes)
- [ ] Session history with a results table
- [ ] Export results to CSV
- [ ] `gpt-4o-mini` toggle for cost-conscious usage
- [ ] Docker image for one-command deployment

---

## License

This project is licensed under the [MIT License](LICENSE).
