"""Render the illustrative Appopty report pages shown on the homepage (synthetic Riverside Technology Group data).

Usage: python build/make_report_previews.py <repo root> <work folder>
Writes public/img/hero/*.webp and public/img/gallery/*.webp. Needs Playwright (Chromium) and Pillow.
"""
import sys
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright

repo = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2]).resolve()
work.mkdir(parents=True, exist_ok=True)
fonts = (repo / "public/fonts").as_uri()

MARK = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="{s}" height="{s}"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fb7185"/><stop offset="1" stop-color="#e11d48"/></linearGradient></defs><path d="M16 32 C30 32 30 12 48 12 M16 32 H48 M16 32 C30 32 30 52 48 52" fill="none" stroke="#fb7185" stroke-width="5" stroke-linecap="round"/><circle cx="15" cy="32" r="10" fill="url(#g)"/><circle cx="50" cy="12" r="7" fill="#f43f5e"/><circle cx="50" cy="32" r="7" fill="#f43f5e"/><circle cx="50" cy="52" r="7" fill="#f43f5e"/></svg>"""

CSS = """
@font-face{font-family:Inter;src:url(FONTS/inter-latin-var.woff2);font-weight:100 900}
@font-face{font-family:Poppins;src:url(FONTS/poppins-latin-500.woff2);font-weight:500}
@font-face{font-family:Poppins;src:url(FONTS/poppins-latin-600.woff2);font-weight:600}
*{box-sizing:border-box}
body{margin:0;font:400 13px/1.45 Inter,sans-serif;color:#2a1018;background:#fff}
.page{display:flex;flex-direction:column;padding:38px 46px 26px;background:#fff;overflow:hidden}
.hdr{display:flex;justify-content:space-between;align-items:center;padding-bottom:12px;border-bottom:2px solid #e11d48}
.logo{display:flex;align-items:center;gap:8px;font:600 19px/1 Poppins;color:#2a0c14}
.hdr .ctx{font-size:11.5px;color:#7d5a63;letter-spacing:.04em}
.pill{font:600 10px/1 Inter;letter-spacing:.12em;text-transform:uppercase;color:#9f1239;border:1.5px solid #fb7185;border-radius:5px;padding:7px 11px;background:#fff1f3}
.kicker{font:600 11px/1 Inter;letter-spacing:.16em;text-transform:uppercase;color:#be123c;margin:22px 0 8px}
h1{font:600 27px/1.15 Poppins;color:#210e15;margin:0}
h2{font:600 15px/1.2 Poppins;color:#210e15;margin:20px 0 8px}
.lead{color:#5e3540;margin-top:8px;max-width:760px;font-size:13.5px}
.ftr{margin-top:auto;padding-top:10px;border-top:1px solid #f0d9de;display:flex;justify-content:space-between;font-size:10.5px;color:#7d5a63}
.tiles{display:grid;gap:12px;margin-top:16px}
.tile{border:1px solid #f0d9de;border-radius:8px;padding:12px 14px;background:#fffafb}
.tile b{display:block;font:600 26px/1 Poppins;color:#2a0c14}
.tile span{display:block;margin-top:6px;font-size:11.5px;color:#5e3540}
.tile.warn b{color:#1d4ed8}.tile.bad b{color:#b42318}
table{width:100%;border-collapse:collapse;font-size:12px}
th{text-align:left;font:600 10.5px/1.2 Inter;letter-spacing:.08em;text-transform:uppercase;color:#5e3540;background:#fcf0f2;padding:8px 10px;border-bottom:1px solid #ecc9d0}
td{padding:8px 10px;border-bottom:1px solid #f4e3e6;vertical-align:top}
.mono{font-family:Consolas,"Cascadia Mono",monospace;font-size:11.5px}
.b{display:inline-block;font:700 9.5px/1 Inter;letter-spacing:.07em;text-transform:uppercase;color:#fff;border-radius:4px;padding:4px 7px;white-space:nowrap}
.high{background:#b42318}.med{background:#b9650f}.low{background:#6b7280}.ok{background:#18794e}.ver{background:#fff;color:#1d4ed8;border:1px solid #6b8fe8}.plain{background:#fff;color:#5e3540;border:1px solid #dcbcc3}
.call{border-left:5px solid #e11d48;background:#fff1f3;padding:11px 14px;border-radius:0 6px 6px 0;margin-top:16px}
.call b{display:block;font:600 11px/1.2 Inter;letter-spacing:.08em;text-transform:uppercase;color:#9f1239;margin-bottom:3px}
.cols{display:grid;gap:26px}
.muted{color:#7d5a63}
.bar{display:flex;height:16px;border-radius:4px;overflow:hidden;background:#fcf0f2}
.bar i{display:block;height:100%}
.legend{display:flex;gap:16px;font-size:11px;color:#5e3540;margin-top:10px}
.legend i{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:5px;vertical-align:-1px}
.cap{position:relative;height:14px;background:#fcf0f2;border-radius:3px;overflow:hidden;min-width:170px}
.cap i{position:absolute;left:0;top:0;bottom:0;border-radius:3px}
/* dependency map */
.map{display:flex;align-items:stretch;gap:0;margin-top:14px}
.stage{flex:1;display:flex;flex-direction:column;gap:8px;justify-content:center}
.stage h3{font:600 10px/1.2 Inter;letter-spacing:.1em;text-transform:uppercase;color:#7d5a63;margin:0 0 2px;text-align:center}
.node{border:1.5px solid #ecc9d0;border-radius:8px;background:#fffafb;padding:9px 10px;text-align:center}
.node b{display:block;font:600 12px/1.25 Inter;color:#210e15}
.node span{display:block;font-size:10.5px;color:#5e3540;margin-top:2px}
.node.key{border-color:#e11d48;background:#fff1f3}
.node.flag{border-color:#b42318;border-style:dashed}
.arrow{flex:0 0 34px;display:flex;align-items:center;justify-content:center;color:#be123c;font:600 20px/1 Inter}
""".replace("FONTS", fonts)


