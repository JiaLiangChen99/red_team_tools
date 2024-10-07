from dataclasses import dataclass

@dataclass
class Proxy:
    port: int
    clash_conf_path: str
    server_name: str

clash_proxies = []
