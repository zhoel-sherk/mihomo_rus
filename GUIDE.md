# Руководство по config.yaml Mihomo

> **Версия документа:** ориентир — ядро Mihomo **v1.19.x** и новее (проверяйте `mihomo -v` и [релизы](https://github.com/MetaCubeX/mihomo/releases): отдельные ключи и значения по умолчанию меняются между версиями).

Справочник по настройке ядра [Mihomo](https://github.com/MetaCubeX/mihomo) (Clash Meta). Официальная вики: [Configuration](https://wiki.metacubex.one/en/config/).

Полное руководство перенесено в **[GitHub Wiki](https://github.com/zhoel-sherk/mihomo_rus/wiki)**.

## С чего начать

1. Открой [Wiki](https://github.com/zhoel-sherk/mihomo_rus/wiki) — там все разделы постранично
2. Готовый публикуемый пример без личных узлов — [`mihomo/config.yaml`](mihomo/config.yaml)
3. Типы исходящих узлов — [`docs/ru/proxies.md`](docs/ru/proxies.md)
4. Веб-панели — [`docs/ru/web-ui.md`](docs/ru/web-ui.md)

## Быстрый старт (минимальный конфиг)

```yaml
mixed-port: 10801
allow-lan: true
mode: rule
log-level: info
ipv6: false
find-process-mode: off

proxies: []

proxy-groups:
  - name: PROXY
    type: select
    proxies:
      - DIRECT

rules:
  - MATCH,PROXY
```

## Страницы Wiki

- [Home](https://github.com/zhoel-sherk/mihomo_rus/wiki/Home) — введение, быстрый старт
- [General](https://github.com/zhoel-sherk/mihomo_rus/wiki/General) — глобальная конфигурация
- [Proxy Ports](https://github.com/zhoel-sherk/mihomo_rus/wiki/Proxy-Ports) — порты прокси
- [TUN](https://github.com/zhoel-sherk/mihomo_rus/wiki/TUN) — виртуальный интерфейс
- [DNS](https://github.com/zhoel-sherk/mihomo_rus/wiki/DNS) — hosts, dns-блок, схемы
- [Sniffer](https://github.com/zhoel-sherk/mihomo_rus/wiki/Sniffer) — перехват SNI/Host
- [Listeners](https://github.com/zhoel-sherk/mihomo_rus/wiki/Listeners) — входящие listeners
- [Proxies (Common Fields)](https://github.com/zhoel-sherk/mihomo_rus/wiki/Proxies-Common) — общие поля исходящих
- [Proxy Groups](https://github.com/zhoel-sherk/mihomo_rus/wiki/Proxy-Groups) — группы прокси
- [VLESS](https://github.com/zhoel-sherk/mihomo_rus/wiki/VLESS) — протокол VLESS
- [Rules](https://github.com/zhoel-sherk/mihomo_rus/wiki/Rules) — правила и rule-set
- [Proxy Providers](https://github.com/zhoel-sherk/mihomo_rus/wiki/Proxy-Providers) — провайдеры прокси
- [Sub-Rules](https://github.com/zhoel-sherk/mihomo_rus/wiki/Sub-Rules) — подправила
- [Tunnels](https://github.com/zhoel-sherk/mihomo_rus/wiki/Tunnels) — туннели
- [nfqws2](https://github.com/zhoel-sherk/mihomo_rus/wiki/nfqws2) — совместная работа с nfqws2
- [NTP](https://github.com/zhoel-sherk/mihomo_rus/wiki/NTP) — синхронизация времени
- [Experimental](https://github.com/zhoel-sherk/mihomo_rus/wiki/Experimental) — экспериментальные опции
