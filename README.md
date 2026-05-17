# mihomo_rus

Документация и практические гайды по **[Mihomo](https://github.com/MetaCubeX/mihomo)** (Clash Meta) **на русском языке** — и смежные темы: DNS, fake-ip, sniffer, правила, геоданные, связка с **nfqws2** / **XKeen** на роутерах вроде Keenetic.

Это **неофициальное** собрание: сверяйтесь с [официальной вики Mihomo](https://wiki.metacubex.one/ru/config/) и релизами вашего ядра.

---

## Содержимое репозитория

| Файл / папка | Описание |
|--------------|----------|
| [**GUIDE.md**](GUIDE.md) | Основное руководство по `config.yaml`: `general`, DNS, sniffer, `proxies`, `rules`, rule-providers, nfqws2, типичные ошибки (`GEOIP` vs сервисы, `fake-ip-filter` и др.). |
| [**mihomo/README-GEO.md**](mihomo/README-GEO.md) | Локальные `GeoSite.dat` / `geoip.metadb`, [meta-rules-dat](https://github.com/MetaCubeX/meta-rules-dat), релиз [`latest`](https://github.com/MetaCubeX/meta-rules-dat/releases/tag/latest), подключение [antifilter.download](https://antifilter.download/) через `rule-providers`. |
| [**dat/README-DAT.md**](dat/README-DAT.md) | Папка геоданных Xray (`dat/`), симлинки в Mihomo, `geodata-mode`, отличие `geoip.metadb` от набора `xray/dat`. |
| [**mihomo/config.yaml**](mihomo/config.yaml) | Пример конфига **без личных узлов** (на роутере обычно копируют как `config.yaml` в каталог `-d` Mihomo); в комментариях ссылки на гайд. |
| [**mihomo+.yml**](mihomo+.yml) | Рабочий личный конфиг (шаблон «как у автора»); **не публикуйте** без вырезания `uuid`, ключей и адресов VPS. |
| [**mihomo/**](mihomo/) | Пример `config.yaml`, снимки геоданных для гайда (`GeoSite.dat`, `geoip.metadb` — **не** обязательно актуальные; см. README-GEO), `list_geosite_tags.py`, `info.txt` (пути Entware). |

---

## С чего начать

1. Прочитать [**GUIDE.md**](GUIDE.md) по оглавлению — от `mode` и портов до `dns:` и `rules:`.
2. Если на роутере отдельно стоят Xray и Mihomo — [**dat/README-DAT.md**](dat/README-DAT.md) и [**mihomo/README-GEO.md**](mihomo/README-GEO.md).
3. Взять за основу [**mihomo/config.yaml**](mihomo/config.yaml), подставить свой прокси и группы; обновить геоданные с [meta-rules-dat `latest`](https://github.com/MetaCubeX/meta-rules-dat/releases/tag/latest) или включить `geo-auto-update` в конфиге.

---

## Полезные внешние ссылки

- [Mihomo — репозиторий](https://github.com/MetaCubeX/mihomo)
- [Конфигурация (вики, RU)](https://wiki.metacubex.one/ru/config/)
- [meta-rules-dat — геобазы под экосистему Meta](https://github.com/MetaCubeX/meta-rules-dat) · [релиз `latest`](https://github.com/MetaCubeX/meta-rules-dat/releases/tag/latest)

---

## Лицензия и вклад

Материалы распространяются «как есть», без гарантий. Если репозиторий приватный — приглашайте соавторов через GitHub; для публичного форка достаточно сохранить указание источника и не публиковать чужие секреты из конфигов.

Предложения по правкам — через issues / pull requests в вашем процессе работы с репозиторием **mihomo_rus**.
