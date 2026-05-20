# Совместимость XKeen, XKeen-UI, nfqws2-keenetic, Mihomo и sign-craze

> **Дисклеймер.** Ниже — обобщение по **открытой документации** проектов ([XKeen](https://github.com/Corvus-Malus/XKeen), [XKeen-UI](https://github.com/zxc-rv/XKeen-UI), [nfqws2-keenetic](https://github.com/nfqws/nfqws2-keenetic), [Mihomo](https://github.com/MetaCubeX/mihomo), [sign-craze](https://github.com/kittylabassistant/sign-craze)) и по материалам этого репозитория ([**GUIDE.md**](../../GUIDE.md)). Реальные цепочки **iptables/nftables**, номера **NFQUEUE**, имена цепочек и порядок правил на вашем роутере **могут отличаться** от примеров в README. Проверяйте: `iptables-save`, `nft list ruleset`, логи **nfqws2** и **Mihomo**, счётчики правил.

---

## 1. Роли компонентов

| Компонент | Назначение | Типичное влияние на сеть |
|-----------|------------|---------------------------|
| **[XKeen](https://github.com/Corvus-Malus/XKeen)** | Установка и оркестрация **Xray** и/или **Mihomo** на Entware Keenetic, бэкапы конфигов, обновление ядер (`-ux`, `-um`), геофайлы Xray (`-g`), запуск сценария проксирования. | В README указаны зависимости вроде **iptables**; применяются правила **iptables/ip6tables**; в changelog упоминаются режимы **TProxy**, **Mixed**, **Redirect** для входящих/прозрачного прокси. |
| **[XKeen-UI](https://github.com/zxc-rv/XKeen-UI)** | Веб-панель: мониторинг, логи, редактирование конфигов, **переключение/обновление ядер Xray и Mihomo**, реализация **Clash API** для Mihomo. | Сама по себе **не** ставит netfilter-правила; влияет через **перезапуск** сервисов и изменение **`config.yaml`** / `external-controller`. |
| **[nfqws2-keenetic](https://github.com/nfqws/nfqws2-keenetic)** | Пакеты **nfqws2** (ветка zapret): модификация TCP/UDP на уровне пакетов через **NFQUEUE** ([теория](https://github.com/bol-van/zapret2)). | Скрипты добавляют правила **iptables** (пример цепочки **`nfqws_post`**, очередь **`NFQUEUE`**, в README — исключение по **mark** `0x40000000/0x40000000`). Порты задаются **`TCP_PORTS` / `UDP_PORTS`** (в т.ч. **443** для QUIC). |
| **Mihomo** | Выбор исходящей политики (**`rules:`**, **`proxy-groups:`**), прозрачный **tproxy/redir**, опционально **`tun:`**, встроенный **`dns:`**, **sniffer**, **fake-ip**. | Может менять **маршрутизацию** (`tun` + `auto-route`), **nftables** (например `auto-redirect` в Linux), DNS-ответы клиентам. |
| **[sign-craze](https://github.com/kittylabassistant/sign-craze)** | Отдельный **оркестратор** на Go: **iptables/ipset**, выбор ядра (**sing-box** / **xray** / **mihomo**), опционально **nfqws2** (DPI через NFQUEUE), Web UI (**9090** / **9091** / **9092** по README). | Параллельно с XKeen — **два установщика** одних и тех же бинарников и **два набора** netfilter-правил, если не развести роли. С **Mihomo** — следите за портом **`external-controller`** vs **9090** (Zashboard); см. [**web-ui.md**](web-ui.md). |

**Сводка:** на одном роутере одновременно работают **несколько независимых «слоёв»** — установщик/обвязка (XKeen или отдельно **sign-craze**), DPI-обход (nfqws2), политика трафика (Mihomo), UI (XKeen-UI и/или панели sign-craze). Конфликты возникают, когда **два слоя пытаются сделать одно и то же** (захват того же трафика, подмена DNS, резание того же QUIC).

---

## 2. Netfilter и маршрутизация — где сталкиваются

### 2.1. iptables (XKeen, nfqws2) и nftables / ip route (Mihomo TUN)

- **XKeen** в документации опирается на **iptables** и **ip6tables** (в т.ч. отдельная логика при отсутствии IPv6).
- **nfqws2-keenetic** строит правила **iptables** (цепочки вроде **`nfqws_post`**, отправка в **NFQUEUE**).
- **Mihomo** в режиме **TUN** на Linux может использовать **nftables** для `auto-redirect` и править **таблицы маршрутизации** (`auto-route`, `iproute2-*` в конфиге — см. [GUIDE.md § TUN](../../GUIDE.md#sec-tun)).

На KeeneticOS часть функций ядра и **ускорителей** может обходить классический путь netfilter. В README **nfqws2-keenetic** прямо указано: при **flow offloading / hardware NAT** пакеты могут **не попадать** в ожидаемые цепочки iptables — то же влияет на **прозрачный прокси Mihomo**, если он завязан на тот же путь.

**Вывод:** не смешивайте без необходимости **полный TUN Mihomo** (`auto-route: true`, `strict-route: true`) с уже настроенной цепочкой **прозрачного прокси + nfqws**, если не контролируете все маршруты и mark. Подробнее — [GUIDE.md § TUN и Keenetic](../../GUIDE.md#sec-tun), [§ nfqws2, п. 6](../../GUIDE.md#sec-nfqws).

### 2.2. Mihomo `tun:` vs «классика» XKeen (tproxy / redir)

Корневой **`tun:`** с **`auto-route: true`** перехватывает **маршрут по умолчанию** на самом роутере. Типичная схема XKeen + Mihomo на Keenetic — **tproxy-порт Mihomo** + правила перенаправления **без** глобального TUN-захвата. Включение TUN «как на ПК» поверх **nftables → nfqws → tproxy** даёт риск **петель, обхода nfqws или потери доступа к веб-морде роутера**.

### 2.3. NFQUEUE (nfqws2) и политика Mihomo на тот же трафик

- nfqws2 обрабатывает пакеты, попавшие в **очередь** по правилам (TCP/UDP порты из конфига, списки доменов/IP).
- Mihomo может **REJECT** или иначе обрывать **тот же UDP** (например QUIC к `GEOSITE,google`), менять назначение через **sniffer**.

Если один и тот же поток **сначала режется в Mihomo**, до nfqws он может **не дойти** в ожидаемом виде; если порядок обратный — nfqws и sniffer могут **расходиться** в представлении о «целевом» хосте.

**Практика:** явно решить, **какие протоколы и сервисы** обходит только nfqws, а какие ведёт только Mihomo ([GUIDE.md § nfqws, п. 1 и 5](../../GUIDE.md#sec-nfqws)).

### 2.4. Маркировка пакетов (fwmark)

В примере из README nfqws2 встречается исключение по **mark** (не слать в NFQUEUE уже помеченное). У Mihomo в **`general`** есть **`routing-mark`** — при стыковке с собственными цепочками важно **не пересечься** с чужими масками и не создать цикл «пометил → снова в очередь».

### 2.5. Режимы XKeen: TProxy, Mixed, Redirect

В README XKeen описано: **Mixed** сочетает преимущества TProxy и Redirect (UDP через TProxy, TCP через Redirect); **TProxy** — для UDP+TCP; **Redirect** — только TCP. В changelog отмечено исправление **совместной работы TProxy и SOCKS5** (раньше Mixed ломал прозрачное проксирование). Это значит: **несогласованный выбор режима** ломает не Mihomo как таковой, а **путь пакета до входа в Mihomo**.

---

## 3. DNS — конфликты и разводка

**nfqws2-keenetic** рекомендует:

- игнорировать DNS провайдера в интерфейсе Keenetic;
- по возможности использовать **DoT/DoH** на стороне роутера;
- отключать сторонние **DNS-фильтры** (NextDNS, SkyDNS и т.д.) в веб-интерфейсе.

**Mihomo** при **`enhanced-mode: fake-ip`** сам становится DNS для клиентов, которые на него направлены, и ведёт **`nameserver` / `fallback` / `nameserver-policy`**.

**Зона конфликта:** «честный» IP для домена, который нужен **nfqws** для стратегии по имени, vs **fake-ip** от Mihomo. Решения уже собраны в [GUIDE.md § nfqws, п. 3](../../GUIDE.md#sec-nfqws): **`real-ip`** в `fake-ip-filter`, ранний **DIRECT** в `rules:`, **`nameserver-policy`** для зон.

---

## 4. Геоданные и автообновления

- **XKeen**: параметр **`-g`** для переустановки/грузов **геофайлов Xray** (`opt/etc/xray/dat` и смежные пути — см. README XKeen).
- **Mihomo**: **`geo-auto-update`**, **`geox-url`**, файлы в каталоге **`-d`** (`GeoSite.dat`, `geoip.metadb`, …).

Полный разбор симлинков Xray `dat` vs Mihomo — [**geo-xray-dat.md**](geo-xray-dat.md). Кратко: **не запускайте два независимых автообновления**, перезаписывающих одни и те же файлы без контроля версий; согласуйте **`geo-auto-update`** в Mihomo с тем, обновляет ли гео **XKeen** по расписанию.

---

## 5. XKeen-UI — косвенные конфликты

Панель **не** является частью netfilter, но:

1. **Смена ядра** (Xray ↔ Mihomo) или обновление бинарника во время активного трафика даёт краткий **обрыв** и рассинхрон с **iptables**-правилами, которые ожидают процесс на конкретном порту.
2. **Clash API** для Mihomo: второй клиент к **`external-controller`** или смена **`secret`** ломает уже настроенные панели (**Yacd**, **metacubexd**) — см. также [**web-ui.md**](web-ui.md).
3. **Доступ из WAN**: в README XKeen-UI предупреждение о рисках открытия панели в интернет; к **Mihomo API** то же относится.

---

## 6. Рекомендуемые паттерны («как не бороться»)

- **Прозрачный Mihomo** (`tproxy-port` / **`listeners:`** type `tproxy`) + правила XKeen; **без** `tun.auto-route`, если нет полной схемы маршрутов ([GUIDE.md § nfqws, п. 6](../../GUIDE.md#sec-nfqws)).
- **`ipv6: false`** и **`find-process-mode: off`** в `general` для роутера — см. [GUIDE.md § nfqws, п. 2](../../GUIDE.md#sec-nfqws).
- **Порядок `rules:`**: сначала исключения (**DIRECT** / узкие **AND**) для трафика под **nfqws**, затем общие правила на прокси ([п. 5](../../GUIDE.md#sec-nfqws)).
- **Sniffer `skip-domain`**: зоны, где DPI уже «подправлен» nfqws, не должны дополнительно ломаться sniffer ([п. 4](../../GUIDE.md#sec-nfqws)).
- **Один ответственный за QUIC**: либо режете QUIC в Mihomo, либо ведёте через nfqws — не дублируйте без понимания ([п. 5](../../GUIDE.md#sec-nfqws)).
- **Offloading / IntelliQOS / фильтры Keenetic** — при «ничего не матчится» в NFQUEUE или tproxy сначала проверьте README nfqws2 (раздел «Если ничего не работает»).

### Симптом → куда смотреть

| Симптом | Возможные причины (сводно) |
|---------|---------------------------|
| Работает по IP, не работает по домену | **DNS**, **fake-ip**, **sniffer**; не только nfqws ([GUIDE.md § nfqws, п. 7](../../GUIDE.md#sec-nfqws)). |
| Прозрачный прокси «мёртв», SOCKS жив | Режим **Redirect** вместо **TProxy/Mixed** для нужного сценария (см. README XKeen). |
| nfqws не видит трафик | **Hardware NAT / offloading**, не те **интерфейсы** в `ISP_INTERFACE`, фильтры DNS в веб-интерфейсе (nfqws2 README). |
| Петля или нет интернета после включения TUN | **`auto-route` / `strict-route`** vs маршруты XKeen; отключить TUN и вернуться к tproxy-схеме. |
| TLS handshake timeout на прокси | Время (**NTP** на роутере и в Mihomo — [GUIDE.md § NTP](../../GUIDE.md#sec-ntp)), а не nfqws. |

---

## 7. sign-craze — ещё один «слой» на том же Keenetic

**sign-craze** — не форк XKeen и не замена Mihomo: это **свой** сценарий управления файрволом и одним из трёх ядер (**sing-box**, **xray**, **mihomo**) с единым CLI/Web UI. В README заявлены **DPI через nfqws2** (opt-in: загрузка nfqws2 при `--dpi on` или `--install --with-dpi`) и отдельные цепочки вроде **`signcraze_dpi_fwd`** в **mangle FORWARD** — то есть возможен **второй независимый** путь NFQUEUE рядом с правилами из **nfqws2-keenetic** или XKeen, если включить всё сразу.

**Риски совмещения с таблицей выше:**

| Тема | Замечание |
|------|-----------|
| **Двойной DPI / двойная очередь** | И **sign-craze**, и «голый» nfqws2-keenetic работают через iptables/NFQUEUE. Два набора правил на один и тот же TCP/443 или QUIC без исключений по **mark**/интерфейсу дают непредсказуемый порядок и лишнюю нагрузку. Обычно выбирают **один** активный DPI-стек. |
| **Двойной оркестратор ядра** | XKeen и sign-craze оба могут ставить/обновлять **mihomo** или **xray**. Имеет смысл не запускать два установщика на одну и ту же роль без явного разделения (кто владеет бинарником, автозапуском и `config.yaml`). |
| **Порты Web / API** | У sign-craze по документации UI на **9090**, **9091**, **9092**; у Mihomo часто **`external-controller: …:9090`**. На одном хосте — коллизия; см. [**web-ui.md**](web-ui.md). |
| **TUN и policy/full** | У sign-craze описаны режимы маршрутизации (**policy** vs **full**) и взаимодействие с DPI; у Mihomo отдельно — **TUN** и **tproxy**. Совмещение «полный прокси на роутере» из двух инструментов без схемы маршрутов повышает риск петель — как в [§ 2.2](#22-mihomo-tun-vs-классика-xkeen-tproxy--redir). |
| **DNS** | Как и для связки nfqws + Mihomo: один источник правды для имён, согласованность с **fake-ip** ([§ 3](#3-dns--конфликты-и-разводка)). |

Практический совет: если вы уже на **XKeen + XKeen-UI + Mihomo + nfqws2**, перед добавлением **sign-craze** прочитайте wiki проекта и решите, **какой** компонент владеет iptables, **какое** ядро основное и **какие** порты закреплены за API панелей.

---

## 8. Ссылки

| Ресурс | URL |
|--------|-----|
| XKeen | [https://github.com/Corvus-Malus/XKeen](https://github.com/Corvus-Malus/XKeen) |
| XKeen-UI | [https://github.com/zxc-rv/XKeen-UI](https://github.com/zxc-rv/XKeen-UI) |
| nfqws2-keenetic | [https://github.com/nfqws/nfqws2-keenetic](https://github.com/nfqws/nfqws2-keenetic) |
| zapret2 (основа nfqws) | [https://github.com/bol-van/zapret2](https://github.com/bol-van/zapret2) |
| Mihomo | [https://github.com/MetaCubeX/mihomo](https://github.com/MetaCubeX/mihomo) |
| sign-craze | [https://github.com/kittylabassistant/sign-craze](https://github.com/kittylabassistant/sign-craze) |
| Гайд по `config.yaml` (этот репозиторий) | [../../GUIDE.md](../../GUIDE.md) |
| Xray `dat` vs Mihomo geo | [geo-xray-dat.md](geo-xray-dat.md) |
| Веб-панели и API | [web-ui.md](web-ui.md) |

---

*Материал носит справочный характер; законность использования обхода ограничений сети определяется законодательством вашей страны и условиями договора с провайдером.*
