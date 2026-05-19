# Исходящие узлы Mihomo: блок `proxies:`

Справочник по полям и типам **исходящих** прокси в [Mihomo](https://github.com/MetaCubeX/mihomo). Общая архитектура конфига и смежные разделы — в корневом [**GUIDE.md**](../../GUIDE.md).

**Канон по формулировкам и YAML:** исходники [Meta-Docs](https://github.com/MetaCubeX/Meta-Docs), каталог `docs/config/proxies/` (удобно клонировать локально — см. [**REFERENCE-META-DOCS.md**](../REFERENCE-META-DOCS.md)). Русские `*.ru.md` там часто машинные: этот текст переписан с опорой на **английские** `*.en.md` / нейтральные `*.md`.

## Оглавление

1. [Общие поля](#obshchie-polya)
2. [TLS (общие поля для протоколов с TLS)](#tls)
3. [Транспорт `network`](#transport)
4. [Встроенные политики (DIRECT, REJECT, …)](#builtin)
5. [Тип `direct`](#direct)
6. [Тип `dns`](#dns)
7. [Цепочка `dialer-proxy`](#dialer-proxy)
8. [`http`](#http) · [`socks5`](#socks5)
9. [`ss` Shadowsocks](#ss)
10. [`ssr` ShadowsocksR](#ssr)
11. [`vmess`](#vmess)
12. [`vless`](#vless)
13. [`trojan`](#trojan)
14. [`snell`](#snell)
15. [`ssh`](#ssh)
16. [`wireguard`](#wireguard)
17. [`hysteria`](#hysteria) · [`hysteria2`](#hysteria2)
18. [`tuic`](#tuic)
19. [`anytls`](#anytls)
20. [`mieru`](#mieru) · [`masque`](#masque)
21. [`openvpn`](#openvpn) · [`tailscale`](#tailscale)
22. [`sudoku`](#sudoku) · [`trusttunnel`](#trusttunnel)

---

<a id="obshchie-polya"></a>

## Общие поля

Узлы задаются **массивом** под ключом `proxies:`. У каждого элемента есть общие поля (подробнее — [Meta-Docs proxies index (EN)](https://github.com/MetaCubeX/Meta-Docs/blob/main/docs/config/proxies/index.en.md)).

```yaml
proxies:
  - name: "example"
    type: ss
    server: server.example
    port: 443
    ip-version: ipv4
    udp: true
    interface-name: eth0
    routing-mark: 1234
    tfo: false
    mptcp: false
    dialer-proxy: other-node
    smux:
      enabled: false
```

| Поле | Обязательно | Смысл |
|------|---------------|--------|
| `name` | да | Уникальное имя узла; на него ссылаются `proxy-groups` и `rules`. |
| `type` | да | Тип протокола (`ss`, `vless`, …). |
| `server` | да* | Хост или IP сервера (*у `direct`/`dns` и части особых типов — свои правила, см. ниже). |
| `port` | да* | Порт (*аналогично). |
| `ip-version` | нет | `dual` / `ipv4` / `ipv6` / `ipv4-prefer` / `ipv6-prefer`. Для не-`direct` влияет на то, какой адрес берётся при **доменном** `server`. По умолчанию `dual`. |
| `udp` | нет | Разрешить UDP через узел. По умолчанию `false`; для UDP-протоколов вроде `tuic`, а также `direct` и `dns` — по смыслу протокола часто включается по умолчанию (см. upstream-доки). |
| `interface-name` | нет | Исходящие соединения узла привязать к интерфейсу ОС. |
| `routing-mark` | нет | Маркировка маршрута (fwmark) при установке соединений (Linux). |
| `tfo` | нет | TCP Fast Open, только для TCP. |
| `mptcp` | нет | MPTCP, только для TCP. |
| `dialer-proxy` | нет | Имя **другого** узла или **группы**: до целевого сервера этот узел строит туннель **через** указанный dialer (цепочка). См. [§ dialer-proxy](#dialer-proxy). |
| `smux` | нет | sing-mux: мультиплексирование поверх **TCP**-транспорта (`enabled`, `protocol`, лимиты потоков, `brutal-opts` и т.д.). На UDP влияет только при `only-tcp: false` по правилам smux — см. upstream. |

---

<a id="tls"></a>

## TLS

Используется в протоколах с TLS (VLESS/VMess/Trojan/…). Полный перечень — [Meta-Docs tls.en.md](https://github.com/MetaCubeX/Meta-Docs/blob/main/docs/config/proxies/tls.en.md).

Кратко:

| Поле | Смысл |
|------|--------|
| `tls` | Включить TLS (для `trojan` обязателен). |
| `sni` / `servername` | Имя для SNI; в VMess/VLESS поле исторически называется `servername`. Пустое — по умолчанию как `server`. |
| `fingerprint` | SHA256 отпечаток **сертификата** (pinning). Не путать с HPKP «публичный ключ». Поведение для leaf vs CA — см. предупреждения в upstream. |
| `alpn` | Список ALPN по приоритету (`h2`, `http/1.1`, `h3`, …). |
| `skip-cert-verify` | Отключить проверку сертификата (только осознанно). |
| `certificate` / `private-key` | Клиентский mTLS (PEM или путь к файлу). |
| `client-fingerprint` | Отпечаток клиента (uTLS): `chrome`, `firefox`, …, `random` — для VMess/VLESS/Trojan/AnyTLS. |
| `reality-opts` | REALITY: `public-key`, `short-id`, опционально `support-x25519mlkem768`. |
| `ech-opts` | ECH: `enable`, `config` (base64), опционально `query-server-name`. Генерация: `mihomo generate ech-keypair …`. |

---

<a id="transport"></a>

## Транспорт `network`

Поле **`network`** (и вложенные `*-opts`) задаёт оболочку поверх TCP/QUIC: `ws`, `http`, `h2`, `grpc`, `xhttp` и др. Точные ключи зависят от типа протокола (например, VLESS поддерживает `xhttp`, VMess — нет).

Полная таблица опций, режимы `xhttp-opts`, HTTPUpgrade и пр. — в [Meta-Docs transport.en.md](https://github.com/MetaCubeX/Meta-Docs/blob/main/docs/config/proxies/transport.en.md) (файл большой; держите локальный клон Meta-Docs для поиска).

---

<a id="builtin"></a>

## Встроенные политики

В **`rules:`** и **`proxy-groups`** используются не только имена из `proxies:`, но и встроенные исходы:

| Имя | Действие |
|-----|----------|
| `DIRECT` | Прямое соединение. |
| `REJECT` | Отклонить с уведомлением (типично RST/ошибка в зависимости от транспорта). |
| `REJECT-DROP` | Тихо сбросить. |
| `PASS` | Пропустить правило (редкий сценарий в подправилах). |
| `COMPATIBLE` | Совместимость: когда в группе не выбран узел — эквивалентно `DIRECT`. |

---

<a id="direct"></a>

## Тип `direct`

Прямой выход без прокси-сервера. Поля — общие (`udp`, `ip-version`, `interface-name`, `routing-mark`).

```yaml
proxies:
  - name: "direct-out"
    type: direct
    udp: true
    ip-version: ipv4
```

---

<a id="dns"></a>

## Тип `dns`

Исходящий тип **`dns`** перехватывает запросы во **внутренний DNS-модуль** Mihomo (см. блок `dns:` в конфиге), обработка идёт внутри ядра.

```yaml
proxies:
  - name: "dns-out"
    type: dns
```

---

<a id="dialer-proxy"></a>

## Цепочка `dialer-proxy`

Поле **`dialer-proxy`** указывает, что **этот** узел сначала устанавливает транспорт **через** другой узел или группу (по `name`). Типичный сценарий: свой VPS доступен только через узел из подписки. Подробные примеры и предупреждения (не брать «любой» UDP/Reality на нижнем звене) — [dialer-proxy.en.md](https://github.com/MetaCubeX/Meta-Docs/blob/main/docs/config/proxies/dialer-proxy.en.md).

---

<a id="http"></a>

## `http`

HTTP CONNECT (опционально с TLS = HTTPS-прокси). Поддерживаются `username`/`password`, заголовки `headers:`, все поля из [§ TLS](#tls) при `tls: true`.

```yaml
proxies:
  - name: "corp-http"
    type: http
    server: proxy.corp
    port: 8080
    # username: u
    # password: p
    # tls: true
```

---

<a id="socks5"></a>

## `socks5`

В YAML указывается **`type: socks5`** (в некоторых примерах Meta-Docs встречается сокращение `socks` — ориентируйтесь на версию ядра и ошибки парсера). Опционально TLS и учётные данные; см. [§ TLS](#tls).

```yaml
proxies:
  - name: "socks-local"
    type: socks5
    server: 127.0.0.1
    port: 1080
```

---

<a id="ss"></a>

## `ss` Shadowsocks

Поля: `cipher`, `password`, опционально `udp-over-tcp`, `plugin` / `plugin-opts` (obfs, v2ray-plugin, shadow-tls, …). Полный список шифров — в upstream `ss.en.md`.

```yaml
proxies:
  - name: "ss1"
    type: ss
    server: example.com
    port: 443
    cipher: aes-128-gcm
    password: "secret"
    udp: true
```

---

<a id="ssr"></a>

## `ssr` ShadowsocksR

Устаревший вариант SS с обфускацией `obfs` и `protocol`. Поля: `cipher`, `password`, `obfs`, `protocol`, опционально `obfs-param`, `protocol-param`.

---

<a id="vmess"></a>

## `vmess`

Обязательные: `uuid`, **`alterId`** (если не `0` — включается legacy-режим), **`cipher`** (`auto`, `none`, `aes-128-gcm`, …). Опционально `packet-encoding` (`packetaddr` / `xudp`), `global-padding`, `authenticated-length`, TLS и **`network`** из [§ Транспорт](#transport) (`ws`, `http`, `h2`, `grpc`).

---

<a id="vless"></a>

## `vless`

Обязательные: `uuid`. Часто: `tls`, `servername`, `flow` (например `xtls-rprx-vision` — по upstream эквивалентно xtls-*-udp443 в Xray), `packet-encoding`, поле **`encryption`** для расширенных режимов (см. длинное описание в upstream `vless.en.md`). **`network`**: `ws` / `http` / `h2` / `grpc` / `xhttp` или TCP по умолчанию.

Для блокировки «голого» UDP на 443 при использовании vision в Meta рекомендуют отдельное правило в `rules:`:

`AND,((NETWORK,UDP),(DST-PORT,443)),REJECT`

---

<a id="trojan"></a>

## `trojan`

Обязательное: `password`. TLS обязателен по смыслу протокола. Опционально **`ss-opts`**: режим совместимости с trojan-go (Shadowsocks AEAD поверх). **`network`**: `ws`, `grpc` или TCP.

---

<a id="snell"></a>

## `snell`

Проприетарный протокол Surge: `psk`, `version` (v1–v3; UDP только v3), `obfs-opts` (`mode`: `http`/`tls`, `host`).

---

<a id="ssh"></a>

## `ssh`

Тип **`ssh`**: доступ по SSH как к транспорту. Поля: `username`, `password` или ключи `private-key`, `private-key-passphrase`, доверенные `host-key`, `host-key-algorithms`.

---

<a id="wireguard"></a>

## `wireguard`

Есть **упрощённый** синтаксис (один peer) и полный (несколько peers). Ключевые поля: `private-key`, `server`, `port`, `ip`/`ipv6` внутри туннеля, `public-key` пира, `allowed-ips`, опционально `pre-shared-key`, `reserved`, `persistent-keepalive`, `mtu`, `dialer-proxy`, `remote-dns-resolve` + `dns`, блок **AmneziaWG** `amnezia-wg-option` — см. [wg.en.md](https://github.com/MetaCubeX/Meta-Docs/blob/main/docs/config/proxies/wg.en.md).

---

<a id="hysteria"></a>

## `hysteria`

Первый протокол Hysteria (QUIC). Ключевые поля: `auth-str`, `protocol` (`udp` / `wechat-video` / `faketcp`), `up` / `down` (скорости, по умолчанию Mbps), TLS, окна `recv-window-*`, опционально `obfs`. См. [hysteria.en.md](https://github.com/MetaCubeX/Meta-Docs/blob/main/docs/config/proxies/hysteria.en.md).

<a id="hysteria2"></a>

## `hysteria2`

Актуальный Hysteria2: `password`, `ports` + `hop-interval` для прыжков по портам, `up`/`down`, `obfs`/`obfs-password` (часто `salamander`), TLS, опционально `realm-opts`. Официальный справочник клиента: [hysteria.network](https://hysteria.network/en/docs/advanced-usage/#client-side).

---

<a id="tuic"></a>

## `tuic`

QUIC-based TUIC: либо **v4** (`token`), либо **v5** (`uuid` + `password`) — не смешивать поля версий. Важны `udp-relay-mode` (`native`/`quic`), `reduce-rtt` (0-RTT), `disable-sni`, TLS. См. [tuic.en.md](https://github.com/MetaCubeX/Meta-Docs/blob/main/docs/config/proxies/tuic.en.md).

---

<a id="anytls"></a>

## `anytls`

TLS-обёртка с паролем, сессии idle (`idle-session-*`, `min-idle-session`). **Mihomo не поддерживает AnyTLS+REALITY** и не планирует (upstream); для скрытия SNI — **ECH**, для Reality — VMess/VLESS/Trojan.

---

<a id="mieru"></a>

## `mieru`

Поля: `username`, `password`, `transport` (`TCP`/`UDP`), `multiplexing`, опционально `port-range` вместо `port`, `traffic-pattern` (base64, см. документацию mieru).

<a id="masque"></a>

## `masque`

RFC MASQUE / CONNECT-UDP / IP proxying: ключи `private-key`, `public-key`, адресация `ip`/`ipv6`, `mtu`, опционально `network: h2`, `dialer-proxy`, DNS-форсинг. Генерация конфигурации — инструмент [usque](https://github.com/Diniboy1123/usque) (см. upstream `masque.en.md`).

---

<a id="openvpn"></a>

## `openvpn`

Клиент OpenVPN: `proto`, либо логин/пароль, либо `cert`/`key`, плюс `ca`, опционально `tls-crypt`, шифры, `mtu`, `dialer-proxy`. См. [openvpn.en.md](https://github.com/MetaCubeX/Meta-Docs/blob/main/docs/config/proxies/openvpn.en.md).

<a id="tailscale"></a>

## `tailscale`

Встроенный `tsnet`: `hostname`, `auth-key`, `control-url` (Headscale), `state-dir`, `ephemeral`, маршруты `accept-routes`, `exit-node`, `dialer-proxy` и т.д. См. [tailscale.en.md](https://github.com/MetaCubeX/Meta-Docs/blob/main/docs/config/proxies/tailscale.en.md).

---

<a id="sudoku"></a>

## `sudoku`

Обфусцированный протокол: `key`, `aead-method`, padding, `table-type`, блок `httpmask`, `enable-pure-downlink`. Подробности полей — [sudoku.en.md](https://github.com/MetaCubeX/Meta-Docs/blob/main/docs/config/proxies/sudoku.en.md).

<a id="trusttunnel"></a>

## `trusttunnel`

TLS/QUIC-туннель с `username`/`password`, опционально `quic`, мультиплексирование (`max-connections` / `min-streams` / `max-streams` — взаимоисключающие с upstream-правилами). Русской страницы в Meta-Docs нет — ориентир только **английский** [trusttunnel.en.md](https://github.com/MetaCubeX/Meta-Docs/blob/main/docs/config/proxies/trusttunnel.en.md).

---

## Практика на роутере

- Держите **уникальные** `name` и осмысленные имена — ими же пользуются правила и панели.
- Для узла с **доменным** `server:` при обходе nfqws/zapret задайте **`ip-version: ipv4`** (или нужный режим), если IPv6 ломает схему — см. [**GUIDE.md** — nfqws](../../GUIDE.md).
- После правок всегда смотрите **лог старта** ядра: опечатки в типах и полях дают `FATAL Parse config error`.

Если какого-то поля нет в этом сжатом файле — откройте соответствующий `*.en.md` в локальном клоне **Meta-Docs** и допишите в свой конфиг по аналогии.
