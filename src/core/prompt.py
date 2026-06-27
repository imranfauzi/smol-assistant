from pathlib import Path
from core.config import settings

prompts_dir = Path(settings.PROMPT_PATH).resolve()

def load_prompt(name: str) -> str:
    file_path = prompts_dir / f"{name}.md"
    
    if not file_path.exists():
        raise FileNotFoundError(f"Prompt file '{name}.md' not found: {file_path}")
        
    return file_path.read_text(encoding="utf-8").strip()
