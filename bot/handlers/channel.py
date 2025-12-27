import re
from aiogram import Router, F, types
from ..utils.api import api_client
from ..config import DB_TG_CHANNEL

router = Router()

def parse_caption(caption: str):
    # Pattern to match "number-qism", "number qism", "numberqism"
    match = re.search(r'(\d+)[-\s]*qism', caption, re.IGNORECASE)
    
    # Try to find "Kino nomi: Title"
    name_match = re.search(r'Kino nomi:?\s*([^\n\r|➖]+)', caption, re.IGNORECASE)
    
    if name_match:
        title = name_match.group(1).strip()
        # Clean title from common emojis and special chars
        title = re.sub(r'[^\w\s\']+', '', title).strip()
    else:
        # Fallback: take first line and clean it
        title = caption.split('\n')[0].strip()
        if match:
            title = title.replace(match.group(0), '').strip()
        title = re.sub(r'\s+', ' ', title).strip(' ()[]-')

    if match:
        episode_number = int(match.group(1))
        return title, episode_number, True
        
    return title, None, False

@router.channel_post(F.video)
async def handle_channel_post(message: types.Message):
    if message.chat.id != DB_TG_CHANNEL:
        return
    caption = message.caption or "Nomsiz media"
    file_id = message.video.file_id
    
    title, episode_number, is_series = parse_caption(caption)
    
    data = {
        "title": title,
        "description": caption,
        "file_id": file_id,
        "is_series": is_series,
        "episode_number": episode_number
    }
    
    result = await api_client.create_media(data)
    
    code = result.get('new_code') or result.get('code')
    if code:
        await message.answer(f"✅ Media saqlandi!\n\nKod: `{code}`\nMedia: {title}" + (f" ({episode_number}-qism)" if is_series else ""))