def chrome(body, w, h, page_no, ctx="Application Delivery Report · Riverside Technology Group"):
    return f"""<!doctype html><meta charset="utf-8"><style>{CSS}.page{{width:{w}px;height:{h}px}}</style>
<div class="page"><div class="hdr"><div class="logo">{MARK.format(s=24)}Appopty</div><div class="ctx">{ctx}</div></div>
{body}
<div class="ftr"><span>Illustrative preview · synthetic data · Riverside Technology Group is a fictional organisation</span><span>{page_no}</span></div></div>"""


def rows(data):
    return "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in data)


def head(cols):
    return "<tr>" + "".join(f"<th>{c}</th>" for c in cols) + "</tr>"


def tiles(items, cols=4):
    return f'<div class="tiles" style="grid-template-columns:repeat({cols},1fr)">' + "".join(
        f'<div class="tile {cls}"><b>{n}</b><span>{t}</span></div>' for n, t, cls in items) + "</div>"


def observations(items):
    return "<h2>Observations</h2><table>" + head(["Finding", "Where", "Severity"]) + rows(items) + "</table>"


B = lambda cls, text: f'<span class="b {cls}">{text}</span>'
M = lambda t: f'<span class="mono">{t}</span>'
HIGH, MED, LOW, VER, OK = B("high", "High"), B("med", "Medium"), B("low", "Low"), B("ver", "Verify"), B("ok", "No issue")

# Findings per area: high, medium, low, needs verification. The pages below list exactly these.
COUNTS = [
    ("Controllers and load balancing", 0, 1, 1, 0),
    ("Certificates and TLS", 1, 1, 0, 0),
    ("Remote access gateways", 0, 1, 0, 1),
    ("Web application firewall", 0, 1, 1, 0),
    ("Cloud gateways and Kubernetes ingress", 0, 1, 0, 1),
]
tot = [sum(c[i] for c in COUNTS) for i in (1, 2, 3, 4)]

# ---------------------------------------------------------------- portrait pages (A4 at 96 dpi)
PW, PH = 794, 1123

