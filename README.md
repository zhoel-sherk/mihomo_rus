# mihomo_rus

Документация и практические гайды по **[Mihomo](https://github.com/MetaCubeX/mihomo)** (Clash Meta) **на русском языке** — и смежные темы: DNS, fake-ip, sniffer, правила, геоданные, связка с **nfqws2** / **XKeen** на роутерах вроде Keenetic.

Это **неофициальное** собрание: перекрёстно сверяйтесь с [вики Mihomo](https://wiki.metacubex.one/ru/config/) (по факту страницы **на английском и китайском**, полноценного русского нет — как раз поэтому здесь свой гайд) и с релизами вашего ядра.

---

## Содержимое репозитория

| Файл / папка | Описание |
|--------------|----------|
| [**GUIDE.md**](GUIDE.md) | Основное руководство по `config.yaml`: `general`, DNS, sniffer, `proxies`, `rules`, rule-providers, nfqws2, типичные ошибки (`GEOIP` vs сервисы, `fake-ip-filter` и др.). |
| [**docs/README.md**](docs/README.md) | Оглавление разделов в **`docs/`** (русские справочники). |
| [**docs/ru/proxies.md**](docs/ru/proxies.md) | Единый справочник по исходящим **`proxies:`** (общие поля, TLS, транспорты, все типы узлов). |
| [**docs/ru/web-ui.md**](docs/ru/web-ui.md) | Веб-интерфейсы к Mihomo и **XKeen-UI** для XKeen. |
| [**docs/REFERENCE-META-DOCS.md**](docs/REFERENCE-META-DOCS.md) | Как клонировать [Meta-Docs](https://github.com/MetaCubeX/Meta-Docs) локально; папка **`Meta-Docs/`** в **`.gitignore`** (не коммитить). |
| [**mihomo/README-GEO.md**](mihomo/README-GEO.md) | Локальные `GeoSite.dat` / `geoip.metadb`, [meta-rules-dat](https://github.com/MetaCubeX/meta-rules-dat), релиз [`latest`](https://github.com/MetaCubeX/meta-rules-dat/releases/tag/latest), подключение [antifilter.download](https://antifilter.download/) через `rule-providers`. |
| [**docs/ru/geo-xray-dat.md**](docs/ru/geo-xray-dat.md) | Каталог **`opt/etc/xray/dat`**, симлинки `GeoSite.dat` / `GeoIP.dat` в Mihomo, `geodata-mode`, отличие `geoip.metadb` от набора Xray. |
| [**docs/ru/interop-xkeen-nfqws-mihomo.md**](docs/ru/interop-xkeen-nfqws-mihomo.md) | **XKeen + XKeen-UI + nfqws2-keenetic + Mihomo:** netfilter, DNS, геоданные, типичные конфликты. |
| [**mihomo/config.yaml**](mihomo/config.yaml) | Пример конфига **без личных узлов** (на роутере копируют как `config.yaml` в каталог `-d` Mihomo); в комментариях ссылки на гайд. |
| [**mihomo/examples/**](mihomo/examples/) | Учебные **фрагменты** `config.yaml` по сценариям (DNS, TUN, подписки, sub-rules, listeners) с пояснениями для начинающих — см. **`examples/README.md`**. |
| [**mihomo/**](mihomo/) | Пример `config.yaml`, снимки геоданных для гайда (`GeoSite.dat`, `geoip.metadb` — **не** обязательно актуальные; см. README-GEO), `list_geosite_tags.py`, `info.txt` (пути Entware). **Не путать** с локальным клоном Meta-Docs — см. **`docs/REFERENCE-META-DOCS.md`**. |

---

## С чего начать

1. Прочитать [**GUIDE.md**](GUIDE.md) по оглавлению — от `mode` и портов до `dns:` и `rules:`.
2. Детально по типам исходящих узлов — [**docs/ru/proxies.md**](docs/ru/proxies.md); панели в браузере — [**docs/ru/web-ui.md**](docs/ru/web-ui.md).
3. Если на роутере отдельно стоят Xray и Mihomo — [**docs/ru/geo-xray-dat.md**](docs/ru/geo-xray-dat.md) и [**mihomo/README-GEO.md**](mihomo/README-GEO.md).
4. Взять за основу [**mihomo/config.yaml**](mihomo/config.yaml) или заглянуть в [**mihomo/examples/**](mihomo/examples/) для отдельных сценариев; подставить свой прокси и группы; обновить геоданные с [meta-rules-dat `latest`](https://github.com/MetaCubeX/meta-rules-dat/releases/tag/latest) или включить `geo-auto-update` в конфиге.

---

## Полезные внешние ссылки

- [Mihomo — репозиторий](https://github.com/MetaCubeX/mihomo)
- [Вики: конфигурация](https://wiki.metacubex.one/ru/config/) — официальный источник; разделы в основном **EN/ZH**, русская локаль в URL не означает полный перевод
- [meta-rules-dat — геобазы под экосистему Meta](https://github.com/MetaCubeX/meta-rules-dat) · [релиз `latest`](https://github.com/MetaCubeX/meta-rules-dat/releases/tag/latest)

---

## Лицензия и вклад

Материалы распространяются «как есть», без гарантий. Если репозиторий приватный — приглашайте соавторов через GitHub; для публичного форка достаточно сохранить указание источника и не публиковать чужие секреты из конфигов.

Предложения по правкам — через issues / pull requests в вашем процессе работы с репозиторием **mihomo_rus**.
---

## Происхождение текста и оговорки

### Как писался гайд

Значительная часть текста подготовлена с помощью **нейросетей** и затем вычитана вручную: такой объём за короткий срок «в соло» иначе собрать сложно. **Полный аудит** ещё впереди — пока публикуем **как есть**. Официальная вики MetaCubeX по языкам (в основном EN/ZH) и по объёму читается тяжело; при появлении времени разумно вынести из этого репозитория структурированный материал и в сторону их документации.

### Юридическая оговорка

- **Законодательство и договор с провайдером.** Вы сами отвечаете за законность своих действий в стране пребывания и за соблюдение условий договора с оператором связи.
- **Ограничение ответственности.** Авторы и соавторы репозитория не несут ответственности за любой прямой или косвенный ущерб — в том числе за сбои сети, потерю данных или потерю доступа к оборудованию.
- **Назначение материалов.** Документы носят **научно‑технический** и справочный характер: они описывают настройку открытого ПО (в т.ч. Mihomo) и **не** заменяют юридическую консультацию и **не** являются призывом к действиям, нарушающим закон.
