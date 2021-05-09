import asyncio
import json
import logging
from math import floor
import os
import requests
from requests.auth import HTTPBasicAuth
import sys
from time import sleep


FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def get_ip_addr():
    ip_addr = requests.get('https://api.ipify.org?format=json').json()['ip']
    set_ip_cache(ip_addr)
    return ip_addr

def opendns_needs_updating():
    try:
        cached_ip = get_ip_cache()
        return (cached_ip == None or cached_ip != get_ip_addr())
    except json.decoder.JSONDecodeError:
        return True

def update_opendns(settings):
    ip_addr = get_ip_addr()
    endpoint= f"https://updates.opendns.com/nic/update?hostname={ip_addr}"
    response = requests.get(endpoint, auth=(settings['username'], settings['token']))
    return (response.status_code <= 299)

def get_ip_cache():
    try:
        with open('cache.json', 'r') as cache:
            return json.loads(cache.read())['ip']
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        return None

def set_ip_cache(ip):
    with open('cache.json', 'w') as cache:
        cache.write(json.dumps({"ip": ip}))

async def run_forever():
    logger.info('Setting credentials from environment...')
    credentials = {
        "username": os.environ['username'],
        "token": os.environ['token']
    }
    run_delay = 1800 if 'delay' not in os.environ else int(os.environ['delay'])
    while True:
        logger.info(f"Checking current IP configuration...delay set to {floor(run_delay/60)} minutes.")
        if opendns_needs_updating():
            logger.info('Updating OpenDNS...')
            if not update_opendns(credentials):
                logger.error('Failed to update OpenDNS')
            else:
                logger.info('Successfully updated OpenDNS')
        else:
            logger.info("Skipping update. OpenDNS already reflects the latest address.")
        logger.info('Sleeping...')
        sleep(run_delay)

async def main():
    if 'username' not in os.environ or 'token' not in os.environ:
        logger.critical('Missing environment variables.')
        sys.exit(1)
    logger.info('Starting main loop...')
    main_task = asyncio.create_task(
        run_forever()
    )
    await main_task


if __name__ == "__main__":
    asyncio.run(main())