cover = f"""<!doctype html><meta charset="utf-8"><style>{CSS}
.page{{width:{PW}px;height:{PH}px;padding:0}}
.top{{padding:64px 62px 0;display:flex;justify-content:space-between;align-items:center}}
.top .logo{{font-size:30px;gap:12px}}
.band{{margin-top:190px;background:#210e15;color:#fff;padding:44px 62px 48px;border-bottom:6px solid #f43f5e}}
.band .k{{font:600 11.5px/1 Inter;letter-spacing:.18em;text-transform:uppercase;color:#fda4af;border-top:3px solid #f43f5e;display:inline-block;padding-top:12px}}
.band h1{{color:#fff;font-size:40px;margin-top:20px}}
.band p{{margin:10px 0 0;font-size:16px;color:#f3dfe3}}
.band p.o{{font:600 17px/1.2 Poppins;color:#fff;margin-top:14px}}
.meta{{margin:auto 62px 70px}}
.meta td{{padding:10px 0;font-size:12.5px;border-bottom:1px solid #f4e3e6}}
.meta td:first-child{{width:170px;font-weight:600;color:#4d2832}}
</style><div class="page"><div class="top"><div class="logo">{MARK.format(s=40)}Appopty</div><span class="pill">Illustrative preview · synthetic data</span></div>
<div class="band"><span class="k">Application delivery report</span><h1>Riverside Technology Group</h1><p class="o">Application delivery estate</p><p>Controllers, load balancing, remote access, web application firewall, cloud gateways and Kubernetes ingress</p></div>
<div class="meta"><table>{rows([
    ["Organisation", "Riverside Technology Group"],
    ["Document", "Application Delivery Report"],
    ["Scope", "4 controllers, 2 cloud application gateways and 1 Kubernetes cluster"],
    ["Evidence collected", "20 Oct 2026, read-only access to each platform"],
    ["Report sections", "Six sections, with audit evidence and coverage"],
    ["Review status", "Not reviewed: illustrative layout"],
    ["Classification", "Public preview: synthetic data, fictional organisation"],
])}</table></div></div>"""

UNIT = 34
bar_rows = "".join(
    f"""<tr><td style="width:250px">{n}</td><td><div class="bar" style="width:{(h + m + l + v) * UNIT}px">
<i class="high" style="width:{h * UNIT}px"></i><i class="med" style="width:{m * UNIT}px"></i><i class="low" style="width:{l * UNIT}px"></i><i style="width:{v * UNIT}px;background:#a9bff5"></i></div></td>
<td style="width:44px;text-align:right;font-weight:600">{h + m + l + v}</td></tr>"""
    for n, h, m, l, v in COUNTS)

overview = chrome(f"""
<p class="kicker">Section 1</p><h1>Delivery estate at a glance</h1>
{tiles([("38", "virtual servers on 4 controllers", ""), ("23", "applications identified", ""), (str(tot[0] + tot[1] + tot[2]), "findings in total", "bad"), (str(tot[3]), "items needing verification", "warn")])}
<h2>What delivers your applications</h2>
<table>{head(["Platform", "Role", "In scope", "Publishes"])}{rows([
    [M("ns-hq-01, ns-hq-02"), "NetScaler pair: load balancing, gateway, WAF", "24 virtual servers", "14 applications"],
    [M("f5-dc-01, f5-dc-02"), "F5 pair: load balancing", "14 virtual servers", "6 applications"],
    [M("agw-prod-01, agw-web-01"), "Cloud application gateways", "9 listeners", "2 applications"],
    [M("aks-prod"), "Kubernetes ingress controller", "14 ingress hosts", "1 application"],
])}</table>
<h2>Findings by area</h2>
<table>{bar_rows}</table>
<div class="legend"><span><i class="high"></i>High</span><span><i class="med"></i>Medium</span><span><i class="low"></i>Low</span><span><i style="background:#a9bff5"></i>Needs verification</span></div>
<h2>Audit evidence and coverage</h2>
<table>{head(["Platform", "Access used", "Collected", "Coverage"])}{rows([
    ["NetScaler pair", "Read-only account", "20 Oct 2026", B("ok", "Complete")],
    ["F5 pair", "Read-only account", "20 Oct 2026", B("ok", "Complete")],
    ["Cloud application gateways", "Read-only role, 1 subscription", "20 Oct 2026", B("ok", "Complete")],
    ["Kubernetes ingress", "Read-only access, 1 of 2 clusters", "20 Oct 2026", B("ver", "Partial")],
])}</table>
<p class="muted" style="margin-top:8px;font-size:11.5px">Where access was not granted, the related sections are marked as needing verification and are not reported as complete.</p>""", PW, PH, "Page 3")

