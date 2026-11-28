import ipaddress
import socket
from urllib.parse import urlparse

import requests
import trafilatura


def _is_safe_url(url: str) -> bool:
    """http/https만 허용하고, 내부망·로컬 주소는 막기"""
    p = urlparse(url)
    if p.scheme not in ("http", "https") or not p.hostname:
        return False
    try:
        for info in socket.getaddrinfo(p.hostname, None):
            ip = ipaddress.ip_address(info[4][0])
            if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved:
                return False
    except socket.gaierror:
        return False
    return True


def extract_from_url(url: str) -> str:
    if not _is_safe_url(url):
        raise ValueError("허용되지 않는 주소입니다")
    res = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
    res.raise_for_status()
    if not _is_safe_url(res.url):  # 리다이렉트된 주소도 확인
        raise ValueError("허용되지 않는 주소입니다")
    if res.encoding is None or res.encoding.lower() == "iso-8859-1":
        res.encoding = res.apparent_encoding  # 한글 깨짐 방지
    text = trafilatura.extract(res.text) or ""
    if len(text.strip()) < 100:
        raise ValueError("본문을 읽을 수 없습니다")
    return text