# Локальные базы Mihomo и внешние источники (Geo / списки)

Полный разбор Xray `opt/etc/xray/dat` vs Mihomo: [**`docs/ru/geo-xray-dat.md`**](../docs/ru/geo-xray-dat.md). Маршрутизация и DNS в конфиге: **`../GUIDE.md`**.

### Снимки в репозитории и «живые» геоданные

Файлы **`GeoSite.dat`**, **`geoip.metadb`** (и при наличии другие) в папке **`mihomo/`** в git — **пример формата и снимок для гайда** (разбор тегов, скрипт `list_geosite_tags.py`). Их версия **может отставать** от того, что вы реально положите на роутер.

**Откуда брать актуальные базы**

1. Релиз **[MetaCubeX/meta-rules-dat — `latest`](https://github.com/MetaCubeX/meta-rules-dat/releases/tag/latest)** — скачать `geosite.dat`, `geoip.metadb` (и при необходимости `geoip.dat`, ASN и т.д.) в каталог данных Mihomo (`-d`, на Entware часто `opt/etc/mihomo`).
2. Либо в конфиге включить **`geo-auto-update: true`** и при необходимости задать **`geox-url`** — ядро само будет подтягивать файлы по URL (см. пример в **`config.yaml`** в этой папке и [вики — general](https://wiki.metacubex.one/ru/config/general/)).

Публикуемый пример конфига: **`mihomo/config.yaml`**. Для новичков — пошаговый разбор сценариев и терминов: **`mihomo/examples/README.md`**, рядом — файлы **`scenario-*.yaml`**.

---

## Файлы в этой папке (`mihomo/`)

| Файл | Назначение |
|------|------------|
| `config.yaml` | Публикуемый пример конфигурации Mihomo (в репозитории под этим именем; на роутере кладут в каталог `-d` как `config.yaml`). |
| `examples/` | Учебные **сценарии** (отдельные YAML + развёрнутые комментарии): DNS, TUN, подписки, sub-rules, listeners — начните с **`examples/README.md`**. |
| `GeoSite.dat` | Списки доменов по тегам для правил `GEOSITE,...` и для `geosite:` в DNS/sniffer (protobuf v2ray). **Файл в этом репозитории** — снимок для примера; для боя подставьте актуальный с `latest` или через `geo-auto-update`. |
| `geoip.metadb` | База **GeoIP** (формат **Meta**). **Не** «сборка» всех `xray/dat/*.dat` — см. [**`docs/ru/geo-xray-dat.md`**](../docs/ru/geo-xray-dat.md). Копия в git — для примера; актуальная — с [meta-rules-dat `latest`](https://github.com/MetaCubeX/meta-rules-dat/releases/tag/latest) или автообновление. |
| `cache.db` | Служебный кэш ядра (не для ручного правки). |

Каталог на роутере (Entware): см. `info.txt` — обычно `opt/etc/mihomo`.

---

## [MetaCubeX/meta-rules-dat](https://github.com/MetaCubeX/meta-rules-dat) и ветка `meta`

- Репозиторий собирает **актуальные геобазы и списки** для экосистемы Meta (в т.ч. Mihomo). Ветка **`meta`** в описании помечена как *rules-dat for mihomo* — это линия сборок под ядро, не отдельный «другой Mihomo».
- Готовые бинарники выкладываются в релиз с тегом **`latest`** (часто обновляется):  
  [releases/tag/latest](https://github.com/MetaCubeX/meta-rules-dat/releases/tag/latest).

### Связь с `geoip.metadb` и правилами `GEOIP` / `GEOSITE`

| Ассет в `latest` (примеры) | Зачем Mihomo |
|---------------------------|--------------|
| **`geoip.metadb`** | Основной **GeoIP** в нативном формате Meta; при `geodata-mode: false` ядро ориентируется на **metadb / mmdb**, а не на `GeoIP.dat`. |
| **`geoip.dat`** | Классический GeoIP в формате v2ray; нужен при **`geodata-mode: true`** (и имя на диске обычно `GeoIP.dat`). |
| **`geosite.dat`** | Списки доменов по тегам → правила **`GEOSITE`**, **`geosite:`** в DNS/sniffer. |
| `geoip-lite.*` / `geosite-lite.*` | Облегчённые варианты (меньше размер, другой набор данных — смотрите размеры в релизе). |
| `country.mmdb`, `country-lite.mmdb` | MMDB стран (часть сценариев/совместимости; в дефолтах ядра поле **`mmdb`** в `geox-url` может указывать на **`geoip.metadb`** с этого же релиза). |
| `GeoLite2-ASN.mmdb` | ASN для правил/логики, завязанной на автономные системы. |

**Практика:** либо кладёте нужные файлы в каталог `-d` Mihomo вручную / скриптом роутера (XKeen и т.п.), либо включаете **`geo-auto-update: true`** и при необходимости переопределяете URL в **`geox-url`** (см. [Общие настройки — geodata-mode, geo-auto-update, geox-url](https://wiki.metacubex.one/ru/config/general/)).

Прямые ссылки на те же файлы с GitHub (удобно для `wget` на роутере):

- `https://github.com/MetaCubeX/meta-rules-dat/releases/download/latest/geoip.metadb`
- `https://github.com/MetaCubeX/meta-rules-dat/releases/download/latest/geosite.dat`
- `https://github.com/MetaCubeX/meta-rules-dat/releases/download/latest/geoip.dat`

В **дефолтной** конфигурации ядра `geox-url` уже завязан на этот репозиторий и тег `latest` (поля `geoip` / `geosite` / `mmdb` / `asn` — см. вики). Если вы **вручную** копируете базы и не хотите, чтобы старт ядра их перезаписал, выставьте **`geo-auto-update: false`** (по необходимости поменяйте в своём **`config.yaml`** относительно примера **`mihomo/config.yaml`**).

---

## [antifilter.download](https://antifilter.download/) — подключение списков в Mihomo

Сервис публикует **текстовые списки** (IP, подсети, домены, URL). Для Mihomo их обычно подключают через **`rule-providers`** и правила **`RULE-SET`**, а не через `GeoSite.dat`.

Официально на сайте указаны, в частности:

| URL | Содержимое (по описанию сайта) |
|-----|--------------------------------|
| `https://antifilter.download/list/allyouneed.lst` | Сводный **IP/CIDR** (ipsum + subnet). |
| `https://antifilter.download/list/ipsum.lst` | Суммаризация отдельных адресов по /24. |
| `https://antifilter.download/list/subnet.lst` | Подсети. |
| `https://antifilter.download/list/ip.lst` | Много отдельных IP (объём большой — на слабом роутере может быть тяжело). |
| `https://antifilter.download/list/domains.lst` | Домены. |
| `https://antifilter.download/list/urls.lst` | URL (для «голого» rule-provider без доработки часто неудобны — проще домены/IP). |

**Пример `rule-providers` + правило** (IP из `allyouneed.lst` — по одному префиксу на строку → `behavior: ipcidr`, `format: text`):

```yaml
rule-providers:
  antifilter-ip:
    type: http
    behavior: ipcidr
    format: text
    url: "https://antifilter.download/list/allyouneed.lst"
    path: ./ruleset/antifilter-ip.txt
    interval: 3600

rules:
  - RULE-SET,antifilter-ip,PROXY
```

**Домены** (`domains.lst`, одна строка — один домен / суффикс по смыслу списка):

```yaml
rule-providers:
  antifilter-domains:
    type: http
    behavior: domain
    format: text
    url: "https://antifilter.download/list/domains.lst"
    path: ./ruleset/antifilter-domains.txt
    interval: 3600

rules:
  - RULE-SET,antifilter-domains,PROXY
```

Подставьте вместо `PROXY` имя вашей **`proxy-groups`** (см. **`../GUIDE.md`** → [Группы `proxy-groups:`](../GUIDE.md#sec-proxy-groups)). Порядок правил важен: сначала исключения (LAN, свой прокси-домен), потом `RULE-SET`, потом `MATCH`.

**Замечания по эксплуатации**

- **`interval`** — в секундах; на сайте указано, что проверка обновлений списков делается часто, но вашему ядру достаточно разумного интервала (например 1–6 ч), чтобы не долбить CDN.
- Списки **большие**; на роутере следите за RAM и временем первой загрузки.
- Смысл правила (`PROXY` / `DIRECT` / `REJECT`) — **ваш выбор политики**; документ описывает только техническую связку. Источник и юридический контекст изложены на самом [antifilter.download](https://antifilter.download/).

---

## Как прочитать `GeoSite.dat`

1. Скрипт **`list_geosite_tags.py`** в этой папке выводит теги, реально присутствующие в файле.
2. Перед использованием тега вроде `geosite:ru` в sniffer/DNS убедитесь, что тег **есть** в вашем `.dat` (часто для РФ используют `category-ru` и т.д.).

---

## Как смотреть `geoip.metadb`

Как текст не открывается. Проверка — через работу правил `GEOIP` и логи Mihomo либо утилиты из документации к вашей версии ядра.