sheet = chrome(f"""
<p class="kicker">Section 7 · Application dependency mapping</p><h1>Application sheet: Staff Portal</h1>
<p class="lead">Everything between the address staff type and the servers that answer, read from the controllers.</p>
{tiles([("1", "public address", ""), ("4", "web servers behind it", ""), ("1", "finding that needs action", "bad")], 3)}
<h2>Delivery path</h2>
<table>{rows([
    ["<b>Name</b>", M("portal.riverside.example")],
    ["<b>Virtual server</b>", M("vs-portal-443") + " on " + M("ns-hq-01") + ", " + M("203.0.113.20:443")],
    ["<b>Certificate</b>", M("portal.riverside.example") + ", expires 10 Nov 2026 " + B("high", "21 days")],
    ["<b>Web application firewall</b>", "Profile " + M("waf-portal") + ", blocking"],
    ["<b>Load balancing</b>", "Least connection, cookie persistence"],
    ["<b>Service group</b>", M("sg-portal-web") + ", 4 members, health check " + M("HTTPS /health")],
])}</table>
<h2>Servers</h2>
<table>{head(["Server", "Address", "Port", "State"])}{rows([
    [M("web-portal-01"), M("10.20.30.11"), "8443", B("ok", "Up")],
    [M("web-portal-02"), M("10.20.30.12"), "8443", B("ok", "Up")],
    [M("web-portal-03"), M("10.20.30.13"), "8443", B("ok", "Up")],
    [M("web-portal-04"), M("10.20.30.14"), "8443", B("plain", "Disabled")],
])}</table>
<h2>Depends on</h2>
<table>{head(["Dependency", "Delivered by", "Shared with"])}{rows([
    ["Sign-in", M("vs-sso-443") + " on " + M("ns-hq-01"), "9 other applications"],
    ["Database", M("vs-sql-portal") + " on " + M("f5-dc-01"), "Intranet"],
])}</table>
<div class="call"><b>Finding</b>The certificate on this virtual server expires in 21 days. Renew it and bind the new certificate before 10 Nov 2026.</div>""", PW, PH, "Page 41")

# ---------------------------------------------------------------- landscape figures
LW, LH = 1200, 860

adc = chrome(f"""
<p class="kicker">Section 2 · Application delivery controllers and load balancers</p><h1>Virtual servers and pools</h1>
{tiles([("4", "controllers in 2 pairs", ""), ("38", "virtual servers", ""), ("41", "pools with 96 servers", ""), ("2", "virtual servers with a single server behind them", "bad")])}
<h2>Virtual servers</h2>
<table>{head(["Virtual server", "Controller", "Address", "Method", "Pool", "Servers up", "Review"])}{rows([
    [M("vs-portal-443"), M("ns-hq-01"), M("203.0.113.20:443"), "Least connection", M("sg-portal-web"), "3 of 4", OK],
    [M("vs-intranet-443"), M("ns-hq-01"), M("10.20.0.40:443"), "Round robin", M("sg-intranet"), "2 of 2", OK],
    [M("vs-finance-443"), M("ns-hq-01"), M("10.20.0.52:443"), "Least connection", M("sg-finance"), "1 of 1", B("med", "Single server")],
    [M("vs-api-443"), M("f5-dc-01"), M("203.0.113.31:443"), "Least connection", M("pool-api"), "6 of 6", OK],
    [M("vs-sql-portal"), M("f5-dc-01"), M("10.30.0.15:1433"), "Round robin", M("pool-sql-portal"), "2 of 2", OK],
    [M("vs-print-9100"), M("f5-dc-01"), M("10.30.0.60:9100"), "Round robin", M("pool-print"), "1 of 1", B("med", "Single server")],
])}</table>
<p class="muted" style="margin-top:6px;font-size:11px">Showing 6 of 38 virtual servers.</p>
{observations([
    ["Two virtual servers have a single server behind them, so there is nothing to fail over to", M("vs-finance-443, vs-print-9100"), MED],
    ["Five pools are not used by any virtual server", M("ns-hq-01, f5-dc-01"), LOW],
])}""", LW, LH, "Page 8")


