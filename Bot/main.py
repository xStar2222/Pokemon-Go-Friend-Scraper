from discord_webhook import DiscordWebhook, DiscordEmbed
import requests
import time
import re

def extract_numbers(text):
    numbers = re.findall(r'\d{4} \d{4} \d{4}', text)
    return numbers

url = 'https://www.reddit.com/r/PokemonGoFriends/new/.json'
webhook_url = 'https://discord.com/api/webhooks/1107140365577879644/opXwKiXg8qJcUAeO6OwvL2vO0X4NMDwLLqR_nVCqRB20a0c86lbWASiRExfmJpKdNtjG'

most_recent_post = None

while True:
    response = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})
    data = response.json()

    for post in data['data']['children']:
        if post['data'].get('link_flair_text') == 'Gifts &amp; EXP grind':
            title = post['data']['title']
            selftext = post['data']['selftext']
            poster = post['data']['author']

            if most_recent_post is None or post['data']['created_utc'] > most_recent_post['data']['created_utc']:
                most_recent_post = post

                webhook = DiscordWebhook(url=webhook_url)
                embed = DiscordEmbed()

                embed.set_title("**New r/PokemonGoFriends Post Detected**")
                embed.set_description(f"**Title:** {title}\n\n**Description:** {selftext}\n\n **Poster:** u/{poster}")
                embed.set_color(0x00d5ff)
                embed.set_timestamp()

                webhook.add_embed(embed)
                webhook.execute()

                
                numbers = extract_numbers(title + ' ' + selftext)
                if numbers:
                    numbers_message = f" {', '.join(numbers)}"
                    requests.post(webhook_url, json={'content': numbers_message})

                break

    print("sleeping")
    time.sleep(60)  
