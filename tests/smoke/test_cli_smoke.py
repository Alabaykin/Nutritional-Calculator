import subprocess
import sys
import os

def test_cli_smoke():
    cli_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "app", "cli", "main.py"))
    recipe_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "fixtures", "sample_recipe.json"))
    
    result = subprocess.run(
        [sys.executable, cli_path, recipe_path],
        capture_output=True
    )
    
    stdout = None
    stderr = None
    for encoding in ["utf-8", "cp1251", "cp866"]:
        try:
            stdout = result.stdout.decode(encoding)
            stderr = result.stderr.decode(encoding)
            break
        except UnicodeDecodeError:
            continue
            
    if stdout is None:
        stdout = result.stdout.decode("utf-8", errors="ignore")
        stderr = result.stderr.decode("utf-8", errors="ignore")
    
    assert result.returncode == 0, f"Error code {result.returncode}. Stderr: {stderr}. Stdout: {stdout}"
    
    assert "Рецепт: Куриная грудка с гречкой" in stdout
    assert "Сырой вес: 300" in stdout
    assert "Вес готового блюда: 240.0г" in stdout
    assert "Калории: 539.0 ккал" in stdout or "539.0" in stdout
    assert "Белки: 59.8 г" in stdout or "59.8" in stdout
    assert "Жиры: 7.1 г" in stdout or "7.1" in stdout
    assert "Углеводы: 62.9 г" in stdout or "62.9" in stdout
    assert "КБЖУ на 100г готового блюда" in stdout
