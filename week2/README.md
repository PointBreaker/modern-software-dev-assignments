# Action Item Extractor

A FastAPI-based web application that extracts actionable items from text using both rule-based patterns and LLM-powered analysis.

## Features

- 🚀 **Dual Extraction Methods**: Choose between fast rule-based extraction or intelligent LLM-powered analysis
- 💾 **Note Management**: Save extracted text as notes for future reference
- ✅ **Action Item Tracking**: Mark action items as complete/incomplete
- 📝 **Note History**: View all saved notes with timestamps
- 🎯 **Simple Interface**: Clean, minimal HTML frontend
- 🔧 **Configurable**: Environment-based configuration

## Quick Start

### Prerequisites

- Python 3.10 or higher
- [Ollama](https://ollama.ai/) installed and running (for LLM extraction)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd week2
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r pyproject.toml
```

4. Set up environment variables (optional):
```bash
cp .env.example .env
# Edit .env with your preferences
```

### Running the Application

Start the FastAPI server:

```bash
python -m uvicorn src.app.main:app --reload
```

The application will be available at `http://localhost:8000`

## Usage

### Web Interface

1. **Extract Action Items**:
   - Paste your notes or text in the textarea
   - Choose whether to save as a note
   - Click either:
     - **Extract (Rules)** - Fast extraction using patterns
     - **Extract (LLM)** - Smart extraction using AI (requires Ollama)
   - View extracted items below
   - Check/uncheck items to mark them as complete

2. **View Notes**:
   - Click **List Notes** to see all saved notes
   - Notes display with ID, creation time, and content

### API Endpoints

#### Action Items

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/action-items/extract` | Extract items using rules |
| POST | `/action-items/extract-llm` | Extract items using LLM |
| GET | `/action-items` | List all action items |
| POST | `/action-items/{id}/done` | Mark item as done/undone |
| DELETE | `/action-items/{id}` | Delete an action item |

#### Notes

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/notes` | Create a new note |
| GET | `/notes` | List all notes |
| GET | `/notes/{id}` | Get a specific note |

#### System

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Main web interface |
| GET | `/health` | Health check endpoint |

### API Examples

#### Extract with Rules

```bash
curl -X POST http://localhost:8000/action-items/extract \
  -H "Content-Type: application/json" \
  -d '{
    "text": "- [ ] Review documentation\n- Deploy to production",
    "save_note": true
  }'
```

#### Extract with LLM

```bash
curl -X POST http://localhost:8000/action-items/extract-llm \
  -H "Content-Type: application/json" \
  -d '{
    "text": "We need to complete the code review and update the documentation",
    "save_note": false
  }'
```

#### List Notes

```bash
curl http://localhost:8000/notes
```

## Configuration

Environment variables (create `.env` file):

```bash
# Debug mode
DEBUG=false

# Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL=INFO

# LLM Configuration (optional)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
```

## Rule-Based Extraction Patterns

The application recognizes the following patterns:

- **Bullet points**: `- item`, `* item`, `1. item`
- **Keywords**: `todo:`, `action:`, `next:`
- **Checkboxes**: `[ ]`, `[todo]`
- **Imperative sentences**: Commands starting with verbs like "add", "create", "fix"

## LLM Extraction

When using LLM extraction:
- Make sure Ollama is running locally on port 11434
- The first request might take longer as the model loads
- LLM provides more nuanced understanding of context

## Testing

Run the test suite:

```bash
python -m pytest src/tests/
```

Run tests for extraction specifically:

```bash
python -m pytest src/tests/test_extract.py -v
```

## Project Structure

```
src/
├── app/
│   ├── main.py           # FastAPI application
│   ├── db.py            # Database operations
│   ├── routers/         # API routes
│   │   ├── action_items.py
│   │   └── notes.py
│   └── services/        # Business logic
│       └── extract.py   # Extraction services
├── frontend/
│   └── index.html       # Web interface
└── tests/
    └── test_extract.py   # Unit tests
```

## Architecture

- **FastAPI**: Web framework for API endpoints
- **SQLite**: Database for storing notes and action items
- **Ollama**: Local LLM provider for AI-powered extraction
- **HTML/CSS/JavaScript**: Simple frontend interface

## Development

### Adding New Extraction Patterns

Edit `src/app/services/extract.py` to add new patterns to the extraction logic.

### Database Schema

The application uses two tables:
- `notes`: Stores text notes
- `action_items`: Stores extracted actionable items linked to notes

## Troubleshooting

### LLM Extraction Not Working
- Ensure Ollama is running: `ollama serve`
- Verify the model is available: `ollama list`
- Check the model is pulled: `ollama pull llama3.1:8b`

### Frontend Not Loading
- Check the server is running on the correct port
- Verify the frontend directory exists

### Database Errors
- The SQLite database is automatically created in the `data/` directory
- Delete `data/app.db` to reset the database

## License

This project is part of the Modern Software Development assignments.