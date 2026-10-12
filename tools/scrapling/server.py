"""
Scrapling MCP Server — FastMCP ile kurulmuş web scraping araç havuzu.

Araçlar:
  fetcher_get      — curl_cffi tabanlı hızlı GET (tarayıcısız)
  fetcher_post     — curl_cffi tabanlı POST
  stealthy_fetch   — Chromium tabanlı gizli tarama (anti-bot bypass)
  dynamic_fetch    — Playwright ile tam JS destekli tarama
  spider_crawl     — Çok sayfalı otomatik link takipli örümcek
  parse_html       — Ham HTML'i CSS/XPath ile ayrıştır
"""

from __future__ import annotations

import asyncio
from typing import Optional

from fastmcp import FastMCP

mcp = FastMCP("scrapling")


# ─── YARDIMCI FONKSİYONLAR ───────────────────────────────────────────────────

def _serialize_response(response) -> dict:
    """Response nesnesini JSON-serializable dict'e çevir."""
    title = None
    try:
        t = response.css("title::text").get()
        title = str(t) if t else None
    except Exception:
        pass

    links: list[str] = []
    try:
        for a in response.css("a")[:100]:
            href = a.attrib.get("href", "")
            if href:
                links.append(str(href))
    except Exception:
        pass

    text = ""
    try:
        text = str(response.get_all_text())[:8000]
    except Exception:
        pass

    html = ""
    try:
        h = response.html_content
        html = str(h) if h else ""
    except Exception:
        pass

    headers: dict = {}
    try:
        headers = dict(response.headers)
    except Exception:
        pass

    return {
        "status": response.status,
        "url": str(response.url),
        "title": title,
        "html": html,
        "text": text,
        "links": links,
        "headers": headers,
    }


def _apply_queries(response, base: dict, css_queries: list[str], xpath_queries: list[str]) -> dict:
    """CSS/XPath sorgularını yanıta uygula ve sonuçları dict'e ekle."""
    if css_queries:
        css_results: dict[str, list[str]] = {}
        for selector in css_queries:
            try:
                results = response.css(selector).getall()
                css_results[selector] = [str(r) for r in results]
            except Exception as exc:
                css_results[selector] = [f"HATA: {exc}"]
        base["css_results"] = css_results

    if xpath_queries:
        xpath_results: dict[str, list[str]] = {}
        for selector in xpath_queries:
            try:
                results = response.xpath(selector).getall()
                xpath_results[selector] = [str(r) for r in results]
            except Exception as exc:
                xpath_results[selector] = [f"HATA: {exc}"]
        base["xpath_results"] = xpath_results

    return base


def _build_result(response, css_queries: list[str] | None, xpath_queries: list[str] | None) -> dict:
    base = _serialize_response(response)
    return _apply_queries(response, base, css_queries or [], xpath_queries or [])


# ─── FETCHER (curl_cffi, tarayıcısız) ────────────────────────────────────────

@mcp.tool()
def fetcher_get(
    url: str,
    headers: Optional[dict] = None,
    proxy: Optional[str] = None,
    timeout: Optional[float] = None,
    impersonate: str = "chrome",
    stealthy_headers: bool = True,
    css_queries: Optional[list[str]] = None,
    xpath_queries: Optional[list[str]] = None,
) -> dict:
    """
    Hızlı GET isteği — tarayıcı açmadan curl_cffi ile sayfa indir.

    Statik sayfalar, JSON API'ler ve hafif JS gerektirmeyen siteler için idealdir.
    Gerçek Chrome TLS parmak izi taklit ederek basit anti-bot korumalarını geçer.

    :param url: Hedef URL.
    :param headers: Ekstra HTTP başlıkları.
    :param proxy: Proxy adresi (örn. "http://user:pass@host:port").
    :param timeout: Saniye cinsinden zaman aşımı.
    :param impersonate: Taklit edilecek tarayıcı ("chrome", "firefox", "safari").
    :param stealthy_headers: Gerçekçi tarayıcı başlıkları oluştur (varsayılan: True).
    :param css_queries: Yanıttan veri çekecek CSS seçici listesi (örn. ["h1::text", ".price::text"]).
    :param xpath_queries: Yanıttan veri çekecek XPath ifadesi listesi.
    :return: status, url, title, html, text, links, headers, css_results, xpath_results.
    """
    from scrapling.fetchers import Fetcher

    kwargs: dict = {"impersonate": impersonate, "stealthy_headers": stealthy_headers}
    if headers:
        kwargs["headers"] = headers
    if proxy:
        kwargs["proxy"] = proxy
    if timeout is not None:
        kwargs["timeout"] = timeout

    response = Fetcher.get(url, **kwargs)
    return _build_result(response, css_queries, xpath_queries)


