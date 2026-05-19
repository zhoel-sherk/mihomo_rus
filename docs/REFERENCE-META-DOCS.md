# Локальный референс Meta-Docs

В репозитории [MetaCubeX/Meta-Docs](https://github.com/MetaCubeX/Meta-Docs) лежат исходники сайта [wiki.metacubex.one](https://wiki.metacubex.one) (MkDocs). Это **каноничное описание полей** конфигурации Mihomo на **английском** и **китайском**; файлы `*.ru.md` там часто машинные и неполные.

## Зачем клонировать у себя

- Сверять формулировки при написании русских гайдов в этом репозитории (например [`ru/proxies.md`](ru/proxies.md)).
- Не тащить весь MkDocs и субмодули в **git**: каталог **`Meta-Docs/`** добавлен в [`.gitignore`](../.gitignore).

## Команда

Из корня **mihomo+guide** (рядом с `GUIDE.md`):

```bash
git clone https://github.com/MetaCubeX/Meta-Docs.git Meta-Docs
```

Дальше смотрите, например:

- `Meta-Docs/docs/config/proxies/` — исходящие узлы;
- `Meta-Docs/docs/config/general.md` и смежные файлы — глобальные опции (в т.ч. `external-controller`, DNS).

Если **`Meta-Docs/` уже попал в историю git**, удалите его из индекса отдельным коммитом: `git rm -r --cached Meta-Docs` (сами файлы на диске можно оставить).

---

## Соответствие `Meta-Docs/docs/config/` и [GUIDE.md](../GUIDE.md)

В вики каталог **`inbound/`** описывает входящие узлы; в YAML Mihomo это ключ **`listeners:`** (плюс отдельный файл **`ss-config`** там же, где это поддерживает сборка).

| Папка / корневые файлы в `Meta-Docs/docs/config/` | Где раскрыто в mihomo+guide |
| --- | --- |
| `general.*` | [§ Глобальная конфигурация](../GUIDE.md#sec-general) |
| Порты (`mixed-port`, `socks-port`, …) в `general` | [§ Порты](../GUIDE.md#sec-ports) |
| `dns/` (в т.ч. `hosts.md`) | [§ DNS hosts](../GUIDE.md#sec-dns-hosts), [§ dns:](../GUIDE.md#sec-dns-main), [§ схемы DNS](../GUIDE.md#sec-dns-schemes) |
| `sniff/` | [§ Sniffer](../GUIDE.md#sec-sniffer) |
| `inbound/` (HTTP/SOCKS/Mixed и т.д.; в вики рядом лежит `tun.md`) | Входящие: [§ listeners:](../GUIDE.md#sec-listeners), [поля](../GUIDE.md#sec-listeners-fields), [ss-config / tuic-server](../GUIDE.md#sec-listeners-alt). Корневой блок **`tun:`** в YAML — не путать с listener: [§ TUN](../GUIDE.md#sec-tun) |
| `proxies/` | [§ Общие поля proxies](../GUIDE.md#sec-proxies-common) + [**docs/ru/proxies.md**](ru/proxies.md) |
| `proxy-groups/` | [§ proxy-groups](../GUIDE.md#sec-proxy-groups) |
| `rules/`, `rule-providers/` | [§ rules и rule-set](../GUIDE.md#sec-rules) (включая подраздел про форматы rule-providers) |
| `proxy-providers/` | [§ proxy-providers](../GUIDE.md#sec-proxy-providers) |
| `sub-rule.md` | [§ sub-rules](../GUIDE.md#sec-sub-rules) |
| `tunnels.md` | [§ tunnels](../GUIDE.md#sec-tunnels) |
| `ntp/` | [§ ntp](../GUIDE.md#sec-ntp) |
| `experimental.*` | [§ experimental](../GUIDE.md#sec-experimental) |
| Полный пример в индексе вики (ссылка на репозиторий ядра) | Публикуемый скелет: [**mihomo/config.yaml**](../mihomo/config.yaml) |

**Keenetic / nfqws:** в Meta-Docs отдельного раздела нет — у нас [§ nfqws2](../GUIDE.md#sec-nfqws).

---

## Папки Meta-Docs **вне** `config/` (не дублируем целиком в GUIDE)

| Каталог | Содержание | Как связано с гайдом |
| --- | --- | --- |
| `docs/api/` | REST API (`/configs`, `/proxies`, WebSocket логов и т.д.) | В GUIDE — поля `external-controller`, `secret`, `external-ui` ([§ general](../GUIDE.md#sec-general)); детали панелей и запросов — [**docs/ru/web-ui.md**](ru/web-ui.md); полный перечень эндпоинтов — только в Meta-Docs / [wiki API](https://wiki.metacubex.one/en/api/). |
| `docs/handbook/` | Синтаксис правил, маршрутизация, DNS/вывод — справочный слой | Пересекается с [§ rules](../GUIDE.md#sec-rules) и DNS; GUIDE даёт практичный срез под роутер, не копирует всю «книгу». |
| `docs/startup/` | Установка, сервис, клиенты, FAQ | Про установку Mihomo на ПК/сервер; наш фокус — **config.yaml** на роутере (XKeen и т.п.). |
| `docs/example/` | Примеры конфигов с сайта | Дублируют идею полного `config.yaml`; опора — **mihomo/config.yaml** + GUIDE. |

Итого: **ни один раздел `config/` не «выпал»** — он либо есть в оглавлении GUIDE, либо вынесен в `docs/ru/proxies.md`. То, что **намеренно не полный справочник**: полный REST API, startup/handbook и машинные `*.ru.md` в апстриме (см. абзац выше про EN/ZH).
