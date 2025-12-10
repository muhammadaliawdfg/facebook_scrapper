# import asyncio
# from apify_client import ApifyClientAsync
# import os
# import dotenv
# dotenv.load_dotenv()
# APIFY_TOKEN = os.getenv("APIFY_TOKEN")  # safer than hardcoding

# async def main():
#     client = ApifyClientAsync(APIFY_TOKEN)

#     # Select your actor
#     actor_client = client.actor("apify/facebook-posts-scraper")  # replace with your actor

#     # Define input parameters
#     run_input = {
#         "startUrls": [
#             {"url": "https://www.facebook.com/OpenAI/"}  # your target page URL
#         ],
#         "resultsLimit": 5,   # optional: limit number of posts
#         "keywords": ["Artificial Intelligence", "AI"]  # optional: filter posts by keywords
#     }

#     # Start the actor and wait for completion
#     run = await actor_client.call(run_input=run_input)
    
#     # # Print the results
#     # print(run['output'])
#     run_id = run['id']
#     print(f"our actor run started with run id : {run_id}")
#     dataset_client = client.dataset(run["defaultDatasetId"])
#     dataset_items = await dataset_client.list_items()

#     items =dataset_items.items
#     for item in items:
#         print(item)

# asyncio.run(main())
import asyncio
from apify_client import ApifyClientAsync
import os
import dotenv
import pandas as pd  # for Excel export

dotenv.load_dotenv()
APIFY_TOKEN = os.getenv("APIFY_TOKEN")  # safer than hardcoding

async def main():
    client = ApifyClientAsync(APIFY_TOKEN)

    # Select your actor
    actor_client = client.actor("apify/facebook-posts-scraper")  # replace with your actor

    # Define input parameters
    run_input = {
        "startUrls": [
            {"url": "https://www.facebook.com/OpenAI/"}  # your target page URL
        ],
        "resultsLimit": 5,   # optional: limit number of posts
        "keywords": ["Artificial Intelligence", "AI"]  # optional: filter posts by keywords
    }

    # Start the actor and wait for completion
    run = await actor_client.call(run_input=run_input)
    
    run_id = run['id']
    print(f"our actor run started with run id : {run_id}")

    # Fetch dataset items
    dataset_client = client.dataset(run["defaultDatasetId"])
    dataset_items = await dataset_client.list_items()
    items = dataset_items.items

    # Prepare data for Excel
    data_for_excel = []
    for item in items:
        media_urls = ", ".join([m.get('thumbnail', '') for m in item.get('media', [])])
        data_for_excel.append({
            'Post ID': item.get('postId'),
            'Page Name': item.get('pageName'),
            'Time': item.get('time'),
            'Text': item.get('text'),
            'Likes': item.get('likes'),
            'Comments': item.get('comments'),
            'Shares': item.get('shares'),
            'Is Video': item.get('isVideo'),
            'Views Count': item.get('viewsCount'),
            'Media URLs': media_urls,
            'Post URL': item.get('topLevelUrl')
        })
    # Create folder for media
    # os.makedirs("media", exist_ok=True)

    # data_for_excel = []
    # for idx, item in enumerate(items, 1):
    #     media_file_paths = []
    #     for m_idx, media in enumerate(item.get('media', []), 1):
    #         media_url = media.get('thumbnail') or media.get('url')
    #         if media_url:
    #             ext = ".mp4" if item.get('isVideo') else ".jpg"
    #             file_path = f"media/{item.get('postId')}_{m_idx}{ext}"
    #             try:
    #                 r = requests.get(media_url, stream=True)
    #                 if r.status_code == 200:
    #                     with open(file_path, "wb") as f:
    #                         for chunk in r.iter_content(1024):
    #                             f.write(chunk)
    #                     media_file_paths.append(file_path)
    #             except Exception as e:
    #                 print(f"Failed to download {media_url}: {e}")

    #     data_for_excel.append({
    #         'Post ID': item.get('postId'),
    #         'Page Name': item.get('pageName'),
    #         'Time': item.get('time'),
    #         'Text': item.get('text'),
    #         'Likes': item.get('likes'),
    #         'Comments': item.get('comments'),
    #         'Shares': item.get('shares'),
    #         'Is Video': item.get('isVideo'),
    #         'Views Count': item.get('viewsCount'),
    #         'Media Files': ", ".join(media_file_paths),
    #         'Post URL': item.get('topLevelUrl')
    #     })



    # Convert to DataFrame
    df = pd.DataFrame(data_for_excel)

    # Save to Excel
    df.to_excel("facebook_posts.xlsx", index=False)
    print("Excel file saved as 'facebook_posts.xlsx'")

asyncio.run(main())