@mcp.tool()
def fetcher_post(
    url: str,
    json_data: Optional[dict] = None,
    form_data: Optional[dict] = None,
    headers: Optional[dict] = None,
    proxy: Optional[str] = None,
    timeout: Optional[float] = None,
    impersonate: str = "chrome",
    stealthy_headers: bool = True,
    css_queries: Optional[list[str]] = None,
    xpath_queries: Optional[list[str]] = None,
) -> dict:
    """
    Hızlı POST isteği — curl_cffi ile form veya JSON gönder.

    API endpoint'lerine, login formlarına ve veri gönderimi gerektiren sayfalara uygundur.

    :param url: Hedef URL.
    :param json_data: JSON body olarak gönderilecek dict.
    :param form_data: Form verisi olarak gönderilecek dict.
    :param headers: Ekstra HTTP başlıkları.
    :param proxy: Proxy adresi.
    :param timeout: Saniye cinsinden zaman aşımı.
    :param impersonate: Taklit edilecek tarayıcı.
    :param stealthy_headers: Gerçekçi tarayıcı başlıkları oluştur.
    :param css_queries: Yanıttan veri çekecek CSS seçici listesi.
    :param xpath_queries: Yanıttan veri çekecek XPath ifadesi listesi.
    :return: status, url, title, html, text, links, headers, css_results, xpath_results.
    """
    from scrapling.fetchers import Fetcher

    kwargs: dict = {"impersonate": impersonate, "stealthy_headers": stealthy_headers}
    if json_data:
        kwargs["json"] = json_data
    if form_data:
        kwargs["data"] = form_data
    if headers:
        kwargs["headers"] = headers
    if proxy:
        kwargs["proxy"] = proxy
    if timeout is not None:
        kwargs["timeout"] = timeout

    response = Fetcher.post(url, **kwargs)
    return _build_result(response, css_queries, xpath_queries)


# ─── STEALTHY FETCHER (Chromium anti-bot) ────────────────────────────────────

@mcp.tool()
def stealthy_fetch(
    url: str,
    headless: bool = True,
    disable_resources: bool = False,
    block_ads: bool = False,
    network_idle: bool = False,
    timeout: int = 30000,
    wait: Optional[int] = None,
    wait_selector: Optional[str] = None,
    solve_cloudflare: bool = False,
    proxy: Optional[str] = None,
    useragent: Optional[str] = None,
    google_search: bool = True,
    extra_headers: Optional[dict] = None,
    css_queries: Optional[list[str]] = None,
    xpath_queries: Optional[list[str]] = None,
) -> dict:
    """
    Gizli Chromium taraması — neredeyse tüm anti-bot korumaları ve Cloudflare'i geçer.

    Gerçek bir Chromium tarayıcısı başlatır; canvas parmak izi, WebRTC sızıntısı ve
    fingerprinting korumalarını otomatik olarak uygular. Cloudflare Turnstile/Interstitial
    çözümü için solve_cloudflare=True kullanın.

    :param url: Hedef URL.
    :param headless: Tarayıcıyı gizli (headless) çalıştır (varsayılan: True).
    :param disable_resources: Görsel/font/medya isteklerini iptal et (hız için).
    :param block_ads: ~3.500 reklam/izleme domainini engelle.
    :param network_idle: Ağ bağlantısı kesilene kadar bekle.
    :param timeout: Tüm işlemler için milisaniye cinsinden zaman aşımı (varsayılan: 30000).
    :param wait: Sayfa yüklendikten sonra milisaniye cinsinden ekstra bekleme süresi.
    :param wait_selector: Belirtilen CSS seçici yüklenene kadar bekle.
    :param solve_cloudflare: Cloudflare Turnstile/Interstitial meydan okumalarını çöz.
    :param proxy: Proxy adresi.
    :param useragent: Özel kullanıcı ajanı dizesi.
    :param google_search: Google referer başlığı ekle (varsayılan: True).
    :param extra_headers: Eklenecek ek HTTP başlıkları.
    :param css_queries: Yanıttan veri çekecek CSS seçici listesi.
    :param xpath_queries: Yanıttan veri çekecek XPath ifadesi listesi.
    :return: status, url, title, html, text, links, headers, css_results, xpath_results.
    """
    from scrapling.fetchers import StealthyFetcher

    kwargs: dict = {
        "headless": headless,
        "disable_resources": disable_resources,
        "block_ads": block_ads,
        "network_idle": network_idle,
        "timeout": timeout,
        "solve_cloudflare": solve_cloudflare,
        "google_search": google_search,
    }
    if wait is not None:
        kwargs["wait"] = wait
    if wait_selector:
        kwargs["wait_selector"] = wait_selector
    if proxy:
        kwargs["proxy"] = proxy
    if useragent:
        kwargs["useragent"] = useragent
    if extra_headers:
        kwargs["extra_headers"] = extra_headers

    response = StealthyFetcher.fetch(url, **kwargs)
    return _build_result(response, css_queries, xpath_queries)