def cap(days):
    pct = min(days / 365 * 100, 100)
    colour = "#b42318" if days <= 30 else ("#d08a1c" if days <= 90 else "#c98a96")
    return f'<div class="cap"><i style="width:{pct}%;background:{colour}"></i></div>'


tls = chrome(f"""
<p class="kicker">Section 3 · Certificates and TLS</p><h1>Certificate expiry and TLS settings</h1>
{tiles([("29", "certificates bound to virtual servers", ""), ("1", "certificate expires within 30 days", "bad"), ("3", "certificates expire within 90 days", ""), ("4", "virtual servers still accept TLS 1.0 or 1.1", "bad")])}
<div class="cols" style="grid-template-columns:1.25fr 1fr;margin-top:2px">
<div><h2>Certificates, soonest first</h2>
<table>{head(["Certificate", "Bound to", "Expires", "Days left", ""])}{rows([
    [M("portal.riverside.example"), M("vs-portal-443"), "10 Nov 2026", "21", cap(21)],
    [M("vpn.riverside.example"), M("gw-remote-443"), "02 Jan 2027", "74", cap(74)],
    [M("api.riverside.example"), M("vs-api-443"), "15 Jan 2027", "87", cap(87)],
    [M("*.intranet.riverside.example"), "6 virtual servers", "30 Apr 2027", "192", cap(192)],
    [M("www.riverside.example"), M("agw-web-01"), "18 Aug 2027", "302", cap(302)],
])}</table>
<p class="muted" style="margin-top:6px;font-size:11px">Showing 5 of 29 certificates.</p></div>
<div><h2>TLS versions accepted</h2>
<table>{head(["Setting", "Virtual servers", "Review"])}{rows([
    ["TLS 1.2 and 1.3 only", "27", OK],
    ["TLS 1.2 only", "7", OK],
    ["TLS 1.0 or 1.1 also accepted", "4", B("med", "Old protocols")],
])}</table></div></div>
{observations([
    ["A certificate on an internet-facing virtual server expires in 21 days", M("vs-portal-443"), HIGH],
    ["Four virtual servers still accept TLS 1.0 or 1.1", M("ns-hq-01"), MED],
])}""", LW, LH, "Page 14")

gateway = chrome(f"""
<p class="kicker">Section 4 · Remote access gateways</p><h1>Gateways, sign-in and sessions</h1>
{tiles([("2", "remote access gateways", ""), ("3", "sign-in policies", ""), ("11", "published resources", ""), ("1", "gateway with a single sign-in factor", "warn")])}
<h2>Gateways</h2>
<table>{head(["Gateway", "Controller", "Address", "Sign-in", "Session timeout", "Published resources"])}{rows([
    [M("gw-remote-443"), M("ns-hq-01"), M("203.0.113.25:443"), "Directory password and one-time code", "30 minutes idle", "8"],
    [M("gw-partner-443"), M("ns-hq-01"), M("203.0.113.26:443"), "Directory password only", "Not set", "3"],
])}</table>
<h2>Sign-in policies</h2>
<table>{head(["Policy", "Bound to", "Factor", "Server", "Review"])}{rows([
    [M("pol-ldap-staff"), M("gw-remote-443"), "Directory password", M("ldap-hq"), OK],
    [M("pol-otp-staff"), M("gw-remote-443"), "One-time code", M("radius-otp"), OK],
    [M("pol-ldap-partner"), M("gw-partner-443"), "Directory password", M("ldap-hq"), B("ver", "One factor only")],
])}</table>
{observations([
    ["No idle session timeout is set on the partner gateway", M("gw-partner-443"), MED],
    ["The partner gateway signs users in with one factor. Confirm this is intended", M("gw-partner-443"), VER],
])}""", LW, LH, "Page 20")

