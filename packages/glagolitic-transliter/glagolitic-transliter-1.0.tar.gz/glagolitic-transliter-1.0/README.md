# Glagolitic Transliter
Простой транслитератор кириллицы в глаголицу.
Предоставляет класс [GlagoliticTransliter](https://github.com/IlhomBahoraliev/gltransliter/blob/f8cf7870ac159f42b6ee021260cf1e73a8158f72/gltransliter/transliter.py#L26) c одним методом [translit](https://github.com/IlhomBahoraliev/gltransliter/blob/f8cf7870ac159f42b6ee021260cf1e73a8158f72/gltransliter/transliter.py#L68), что принимает аргументом текст и возвращает его транслитерированную версию.

## Usage case
```python
from gltransliter import GlagoliticTransliter

print(
  GlagoliticTransliter.translit("Мал золотник, да дорог")
) # Ⰿⰰⰾ ⰸⱁⰾⱁⱅⱀⰺⰽ, ⰴⰰ ⰴⱁⱃⱁⰳ
```

## Installing
```bash
pip install glagolitic-transliter
```