# ─── DYNAMIC FETCHER (Playwright tam JS desteği) ─────────────────────────────

@mcp.tool()
def dynamic_fetch(
    url: str,
    headless: bool = True,
    disable_resources: bool = False,
    block_ads: bool = False,
    network_idle: bool = False,
    load_dom: bool = True,
    timeout: int = 30000,
    wait: Optional[int] = None,
    wait_selector: Optional[str] = None,
    proxy: Optional[str] = None,
    useragent: Optional[str] = None,
    google_search: bool = True,
    extra_headers: Optional[dict] = None,
    css_queries: Optional[list[str]] = None,
    xpath_queries: Optional[list[str]] = None,
) -> dict:
    """
    Dinamik Playwright taraması — tam JavaScript yürütme ile sayfa yükle.

    React, Vue, Angular gibi SPA'lar ve dinamik içerik yükleyen siteler için idealdir.
    Stealthy modundan farklı olarak canvas/WebRTC koruması yoktur; ama daha hafiftir.

    :param url: Hedef URL.
    :param headless: Tarayıcıyı gizli çalıştır (varsayılan: True).
    :param disable_resources: Görsel/font/medya isteklerini iptal et (hız için).
    :param block_ads: Reklam/izleme domainlerini engelle.
    :param network_idle: Ağ bağlantısı kesilene kadar bekle.
    :param load_dom: DOM ve JavaScript tam yüklenene kadar bekle (varsayılan: True).
    :param timeout: Milisaniye cinsinden zaman aşımı (varsayılan: 30000).
    :param wait: Sayfa yüklendikten sonra milisaniye cinsinden ekstra bekleme.
    :param wait_selector: Belirtilen CSS seçici yüklenene kadar bekle.
    :param proxy: Proxy adresi.
    :param useragent: Özel kullanıcı ajanı dizesi.
    :param google_search: Google referer başlığı ekle (varsayılan: True).
    :param extra_headers: Eklenecek ek HTTP başlıkları.
    :param css_queries: Yanıttan veri çekecek CSS seçici listesi.
    :param xpath_queries: Yanıttan veri çekecek XPath ifadesi listesi.
    :return: status, url, title, html, text, links, headers, css_results, xpath_results.
    """
    from scrapling.fetchers import DynamicFetcher

    kwargs: dict = {
        "headless": headless,
        "disable_resources": disable_resources,
        "block_ads": block_ads,
        "network_idle": network_idle,
        "load_dom": load_dom,
        "timeout": timeout,
        "google_search": google_search,
    }
    if wait is not None:
        kwargs["wait"] = wait
    if wait_selector:
        kwargs["wait_selector"] = wait_selector
    if proxy:
        kwargs["proxy"] = proxy
    if useragent:
        kwargs["useragent"] = useragent
    if extra_headers:
        kwargs["extra_headers"] = extra_headers

    response = DynamicFetcher.fetch(url, **kwargs)
    return _build_result(response, css_queries, xpath_queries)


# ─── SPIDER (çok sayfalı otomatik crawl) ─────────────────────────────────────