waf = chrome(f"""
<p class="kicker">Section 5 · Web application firewall</p><h1>Coverage by application</h1>
{tiles([("9", "internet-facing applications", ""), ("6", "web application firewall profiles", ""), ("2", "internet-facing applications with no profile", "bad"), ("1", "profile that logs but does not block", "")])}
<h2>Internet-facing applications</h2>
<table>{head(["Application", "Published by", "Profile", "Mode", "Signatures", "Review"])}{rows([
    ["Staff Portal", M("vs-portal-443"), M("waf-portal"), "Blocking", "Updated 12 Oct 2026", OK],
    ["Public Website", M("agw-web-01"), "Gateway rule set", "Blocking", "Managed", OK],
    ["Public API", M("vs-api-443"), M("waf-api"), "Log only", "Updated 12 Oct 2026", B("low", "Not blocking")],
    ["Partner Exchange", M("vs-partner-443"), "None", "None", "None", B("med", "No profile")],
    ["Careers", M("vs-careers-443"), "None", "None", "None", B("med", "No profile")],
    ["Remote Access", M("gw-remote-443"), M("waf-gateway"), "Blocking", "Updated 12 Oct 2026", OK],
])}</table>
<p class="muted" style="margin-top:6px;font-size:11px">Showing 6 of 9 applications.</p>
{observations([
    ["Two internet-facing applications are published with no web application firewall profile", "Partner Exchange, Careers", MED],
    ["One profile logs matches but does not block them", M("waf-api"), LOW],
])}""", LW, LH, "Page 25")

cloud = chrome(f"""
<p class="kicker">Section 6 · Cloud application gateways and Kubernetes ingress</p><h1>Listeners, ingress hosts and back ends</h1>
{tiles([("2", "cloud application gateways with 9 listeners", ""), ("14", "ingress hosts on 1 cluster", ""), ("3", "ingress hosts with no TLS", "bad"), ("1", "cluster not read", "warn")])}
<div class="cols" style="grid-template-columns:1fr 1.1fr;margin-top:2px">
<div><h2>Cloud application gateways</h2>
<table>{head(["Gateway", "Listeners", "Back ends", "Firewall"])}{rows([
    [M("agw-web-01"), "5", "2 pools, 6 servers", "Enabled, blocking"],
    [M("agw-prod-01"), "4", "3 pools, 9 servers", "Enabled, blocking"],
])}</table>
<h2>Clusters</h2>
<table>{head(["Cluster", "Ingress controller", "Coverage"])}{rows([
    [M("aks-prod"), "NGINX ingress", B("ok", "Complete")],
    [M("aks-dev"), "Unknown", B("ver", "Access not granted")],
])}</table></div>
<div><h2>Ingress hosts, {M("aks-prod")}</h2>
<table>{head(["Host", "Path", "Service", "TLS", "Review"])}{rows([
    [M("shop.riverside.example"), M("/"), M("shop-web:80"), "Yes", OK],
    [M("shop.riverside.example"), M("/api"), M("shop-api:8080"), "Yes", OK],
    [M("status.riverside.example"), M("/"), M("status:80"), "No", B("med", "No TLS")],
    [M("docs.riverside.example"), M("/"), M("docs:80"), "No", B("med", "No TLS")],
    [M("hooks.riverside.example"), M("/"), M("hooks:9000"), "No", B("med", "No TLS")],
])}</table>
<p class="muted" style="margin-top:6px;font-size:11px">Showing 5 of 14 ingress hosts.</p></div></div>
{observations([
    ["Three ingress hosts are published without TLS", M("aks-prod"), MED],
    ["Read access to one cluster was not granted, so its ingress hosts are not listed", M("aks-dev"), VER],
])}""", LW, LH, "Page 31")


def node(title, sub, cls=""):
    return f'<div class="node {cls}"><b>{title}</b><span>{sub}</span></div>'


