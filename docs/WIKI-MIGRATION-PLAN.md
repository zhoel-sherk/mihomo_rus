# План миграции GUIDE.md в GitHub Wiki

## Что такое GitHub Wiki

GitHub Wiki — это отдельный git-репозиторий (`<repo>.wiki.git`), где каждый `.md` файл — отдельная страница. Плюсы:

- Страницы открываются мгновенно без скролла 1300+ строк
- Боковая панель (`_Sidebar.md`) — навигация по всем разделам
- Каждая страница может быть найдена через поиск GitHub
- Править можно как через веб-интерфейс, так и клонировав wiki-репозиторий

## Предлагаемая структура страниц

Все файлы — в корне wiki-репозитория (GitHub Wiki не поддерживает подпапки).

| Файл | Содержание | Источник из GUIDE.md |
|------|-----------|---------------------|
| `Home.md` | Введение, с чего начать, ссылки на внешние источники, быстрый старт | Строки 1–45 (шапка, быстрый старт) |
| `General.md` | Глобальная конфигурация (LAN, режимы, keep-alive, REST API, Geo) | § 1 |
| `Proxy-Ports.md` | Порты (HTTP, SOCKS, mixed, tproxy, redir) | § 2 |
| `TUN.md` | Виртуальный интерфейс TUN (stack, маршрутизация, фильтры) | § 3 |
| `DNS.md` | DNS Hosts + блок `dns:` + DNS schemes + fallback-filter | § 4, 5, 6 |
| `Sniffer.md` | Domain Sniffing (протоколы, исключения) | § 7 |
| `Listeners.md` | Inbounds (listeners, локальные и серверные типы) | § 8 |
| `Proxies-Common.md` | Общие поля исходящих узлов (tls, mux, brutal) | § 9 |
| `Proxy-Groups.md` | Группы (select, url-test, fallback, health-check, фильтры) | § 10 |
| `VLESS.md` | Протокол VLESS (XTLS Vision, REALITY, encryption) | § 11 |
| `Rules.md` | Правила (domain, IP, source, ports, логические, rule-set) | § 12 |
| `Rule-Providers.md` | Провайдеры правил (форматы classical/domain/ipcidr) | § 10 (вложенный) |
| `Proxy-Providers.md` | Провайдеры прокси (http/file/inline, override, filter) | § 13 |
| `Sub-Rules.md` | Подправила (вызов из rules, привязка к listener) | § 14 |
| `Tunnels.md` | Прямые туннели (однострочный/многострочный формат) | § 15 |
| `nfqws2.md` | Совместная работа с nfqws2 на Keenetic | § 16 |
| `NTP.md` | Синхронизация времени | § 17 |
| `Experimental.md` | Экспериментальные опции (QUIC-GSO, ECN, IP4P) | § 18 |

## Служебные файлы Wiki

### `_Sidebar.md` — боковая панель навигации

```markdown
## Mihomo Guide (RU)

- [Home](Home)
- [General](General)
- [Proxy Ports](Proxy-Ports)
- [TUN](TUN)
- [DNS](DNS)
- [Sniffer](Sniffer)
- [Listeners](Listeners)
- [Proxies (Common Fields)](Proxies-Common)
- [VLESS](VLESS)
- [Proxy Groups](Proxy-Groups)
- [Rules](Rules)
- [Rule Providers](Rule-Providers)
- [Proxy Providers](Proxy-Providers)
- [Sub-Rules](Sub-Rules)
- [Tunnels](Tunnels)
- [nfqws2](nfqws2)
- [NTP](NTP)
- [Experimental](Experimental)
```

### `_Footer.md` — подвал (одинаков для всех страниц)

```markdown
---

[Наверх](#) · [Репозиторий](https://github.com/ваш-аккаунт/mihomo-guide) · [Официальная вики Mihomo](https://wiki.metacubex.one/en/config/)
```

## Пошаговый процесс миграции