@mcp.tool()
def spider_crawl(
    start_urls: list[str],
    item_selectors: dict[str, str],
    link_selector: str = "",
    allowed_domains: Optional[list[str]] = None,
    concurrent_requests: int = 4,
    max_items: int = 200,
    fetcher_type: str = "fetcher",
    proxy: Optional[str] = None,
    download_delay: float = 0.0,
) -> dict:
    """
    Çok sayfalı otomatik örümcek — link takip ederek birden fazla sayfayı tara.

    Sayfalama, liste sayfaları veya tüm site taraması için idealdir.
    Spider, link_selector ile bulduğu linkleri otomatik takip eder.

    :param start_urls: Taramanın başlayacağı URL listesi.
    :param item_selectors: Çekilecek alanlar: {"alan_adi": "css_seçici"}.
        Örn: {"başlık": "h1::text", "fiyat": ".price::text", "link": "a.product::attr(href)"}.
    :param link_selector: Takip edilecek linkleri seçen CSS seçici.
        Örn: ".pagination .next a" veya ".next-page::attr(href)".
        ::attr(href) eklemezseniz otomatik eklenir.
    :param allowed_domains: İzin verilen domain listesi (boşsa kısıtsız).
    :param concurrent_requests: Eşzamanlı istek sayısı (varsayılan: 4).
    :param max_items: Toplanacak maksimum öğe sayısı (varsayılan: 200).
    :param fetcher_type: Kullanılacak fetcher: "fetcher" | "stealthy" | "dynamic".
    :param proxy: Tüm istekler için proxy adresi.
    :param download_delay: İstekler arası bekleme süresi (saniye).
    :return: items listesi ve crawl istatistikleri.
    """
    from scrapling.spiders import Spider, Response
    from scrapling.spiders.request import Request

    _item_selectors = dict(item_selectors)
    _link_selector = link_selector
    _max_items = max_items
    _fetcher_type = fetcher_type
    _proxy = proxy

    class DynamicSpider(Spider):
        name = "mcp_spider"
        robots_txt_obey = False
        download_delay = 0.0

        def configure_sessions(self, manager):
            if _fetcher_type == "stealthy":
                from scrapling.fetchers import StealthySession
                session_kwargs: dict = {"headless": True}
                if _proxy:
                    session_kwargs["proxy"] = _proxy
                manager.add("default", StealthySession(**session_kwargs))
            elif _fetcher_type == "dynamic":
                from scrapling.fetchers import DynamicSession
                session_kwargs = {"headless": True}
                if _proxy:
                    session_kwargs["proxy"] = _proxy
                manager.add("default", DynamicSession(**session_kwargs))
            else:
                from scrapling.fetchers import FetcherSession
                session_kwargs = {"impersonate": "chrome", "stealthy_headers": True}
                if _proxy:
                    session_kwargs["proxy"] = _proxy
                manager.add("default", FetcherSession(**session_kwargs))

        async def parse(self, response: Response):
            # Öğe çıkar
            item: dict = {}
            for field, selector in _item_selectors.items():
                try:
                    results = response.css(selector).getall()
                    item[field] = [str(r) for r in results] if len(results) > 1 else (str(results[0]) if results else None)
                except Exception:
                    item[field] = None

            if any(v is not None for v in item.values()):
                yield item

            # Link takibi
            if _link_selector:
                selector_for_links = _link_selector
                if "::attr" not in selector_for_links and "::text" not in selector_for_links:
                    selector_for_links = selector_for_links + "::attr(href)"
                try:
                    hrefs = response.css(selector_for_links).getall()
                    for href in hrefs:
                        if href:
                            yield response.follow(str(href))
                except Exception:
                    pass

    DynamicSpider.start_urls = list(start_urls)
    DynamicSpider.concurrent_requests = concurrent_requests
    DynamicSpider.download_delay = download_delay
    if allowed_domains:
        DynamicSpider.allowed_domains = set(allowed_domains)

    spider = DynamicSpider()
    result = spider.start()

    items = list(result.items)
    if _max_items and len(items) > _max_items:
        items = items[:_max_items]

    return {
        "items": items,
        "total_items": len(result.items),
        "returned_items": len(items),
        "paused": result.paused,
        "stats": result.stats.to_dict(),
    }


# ─── PARSE HTML (ham HTML'i ayrıştır) ────────────────────────────────────────

@mcp.tool()
def parse_html(
    html: str,
    url: str = "https://example.com",
    css_queries: Optional[list[str]] = None,
    xpath_queries: Optional[list[str]] = None,
) -> dict:
    """
    Ham HTML içeriğini Scrapling Selector ile ayrıştır.

    Zaten indirilmiş bir HTML'den CSS/XPath ile veri çekmek için kullanılır.
    Yeniden HTTP isteği yapmaz; yalnızca ayrıştırma gerçekleştirir.

    :param html: Ayrıştırılacak HTML içeriği.
    :param url: Göreli URL'leri çözmek için temel URL (varsayılan: https://example.com).
    :param css_queries: Uygulanacak CSS seçici listesi (örn. ["h1::text", "a::attr(href)"]).
    :param xpath_queries: Uygulanacak XPath ifadesi listesi.
    :return: title, links, text, css_results, xpath_results.
    """
    from scrapling.parser import Selector

    selector = Selector(content=html.encode("utf-8"), url=url)

    title = None
    try:
        t = selector.css("title::text").get()
        title = str(t) if t else None
    except Exception:
        pass

    links: list[str] = []
    try:
        for a in selector.css("a")[:100]:
            href = a.attrib.get("href", "")
            if href:
                links.append(str(href))
    except Exception:
        pass

    text = ""
    try:
        text = str(selector.get_all_text())[:8000]
    except Exception:
        pass

    base: dict = {"title": title, "links": links, "text": text, "url": url}
    return _apply_queries(selector, base, css_queries or [], xpath_queries or [])


if __name__ == "__main__":
    mcp.run()
