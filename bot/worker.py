import asyncio
from typing import Dict, List

from telegram_api.api import TgClient
from telegram_api.dto import UpdateObj
from bot.session import UserSession

# Словарь сессий: chat_id → UserSession
SESSIONS: Dict[int, UserSession] = {}


class Worker:
    def __init__(self, token: str, queue: asyncio.Queue, concurrent_workers: int):
        self.tg_client = TgClient(token)
        self.queue = queue
        self.concurrent_workers = concurrent_workers
        self._tasks: List[asyncio.Task] = []

    def _get_session(self, chat_id: int) -> UserSession:
        if chat_id not in SESSIONS:
            SESSIONS[chat_id] = UserSession()
        return SESSIONS[chat_id]

    async def handle_update(self, upd: UpdateObj):
        if not upd.message or not upd.message.text:
            return

        chat_id = upd.message.chat.id
        text = upd.message.text.strip()
        session = self._get_session(chat_id)

        # Команды для запуска разных игр
        if text == "/start":
            from games.base import GAME_REGISTRY
            games_list = "\n".join(f"/{name} — {name.replace('_', ' ').title()}" for name in GAME_REGISTRY.keys())
            await self.tg_client.send_message(
                chat_id,
                f"🎮 Доступные игры:\n{games_list}"
            )
            return

        if text == "/guess_number":
            reply = session.start_game("guess_number")
            await self.tg_client.send_message(chat_id, reply)
            return

        if text == "/rps":
            reply = session.start_game("rps")
            await self.tg_client.send_message(chat_id, reply)
            return

        if session.current_game:
            reply = session.handle_input(text)
            await self.tg_client.send_message(chat_id, reply)
        else:
            await self.tg_client.send_message(
                chat_id,
                "Напиши /start, чтобы выбрать игру."
            )

    async def _worker(self):
        while True:
            upd = await self.queue.get()
            try:
                await self.handle_update(upd)
            except Exception as e:
                print(f"[Worker] Error: {e}")
            finally:
                self.queue.task_done()

    async def start(self):
        self._tasks = [asyncio.create_task(self._worker()) for _ in range(self.concurrent_workers)]

    async def stop(self):
        await self.queue.join()
        for t in self._tasks:
            t.cancel()
        await asyncio.gather(*self._tasks, return_exceptions=True)