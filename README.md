# yugen-site

Публичные страницы Yūgen для App Store Connect и приложения: поддержка, политика конфиденциальности, условия, источники (RU + EN).

- Тексты: `src/<en|ru>/<support|privacy|terms>.md`. Политика и условия — копии из `hello_world/docs/legal`; при изменении править там и копировать сюда.
- Раздел «Источники» живёт в `support.md` (должен совпадать с экраном «Источники и лицензии» в приложении и `docs/THIRD_PARTY_SOURCES.md`).
- Сборка: `python3 build.py` (HTML уже закоммичен, GitHub Pages отдаёт его как есть).
