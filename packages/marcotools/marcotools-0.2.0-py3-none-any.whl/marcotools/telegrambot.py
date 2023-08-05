import logging
import urllib.parse

import reqtry


class tb():
    def __init__(self, token_base):
        self._URL_BASE = f"https://api.telegram.org/bot{token_base}/"
        self._updates = []
        self._last_update_id = None

    def _req_get(self, url: str):
        return reqtry.get(url, timeout=(3, 3), tries=3, delay=1,
                          backoff=1.5, jitter=(1, 1.5))

    def _get_json(self, url: str) -> dict:
        return self._req_get(url).json()

    def _getUpdates(self, offset=None):
        url = self._URL_BASE + "getUpdates"
        if offset:
            url += "?offset={}".format(offset)
        updates = self._get_json(url)
        assert updates["ok"], 'The key "ok" is false.'
        self._updates = updates["result"]

    def _get_last_update_id(self):
        if not self._updates:
            return
        update_ids = []
        for update in self._updates:
            update_ids.append(int(update["update_id"]))
        self._last_update_id = max(update_ids) + 1

    def _get_updates_info(self) -> tuple:
        if not self._updates:
            return
        for update in self._updates:
            if 'edited_message' in update:
                text = update['edited_message']["text"] if "text" in update["message"] else ""
                chat = update['edited_message']["chat"]["id"]
                user = update['edited_message']["from"]["id"]
            else:
                text = update["message"]["text"] if "text" in update["message"] else ""
                chat = update["message"]["chat"]["id"]
                user = update["message"]["from"]["id"]
            yield (text, chat, user)

    def updates_handler(self, resp_handler):
        self._getUpdates(self._last_update_id)
        if not self._updates:
            return
        self._get_last_update_id()
        for update_info in self._get_updates_info():
            resp_handler(update_info)

    def send_message(self, text, chat_id):
        url = self._URL_BASE + f"sendMessage?text={text}&chat_id={chat_id}"
        result = self._req_get(url)
        assert result.status_code == 200, f"Message couldn't be delivered. Http code: {result.status_code}."
