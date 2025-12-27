from aiogram import Router, types, F
from ..utils.api import api_client
from ..keyboards.inline import get_episodes_keyboard

router = Router()

@router.message(F.text)
async def handle_user_code(message: types.Message):
    code = message.text.strip()
    if not code.isdigit():
        return

    media = await api_client.get_media_by_code(code)
    if not media:
        await message.answer("❌ Bunday kodli media topilmadi.")
        return

    if media['is_series']:
        episodes = media.get('episodes', [])
        if not episodes:
            await message.answer("⚠️ Ushbu serial uchun qismlar topilmadi.")
            return
        
        # Check if we have a target episode from the specific code
        target_ep = media.get('target_episode')
        
        # Sort by number for the keyboard
        episodes = sorted(episodes, key=lambda x: x['number'])
        
        # Determine which episode to show as primary and calculate page
        display_ep = target_ep if target_ep else episodes[0]
        
        current_page = 1
        if target_ep:
            # Find which page the target episode is on (1-indexed)
            try:
                ep_index = next(i for i, ep in enumerate(episodes) if ep['id'] == target_ep['id'])
                current_page = (ep_index // 12) + 1
            except StopIteration:
                pass

        title = media['title']
        if target_ep:
            caption = f"🎬 **{title} - {target_ep['number']}-qism**\n\nQismlar:"
        else:
            caption = f"🎬 **{title}**\n\nQismlar:"

        kb = get_episodes_keyboard(media['id'], episodes, page=current_page)
        
        try:
            await message.answer_video(
                video=display_ep['file_id'], 
                caption=caption, 
                reply_markup=kb, 
                parse_mode="Markdown"
            )
        except Exception as e:
            await message.answer(f"🎬 **{title}**\n\nQismlar:", reply_markup=kb, parse_mode="Markdown")
    else:
        # Movie
        await message.answer_video(video=media['file_id'], caption=f"🎬 **{media['title']}**\n\n{media['description']}", parse_mode="Markdown")

@router.callback_query(F.data.startswith("ep_"))
async def handle_episode_click(callback: types.CallbackQuery):
    episode_id = int(callback.data.split("_")[1])
    episode = await api_client.get_episode(episode_id)
    
    if not episode:
        await callback.answer("❌ Qism topilmadi.", show_alert=True)
        return
    
    # We might want the movie title too, but we only have episode data here.
    # To keep it simple, we just send the video.
    await callback.message.answer_video(
        video=episode['file_id'], 
        caption=f"🎬 **Qism: {episode['number']}**", 
        parse_mode="Markdown"
    )
    await callback.answer()

@router.callback_query(F.data.startswith("page_"))
async def handle_pagination(callback: types.CallbackQuery):
    _, media_id, page = callback.data.split("_")
    media_id = int(media_id)
    page = int(page)
    
    media = await api_client.get_media_by_id(media_id)
    if not media or not media['is_series']:
        return
    
    episodes = media.get('episodes', [])
    kb = get_episodes_keyboard(media['id'], episodes, page=page)
    
    await callback.message.edit_reply_markup(reply_markup=kb)
    await callback.answer()
