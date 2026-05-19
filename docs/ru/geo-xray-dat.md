# Каталог геоданных Xray (`opt/etc/xray/dat`) и Mihomo

Источник на роутере (Entware / Keenetic): **`opt/etc/xray/dat`**. Каталог данных Mihomo обычно **`opt/etc/mihomo`** — см. [`mihomo/info.txt`](../../mihomo/info.txt).

Эти файлы в первую очередь для **Xray**. **Mihomo** использует те же protobuf-`.dat` для **GeoSite** и может использовать **GeoIP.dat** (или оставить **geoip.metadb** / `.mmdb` — см. ниже и [`mihomo/README-GEO.md`](../../mihomo/README-GEO.md)).

> В этом репозитории **нет** копии бинарных `*.dat` из роутера: они тяжёлые и относятся к Xray. Документ описывает **смысл файлов** и связку с **`mihomo/config.yaml`**. Скрипт разбора тегов: [`mihomo/list_geosite_tags.py`](../../mihomo/list_geosite_tags.py) — передайте путь к своему `.dat` аргументом.

## `geoip.metadb` (Mihomo) и каталог Xray `dat/` — это не одно целое

Проверка бинарника `mihomo/geoip.metadb`:

- Внутри есть служебная строка вида **`Meta-geoip`** — это **отдельная база GeoIP** в формате Meta (Mihomo / sing-geoip), **не** «архив» и не индекс к файлам из `xray/dat/`.
- По размеру и хэшу файл **не совпадает** с типичными `geoip_v2fly.dat` и `geoip_refilter.dat` из Xray — это **другой слепок** данных, который XKeen/Mihomo кладёт в **`opt/etc/mihomo`** отдельно от **`opt/etc/xray/dat`**.

Итого: **`geoip.metadb` не подключает и не объединяет автоматически** `geosite_v2fly.dat`, `geoip_refilter`, `zkeen.dat` и т.д. Это параллельные линии: **Xray** читает свой каталог `dat`, **Mihomo** — свой `GeoSite.dat` + выбранный источник GeoIP (`.metadb` / `.mmdb` / `GeoIP.dat` в зависимости от `geodata-mode`).

## XKeen и геобазы (контекст)

Скрипты **[XKeen](https://github.com/Corvus-Malus/XKeen)** на Keenetic отдельно обновляют ядра **Xray** и **Mihomo**, а также **геофайлы** (в т.ч. списки **Re:filter**, опционально **[zkeen.dat](https://github.com/jameszeroX/zkeen-domains)** / **[zkeenip.dat](https://github.com/jameszeroX/zkeen-ip)** в сторону Xray). Параметр **`-g`** в XKeen относится к переустановке геофайлов в логике установщика, а не к «сшивке» `metadb` с `dat` на диске.

Веб-интерфейс **[XKeen-UI](https://github.com/zxc-rv/XKeen-UI)** управляет настройками/сценарием XKeen, но **не превращает** `geoip.metadb` в контейнер для всех `.dat` из `xray/dat`.

## Типичный состав файлов в `xray/dat` (имена с роутера)

| Файл | Формат (проверено скриптом) | Назначение |
|------|------------------------------|------------|
| `geosite_v2fly.dat` | GeoSiteList, много тегов | Полный geosite (v2fly / community): `GEOSITE,google`, `GEOSITE,category-gov-ru`, … |
| `geosite_refilter.dat` | GeoSiteList, тег **`REFILTER`** | Доп. домены для «refilter» в связке с Xray; **один тег** — не заменяет полный geosite. |
| `geoip_v2fly.dat` | GeoSiteList wire (v2fly geoip в `.dat`) | IP-диапазоны по тегам для режима **GeoIP через .dat** в Mihomo при `geodata-mode: true`. |
| `geoip_refilter.dat` | теги **`PRIVATE`**, **`REFILTER`** | Доп. к geoip в Xray. |
| `zkeen.dat` | GeoSiteList, набор тегов вроде `BYPASS`, `CN`, `DOMAINS`, … | Локальный набор Keenetic/Zkeen для Xray. |
| `zkeenip.dat` | GeoSiteList, много тегов (`DISCORD`, `GOOGLE`, …) | IP-списки под CDN/сервисы в том же protobuf-виде. |

**Mihomo держит один активный `GeoSite.dat`** в каталоге данных ядра: нельзя одновременно «подмешать» v2fly и zkeen без **слияния файлов** офлайн. Обычно делают симлинк на **`geosite_v2fly.dat`**.

## Подключение к Mihomo на роутере (`opt/etc/mihomo`)

Имена файлов, которые ищет ядро (без учёта регистра): **`GeoSite.dat`**, для GeoIP — **`GeoIP.dat`** или fallback **`geoip.metadb`** / `Country.mmdb` (см. [GEO Databases в Mihomo](https://deepwiki.com/nendonerd/mihomo/6.2-geo-databases)).

### Вариант A — только обновить списки доменов (GeoIP как раньше `.metadb`)

Оставьте в **`mihomo/config.yaml`** (на устройстве — ваш `config.yaml` в каталоге `-d`) **`geodata-mode: false`** и положите рядом с конфигом Mihomo:

```sh
cd /opt/etc/mihomo
ln -sf /opt/etc/xray/dat/geosite_v2fly.dat GeoSite.dat
# geoip.metadb не трогаем
```

### Вариант B — и GeoIP брать из `.dat` (как в Xray)

В **`mihomo/config.yaml`** выставьте **`geodata-mode: true`**, уберите/не используйте `geoip.metadb` для GeoIP и создайте:

```sh
cd /opt/etc/mihomo
ln -sf /opt/etc/xray/dat/geosite_v2fly.dat GeoSite.dat
ln -sf /opt/etc/xray/dat/geoip_v2fly.dat GeoIP.dat
```

После смены режима перезапустите Mihomo и проверьте лог загрузки геоданных.

### Про `*_refilter.dat` и `zkeen*.dat`

- **refilter**: в Mihomo **нет** автослияния с основной базой, как может делать Xray. Либо объединяют списки внешним инструментом, либо оставляют refilter только на стороне Xray/nfqws.
- **zkeen / zkeenip**: если **заменить** `GeoSite.dat` симлинком на `zkeen.dat`, в правилах появятся только теги вроде `GEOSITE,YOUTUBE`, `GEOSITE,BYPASS` — полный v2fly-список пропадёт. Имеет смысл только осознанно.

## Скрипт просмотра тегов

В репозитории: **[`mihomo/list_geosite_tags.py`](../../mihomo/list_geosite_tags.py)**

```bash
cd /path/to/mihomo   # папка со скриптом в клоне репозитория или копия на ПК
python list_geosite_tags.py /opt/etc/xray/dat/geosite_v2fly.dat
python list_geosite_tags.py zkeen.dat
```

Без аргумента скрипт ищет рядом с собой первый из: `GeoSite.dat`, `geosite_v2fly.dat`, `zkeen.dat`, `zkeenip.dat`.

## Связь с публикуемым примером в репозитории

В **[`mihomo/config.yaml`](../../mihomo/config.yaml)** включены **`geo-auto-update`** и комментарии про геоданные. Подстройте **`geodata-mode`** под выбранный вариант A или B выше.
