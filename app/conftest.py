"""Добавляет корень приложения (app/) в sys.path, чтобы импорты
`core.analyzers.*`, `config`, `models.*` работали при запуске pytest."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