ARROW = '<div class="arrow">&rarr;</div>'
depmap = chrome(f"""
<p class="kicker">Section 7 · Application dependency mapping</p><h1>Dependency map: Staff Portal</h1>
<p class="lead">From the address staff type to the servers that answer, and the other services the application relies on.</p>
<div class="map">
<div class="stage"><h3>Name</h3>{node("portal.riverside.example", "203.0.113.20")}</div>{ARROW}
<div class="stage"><h3>Virtual server</h3>{node("vs-portal-443", "ns-hq-01 · HTTPS 443", "key")}{node("Certificate", "expires in 21 days", "flag")}</div>{ARROW}
<div class="stage"><h3>Policies</h3>{node("waf-portal", "web application firewall, blocking")}{node("Sign-in", "vs-sso-443, shared")}</div>{ARROW}
<div class="stage"><h3>Pool</h3>{node("sg-portal-web", "least connection · cookie persistence", "key")}</div>{ARROW}
<div class="stage"><h3>Web servers</h3>{node("web-portal-01", "10.20.30.11 · up")}{node("web-portal-02", "10.20.30.12 · up")}{node("web-portal-03", "10.20.30.13 · up")}{node("web-portal-04", "10.20.30.14 · disabled", "flag")}</div>{ARROW}
<div class="stage"><h3>Database</h3>{node("vs-sql-portal", "f5-dc-01 · 1433", "key")}{node("sql-portal-01", "10.30.40.21 · up")}{node("sql-portal-02", "10.30.40.22 · up")}</div>
</div>
<div class="legend" style="margin-top:14px"><span><i style="background:#fff1f3;border:1.5px solid #e11d48"></i>Delivered by a controller</span><span><i style="background:#fffafb;border:1.5px solid #ecc9d0"></i>Server or policy</span><span><i style="background:#fff;border:1.5px dashed #b42318"></i>Needs attention</span></div>
<div class="cols" style="grid-template-columns:1fr 1fr;margin-top:4px">
<div><h2>Shared with other applications</h2>
<table>{head(["Component", "Also used by"])}{rows([
    [M("vs-sso-443"), "9 other applications"],
    [M("vs-sql-portal"), "Intranet"],
    [M("ns-hq-01, ns-hq-02"), "13 other applications"],
])}</table></div>
<div><h2>What this means</h2>
<table>{rows([
    ["<b>If the sign-in service stops</b>", "Staff Portal and 9 other applications cannot sign users in"],
    ["<b>If the NetScaler pair stops</b>", "14 applications are unreachable"],
    ["<b>Needs attention</b>", "Certificate expires in 21 days. One web server is disabled"],
])}</table></div></div>""", LW, LH, "Page 40")

PAGES = {
    "cover": (cover, PW, PH), "overview": (overview, PW, PH), "sheet": (sheet, PW, PH),
    "controllers": (adc, LW, LH), "certificates": (tls, LW, LH), "gateways": (gateway, LW, LH),
    "waf": (waf, LW, LH), "cloud": (cloud, LW, LH), "dependencies": (depmap, LW, LH),
}

with sync_playwright() as pw:
    browser = pw.chromium.launch()
    for name, (html, w, h) in PAGES.items():
        src = work / f"{name}.html"
        src.write_text(html, encoding="utf-8")
        page = browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=2)
        page.goto(src.as_uri())
        page.evaluate("document.fonts.ready")
        page.wait_for_timeout(250)
        over = page.evaluate("(() => { const p = document.querySelector('.page'); return p.scrollHeight - p.clientHeight; })()")
        if over > 0:
            print("OVERFLOW", name, over)
        page.screenshot(path=str(work / f"{name}.png"), clip={"x": 0, "y": 0, "width": w, "height": h})
        page.close()
    browser.close()


def save(name, out, width):
    im = Image.open(work / f"{name}.png").convert("RGB")
    if width and width < im.width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out, "WEBP", quality=86, method=6)


img = repo / "public/img"
for src, dst in (("cover", "cover"), ("overview", "page2"), ("sheet", "page3")):
    for tag, width in (("480", 480), ("640", 640), ("1200", 1200), ("full", None)):
        save(src, img / f"hero/{dst}-{tag}.webp", width)

# Gallery thumbnails are a legible 3:2 crop from the top left of the page; the lightbox shows all of it.
CROP = {"controllers": 0.62, "certificates": 0.62, "gateways": 0.62, "waf": 0.62, "cloud": 0.62, "dependencies": 0.74}
for name, frac in CROP.items():
    save(name, img / f"gallery/{name}-full.webp", None)
    im = Image.open(work / f"{name}.png").convert("RGB")
    w = round(im.width * frac)
    crop = im.crop((0, 0, w, round(w / 1.5)))
    for width in (800, 1400):
        crop.resize((width, round(width / 1.5)), Image.LANCZOS).save(img / f"gallery/{name}-{width}.webp", "WEBP", quality=86, method=6)
print("report previews written")
