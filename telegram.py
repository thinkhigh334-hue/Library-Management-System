from telethon import TelegramClient
from telethon.tl.types import MessageMediaDocument
import asyncio

# Step 1: Get these from https://my.telegram.org/apps
API_ID = 24503866
API_HASH = '4eda5c84e1aec0ec90ade840e540bbcd'
PHONE_NUMBER = '+919909968936'

# Step 2: Initialize client
client = TelegramClient('session_name', API_ID, API_HASH)

# Your channel ID (extracted from link: https://t.me/c/2391960121/3378)
CHANNEL_ID = -1002391960121  # Note: Add -100 prefix for private channels

async def fetch_videos_in_range(channel_id, start_msg_id, end_msg_id):
    """
    Fetch all videos between two message IDs (inclusive)
    
    Args:
        channel_id: Channel ID (e.g., -1002391960121)
        start_msg_id: Starting message ID (e.g., 3378)
        end_msg_id: Ending message ID (e.g., 3390)
    """
    await client.start(phone=PHONE_NUMBER)
    
    print(f"Fetching videos from Message {start_msg_id} to {end_msg_id}")
    print("=" * 100)
    
    video_count = 0
    total_files = 0
    
    # Fetch messages in the range
    for msg_id in range(start_msg_id, end_msg_id + 1):
        try:
            message = await client.get_messages(channel_id, ids=msg_id)
            
            if message:
                total_files += 1
                
                # Check if message contains video
                if message.video or (message.document and message.document.mime_type and 'video' in message.document.mime_type):
                    video_count += 1
                    
                    # Extract filename
                    file_name = f"video_{msg_id}.mp4"
                    if message.document and message.document.attributes:
                        for attr in message.document.attributes:
                            if hasattr(attr, 'file_name'):
                                file_name = attr.file_name
                                break
                    
                    # Get caption
                    caption = message.text if message.text else "No caption"
                    
                    # Get file details
                    file_size = message.document.size if message.document else 0
                    duration = message.video.duration if message.video and hasattr(message.video, 'duration') else 0
                    
                    # Create message link
                    message_link = f"https://t.me/c/{str(channel_id)[4:]}/{msg_id}"
                    
                    print(f"\n📹 Video #{video_count} - Message ID: {msg_id}")
                    print(f"   Filename: {file_name}")
                    print(f"   Caption: {caption[:200]}")  # First 200 chars
                    print(f"   File Size: {file_size / (1024*1024):.2f} MB")
                    print(f"   Duration: {duration} seconds")
                    print(f"   Link: {message_link}")
                    print("-" * 100)
                    
        except Exception as e:
            print(f"Error fetching message {msg_id}: {e}")
    
    print(f"\n✅ Summary:")
    print(f"   Total messages checked: {total_files}")
    print(f"   Videos found: {video_count}")
    print("=" * 100)

async def download_specific_video(channel_username, message_id):
    """
    Download a specific video by message ID
    
    Args:
        channel_username: Channel username or ID
        message_id: Message ID of the video
    """
    await client.start(phone=PHONE_NUMBER)
    
    message = await client.get_messages(channel_username, ids=message_id)
    
    if message and message.video:
        print(f"Downloading video from message {message_id}...")
        file_path = await message.download_media(file='downloads/')
        print(f"Downloaded to: {file_path}")
        return file_path
    else:
        print("No video found in this message.")
        return None

async def search_videos_by_keyword(channel_username, keyword, limit=50):
    """
    Search for videos with specific keyword in caption
    
    Args:
        channel_username: Channel username or ID
        keyword: Keyword to search in captions
        limit: Number of messages to search through
    """
    await client.start(phone=PHONE_NUMBER)
    
    print(f"Searching for videos with keyword: '{keyword}'\n")
    print("=" * 80)
    
    found_count = 0
    
    async for message in client.iter_messages(channel_username, limit=limit):
        if message.video and message.text:
            if keyword.lower() in message.text.lower():
                found_count += 1
                
                # Extract filename
                file_name = f"video_{message.id}.mp4"
                for attr in message.document.attributes:
                    if hasattr(attr, 'file_name'):
                        file_name = attr.file_name
                        break
                
                print(f"\n📹 Match #{found_count}")
                print(f"   Filename: {file_name}")
                print(f"   Caption: {message.text[:100]}...")
                print(f"   Link: https://t.me/{channel_username}/{message.id}")
                print("-" * 80)
    
    print(f"\nTotal matches found: {found_count}")

# Main execution
async def main():
    """
    Fetch videos from your specific message range
    """
    
    # Your specific range: messages 3378 to 3390
    await fetch_videos_in_range(
        channel_id=CHANNEL_ID,
        start_msg_id=3378,
        end_msg_id=3390
    )
    
    await client.disconnect()

if __name__ == '__main__':
    # Run the async function
    asyncio.run(main())