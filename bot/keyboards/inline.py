from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

def get_episodes_keyboard(movie_id: int, episodes: list, page: int = 1, per_page: int = 12):
    builder = InlineKeyboardBuilder()
    
    # Sort episodes by number just in case
    episodes = sorted(episodes, key=lambda x: x['number'])
    
    start = (page - 1) * per_page
    end = start + per_page
    current_episodes = episodes[start:end]
    
    for ep in current_episodes:
        builder.button(text=f"{ep['number']}", callback_data=f"ep_{ep['id']}")
    
    builder.adjust(4) # 4 buttons per row
    
    pagination_row = []
    if page > 1:
        pagination_row.append(InlineKeyboardButton(text="⬅️ Prev", callback_data=f"page_{movie_id}_{page-1}"))
    if end < len(episodes):
        pagination_row.append(InlineKeyboardButton(text="Next ➡️", callback_data=f"page_{movie_id}_{page+1}"))
        
    if pagination_row:
        builder.row(*pagination_row)
        
    return builder.as_markup()
