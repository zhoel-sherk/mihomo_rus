# Веб-интерфейсы: Mihomo API, XKeen-UI, Yacd-meta, metacubexd

Кратко о том, как открыть **панель управления** ядром Mihomo и чем отличаются популярные UI. Общие настройки в конфиге — раздел **Controller** в [**GUIDE.md**](../../GUIDE.md) и [вики — general](https://wiki.metacubex.one/ru/config/general/).

## Общая схема (Mihomo REST API)

Mihomo поднимает **HTTP API** (по умолчанию `127.0.0.1:9090`). Панели — это **статический фронтенд** + запросы к этому API.

| Параметр конфига | Назначение |
|--------------------|------------|
| `external-controller` | `IP:порт` API (на роутере часто `0.0.0.0:9090`, чтобы был доступ из LAN). |
| `secret` | Токен в заголовке `Authorization: Bearer …` (обязательно задать при доступе не только с localhost). |
| `external-ui` | Путь к **распакованной** папке UI на диске рядом с `-d`. |
| `external-ui-url` | URL **zip**-архива с UI — ядро может скачать/обновить (см. дефолты в исходниках Mihomo). |
| `external-ui-name` | Подкаталог URL вида `http://…:9090/ui/<name>`. |
| `allow-lan` | Должен быть `true`, если заходите к API/UI с других машин в сети. |

Типичный адрес в браузере после настройки `external-ui`:

`http://<IP-роутера>:9090/ui/`

или с именем из `external-ui-name`. Точный путь смотрите в логе старта и вики.

**Безопасность:** не оставляйте `secret: ""` и `0.0.0.0:9090` без файрвола: любой в LAN сможет менять маршрутизацию и читать статистику.

---

## [XKeen-UI](https://github.com/zxc-rv/XKeen-UI)

Веб-интерфейс для установщика/сценария **[XKeen](https://github.com/Corvus-Malus/XKeen)** на роутерах **Keenetic**. Это **не** встроенная панель Meta внутри бинарника Mihomo: XKeen-UI помогает настраивать окружение XKeen (в т.ч. вокруг **Mihomo**, **nfqws**, Xray и т.д. — по возможностям самого XKeen).

- Отдельного «официального руководства» у проекта может не быть — ориентируйтесь на **README** и **Issues** репозитория [zxc-rv/XKeen-UI](https://github.com/zxc-rv/XKeen-UI).
- Если UI предлагает ввести **URL или адрес API Mihomo**, укажите тот же хост/порт, что в `external-controller`, и тот же `secret`, что в конфиге ядра (если поддерживается сценарием XKeen-UI — проверьте актуальную версию).

При расхождении между этим гайдом и репозиторием XKeen-UI **приоритет у upstream**.

---

## [Yacd-meta](https://github.com/MetaCubeX/Yacd-meta)

Форк **Yet Another Clash Dashboard** под Clash **Meta** / Mihomo: лёгкая панель, привычный интерфейс «прокси / правила / лог».

- Установка: положить сборку в каталог из `external-ui` или указать zip в `external-ui-url` (см. релизы [Yacd-meta](https://github.com/MetaCubeX/Yacd-meta/releases)).
- Подходит, если нужен **минималистичный** UI без лишних функций.

---

## [metacubexd](https://github.com/MetaCubeX/metacubexd)

«Домашняя» панель экосистемы **MetaCubeX** для Mihomo: активно развивается, часто используется как **дефолтный** `external-ui-url` в примерах конфигов ядра.

- Репозиторий: [MetaCubeX/metacubexd](https://github.com/MetaCubeX/metacubexd) (ветка `gh-pages` / релизы архивом).
- Удобно сочетать с `profile.store-selected` и группами `select` — состояние выбора узлов сохраняется между перезапусками (см. [**GUIDE.md**](../../GUIDE.md)).

---

## [sign-craze](https://github.com/kittylabassistant/sign-craze)

Отдельная **Go-утилита** для Keenetic + Entware: управление **iptables/ipset**, установка и переключение ядер **sing-box**, **xray** и **mihomo**, опционально **nfqws2** для DPI. Это **не** встроенный `external-ui` Mihomo и **не** панель только к Clash API.

По README проекта при включённом Web UI слушаются (только из LAN, детали — upstream):

| Порт | Назначение (по документации sign-craze) |
|------|----------------------------------------|
| **9090** | Zashboard (дашборд) |
| **9091** | admin API |
| **9092** | Routing Editor (inbound/outbound/rules для активного ядра) |

**Конфликт с Mihomo:** у Mihomo типичный **`external-controller`** — это тоже HTTP API, часто на **`0.0.0.0:9090`** (и путь `/ui/` для статики). Если на одном хосте одновременно работают **sign-craze (Zashboard на 9090)** и **Mihomo с тем же портом**, один из сервисов не поднимется или «перехватит» порт. Имеет смысл заранее развести порты: например, сменить **`external-controller`** в `config.yaml` Mihomo на другой (например **9093**), либо следовать рекомендациям sign-craze по смене портов UI — сверяйте актуальный README и wiki.

Если вы используете **XKeen / XKeen-UI** параллельно со **sign-craze**, не смешивайте понятия: у каждого свой способ установки ядер и своих веб-портов; итоговую схему лучше выстроить по одному «оркестратору» или явно разделить роли (см. [**interop-xkeen-nfqws-mihomo.md**](interop-xkeen-nfqws-mihomo.md)).

---

## Сравнение коротко

| Проект | К чему подключается | Типичный сценарий |
|--------|---------------------|-------------------|
| **XKeen-UI** | XKeen на Keenetic | Установка, сценарии, связка с Mihomo/nfqws — см. README проекта |
| **Yacd-meta** | REST Mihomo | Универсальная лёгкая панель |
| **metacubexd** | REST Mihomo | Рекомендуемая панель Meta, близка к актуальным фичам ядра |
| **sign-craze** | sing-box / xray / mihomo + свой UI на Keenetic | Файрвол, DPI (nfqws2), переключение ядра; **проверьте порты 9090–9092 vs `external-controller`** |

---

## Ссылки

- [Mihomo — репозиторий](https://github.com/MetaCubeX/mihomo)
- [Конфигурация (вики)](https://wiki.metacubex.one/ru/config/) — страницы на EN/ZH; детали полей сверяйте с локальным [Meta-Docs](https://github.com/MetaCubeX/Meta-Docs) ([инструкция клона](../REFERENCE-META-DOCS.md))
- [sign-craze](https://github.com/kittylabassistant/sign-craze) — Keenetic, несколько ядер + Web UI (порты см. выше)
