<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/Mihomo-v1.19+-blue?logo=go&labelColor=1a1a2e&color=00d4aa">
    <img src="https://img.shields.io/badge/Mihomo-v1.19+-blue?logo=go&labelColor=e8f4f8&color=0ea5e9" alt="Mihomo">
  </picture>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/docs-wiki-2ea44f?labelColor=1a1a2e&color=00d4aa">
    <img src="https://img.shields.io/badge/docs-wiki-2ea44f?labelColor=e8f4f8&color=16a34a" alt="Wiki">
  </picture>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/license-MIT-f5f5f5?labelColor=1a1a2e&color=f5f5f5">
    <img src="https://img.shields.io/badge/license-MIT-334155?labelColor=e8f4f8&color=334155" alt="MIT">
  </picture>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/keenetic-gide-ff6b35?labelColor=1a1a2e&color=ff6b35">
    <img src="https://img.shields.io/badge/keenetic-ready-ff6b35?labelColor=e8f4f8&color=ea580c" alt="Keenetic">
  </picture>
</p>

<h1 align="center">🧭 mihomo_rus</h1>

<p align="center">
  <b>Русскоязычное руководство по Mihomo</b><br>
  <i>От первых портов до полного контроля — с нюансами для Keenetic, nfqws2 и XKeen</i>
</p>

<p align="center">
  <a href="https://github.com/zhoel-sherk/mihomo_rus/wiki">📖 GitHub Wiki</a>
  ·
  <a href="GUIDE.md">🚀 Быстрый старт</a>
  ·
  <a href="mihomo/config.yaml">⚙️ Пример конфига</a>
</p>

---

## 📋 Что внутри

| Навигация | О чём |
|-----------|-------|
| [**📖 Wiki**](https://github.com/zhoel-sherk/mihomo_rus/wiki) — полный разбор config.yaml | General, TUN, DNS, Sniffer, Rules, VLESS, Proxy Groups, nfqws2 — всё постранично |
| [**🚀 GUIDE.md**](GUIDE.md) | Индекс с быстрым стартом и ссылками на Wiki |
| [**📄 mihomo/config.yaml**](mihomo/config.yaml) | Рабочий пример без личных узлов |
| [**📚 docs/ru/proxies.md**](docs/ru/proxies.md) | Шпаргалка по всем типам исходящих узлов |
| [**🖥️ docs/ru/web-ui.md**](docs/ru/web-ui.md) | Yacd, Metacubexd, XKeen-UI — панели управления |
| [**🧩 mihomo/examples/**](mihomo/examples/) | Фрагменты конфигов под разные сценарии |
| [**🌐 docs/ru/geo-xray-dat.md**](docs/ru/geo-xray-dat.md) | GeoSite, GeoIP, symlinks, geodata-mode |
| [**🔗 docs/ru/interop-xkeen-nfqws-mihomo.md**](docs/ru/interop-xkeen-nfqws-mihomo.md) | XKeen + nfqws2 + Mihomo — типичные конфликты |

---

## 🚀 С чего начать

```mermaid
flowchart LR
    A[📖 Wiki] --> B[⚙️ config.yaml]
    B --> C[📚 proxies.md]
    C --> D[🖥️ web-ui.md]
    D --> E[🌐 geo-xray-dat.md]
    style A fill:#e0f2fe,stroke:#0284c7
    style B fill:#dcfce7,stroke:#16a34a
    style C fill:#fef3c7,stroke:#d97706
    style D fill:#f3e8ff,stroke:#9333ea
    style E fill:#fce7f3,stroke:#db2777
```

1. **📖 Вики** — открывай [Wiki](https://github.com/zhoel-sherk/mihomo_rus/wiki) и читай нужный раздел
2. **⚙️ Конфиг** — бери за основу [`mihomo/config.yaml`](mihomo/config.yaml)
3. **📚 Прокси** — вставь свои узлы, сверяясь с [`docs/ru/proxies.md`](docs/ru/proxies.md)
4. **🖥️ Панель** — подключи веб-интерфейс: [`docs/ru/web-ui.md`](docs/ru/web-ui.md)
5. **🌐 Гео** — если на роутере Xray — [`docs/ru/geo-xray-dat.md`](docs/ru/geo-xray-dat.md)

---

## 🔗 Ссылки

| Ресурс | Описание |
|--------|----------|
| [![](https://img.shields.io/badge/Mihomo-github-181717?logo=github)](https://github.com/MetaCubeX/mihomo) | Исходники ядра и релизы |
| [![](https://img.shields.io/badge/Wiki-EN/ZH-2ea44f)](https://wiki.metacubex.one/ru/config/) | Официальная документация (русской нет) |
| [![](https://img.shields.io/badge/meta--rules--dat-latest-blue)](https://github.com/MetaCubeX/meta-rules-dat/releases/tag/latest) | Геобазы для Mihomo |
| [![](https://img.shields.io/badge/XKeen-keenetic-ff6b35?logo=go)](https://github.com/Corvus-Malus/XKeen) | Обвязка Mihomo для Keenetic |
| [![](https://img.shields.io/badge/XKeen--UI-web-8b5cf6?logo=react)](https://github.com/zxc-rv/XKeen-UI) | Веб-интерфейс для XKeen |
| [![](https://img.shields.io/badge/sign--craze-utility-f43f5e?logo=python)](https://github.com/kittylabassistant/sign-craze) | Автоматизация подписей в XKeen |

---

<details>
<summary><b>⚖️ Лицензия и дисклеймер</b></summary>

<br>

Материалы распространяются «как есть», без гарантий.  
Вы сами отвечаете за законность использования в своей стране.

**AI-дисклеймер:** значительная часть текста подготовлена с помощью нейросетей и затем вычитана вручную.  
Полный аудит ещё впереди — баги и неточности могут встречаться.

</details>