### Шаг 1. Создать пустой wiki

В интерфейсе репозитория на GitHub перейти в **Wiki → Create the first page**. GitHub создаст `HOME.md` и клонируемый репозиторий `mihomo-guide.wiki.git`.

### Шаг 2. Склонировать wiki-репозиторий локально

```bash
git clone git@github.com:ваш-аккаунт/mihomo-guide.wiki.git
```

### Шаг 3. Создать страницы-заглушки

Скопировать каждый раздел из `GUIDE.md` в соответствующий файл из таблицы выше.  
**Важно:** GitHub Wiki нумерует страницы лексикографически в веб-интерфейсе — для управления порядком можно использовать префиксы `01-General.md`, `02-Proxy-Ports.md` и т.д. Но для навигации через `_Sidebar.md` порядок не важен.

### Шаг 4. Переписать внутренние ссылки

Замена по всему тексту:

| Было (GUIDE.md) | Стало (Wiki) |
|---|---|
| `#sec-general` | `General` |
| `#sec-tun` | `TUN` |
| `[docs/ru/proxies.md](docs/ru/proxies.md)` | `[Proxies (Common Fields)](Proxies-Common)` |
| `[mihomo/config.yaml](mihomo/config.yaml)` | Внешняя ссылка на `https://github.com/.../blob/main/mihomo/config.yaml` |

Внутренние перекрёстные ссылки между разделами GUIDE.md (например, `см. [§ Совместная работа с nfqws2](#sec-nfqws)`) превратить в `см. [nfqws2](nfqws2)`.

### Шаг 5. Создать `_Sidebar.md` и `_Footer.md`

Скопировать содержимое из шаблонов выше, подставив свой аккаунт.

### Шаг 6. Залить и проверить

```bash
git add .
git commit -m "Initial wiki: migrate GUIDE.md to multi-page wiki"
git push
```

Открыть в браузере `https://github.com/ваш-аккаунт/mihomo-guide/wiki` и проверить:

- Боковая панель отображается
- Ссылки между страницами работают
- YAML-блоки корректно подсвечиваются

## Что изменится в GUIDE.md после миграции

После переноса содержимого в Wiki GUIDE.md можно превратить в индекс:

```markdown
# Mihomo Guide (RU)

Основное руководство перенесено в **[GitHub Wiki](https://github.com/ваш-аккаунт/mihomo-guide/wiki)**.

- [General](https://github.com/ваш-аккаунт/mihomo-guide/wiki/General)
- [TUN](https://github.com/ваш-аккаунт/mihomo-guide/wiki/TUN)
- [DNS](https://github.com/ваш-аккаунт/mihomo-guide/wiki/DNS)
- ... и т.д.

В репозитории остаются вспомогательные файлы: `mihomo/config.yaml`, `mihomo/examples/`, `docs/`.
```

Это делает GUIDE.md краткой входной точкой, а всю детальную документацию — в Wiki.

## Примечания

- **Anchor-ссылки** (`<a id="sec-...">`) в Wiki не нужны — каждая страница — это отдельный раздел, достаточно заголовков.
- **Оглавление** в `Home.md` можно сделать через `_Sidebar.md`, а не в самом тексте.
- **Таблица соответствия** из `docs/REFERENCE-META-DOCS.md` (GUIDE.md разделы ↔ папки Meta-Docs) — разместить в `Home.md` или отдельной страницей `Meta-Docs-Reference.md`.
- **Примеры конфигов** (`mihomo/examples/`) — ссылаться на них из Wiki через прямые GitHub-ссылки на файлы в `main`-ветке.
- При каждом обновлении GUIDE.md нужно синхронизировать соответствующую wiki-страницу — автоматизировать это можно через GitHub Actions (см. [github-wiki-sync](https://github.com/marketplace/actions/github-wiki-sync) или action [Decathlon/wiki-page-creator-action](https://github.com/marketplace/actions/github-wiki-action)).
