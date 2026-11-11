#!/usr/bin/env python3
"""Create a PUBLIC GitHub repository for the included project, after confirmation."""
import os, re, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)
FILES = ["3004-mini.yaml", "README.md", "secrets.example.yaml", ".gitignore", "upload.py"]

def run(*args, check=True):
    print("+", " ".join(args), flush=True)
    return subprocess.run(args, check=check)

def main():
    for exe in ("git", "gh"):
        if not shutil.which(exe):
            sys.exit(f"Не найдена команда {exe}. Установите Git и GitHub CLI; см. README.md.")
    if run("gh", "auth", "status", check=False).returncode != 0:
        sys.exit("Сначала войдите в GitHub: gh auth login")
    if (ROOT / ".git").exists():
        sys.exit("В каталоге уже есть .git. Скрипт ничего не меняет. См. README.md, раздел о повторном запуске.")
    for key in ("user.name", "user.email"):
        if subprocess.run(["git", "config", "--get", key], capture_output=True).returncode:
            sys.exit(f"Не настроен git {key}. См. README.md; можно указать GitHub noreply email.")
    name = input("Имя нового репозитория [esp32-3004-mini]: ").strip() or "esp32-3004-mini"
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", name) or name in (".", ".."):
        sys.exit("Недопустимое имя репозитория.")
    print("\nБудет создан ПУБЛИЧНЫЙ репозиторий GitHub. Все включённые файлы и Git-автор будут видны всем.")
    print("Файлы:", ", ".join(FILES))
    print("Пароли и BLE-адрес в подготовленные файлы не включены. Проверьте файлы самостоятельно.")
    if input('Чтобы продолжить, введите PUBLIC: ').strip() != 'PUBLIC':
        sys.exit("Отменено. Репозиторий не создан.")
    try:
        run("git", "init", "-b", "main")
        run("git", "add", "--", *FILES)
        run("git", "commit", "-m", "Initial ESPHome diffuser configuration")
        run("gh", "repo", "create", name, "--public", "--source", ".", "--remote", "origin", "--push")
        print("\nГотово. Ссылка на репозиторий показана выше.")
    except subprocess.CalledProcessError as e:
        sys.exit(f"Ошибка команды (код {e.returncode}). Возможны локальный репозиторий или частично созданный GitHub-репозиторий; проверьте перед повтором, см. README.md.")

if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        sys.exit("\nОперация прервана. Проверьте GitHub и локальный каталог перед повтором.")
