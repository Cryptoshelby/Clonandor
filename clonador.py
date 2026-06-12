from telethon import TelegramClient, sync, events
from telethon.sessions import StringSession
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

API_ID = 27878760
API_HASH = 'b2cd626ab971e67c583c850d6274c39c'
STRING_SESSION = '1AZWarzMBu4nn5sfLXJsTU45fRwuhxj_CCF8jxjRpSGZnrpkM7wtevNJh3pUedLTeYo5OWJrY-EZeSBCuPEu0txOMKqF7cmXjTHfKN94v2iZe0U3PtZhsTkWyqbg_axljjEYSKAwg8eH6MiNiqSMbFvJBuFZqrTnF4BkcS_obg29MG1a_cQjmWM7N3rysFtK5V0tKcQ1csNhKq-sK5ekZj7psAycffE8YIoR0r5lnyOjWh5eJkLJeURG7Q3BK0SOX_F8HiusHQVq3Quu0T5Lc1z-yVFJPH6sOcWPK4L7YWC7_9zHFhupARVirML36mWXaJZVu3LtX1pKGu4FlOGqcED9bv4nJyKM='
CANAL_DESTINO = '@PaperplaneFeed'
CANALES_FUENTE = ['@toncoin', '@tonkeeper_news', '@trendingapps', '@durov', '@cryptowallet_news_en']

class Handler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')

threading.Thread(target=HTTPServer(('0.0.0.0', 3000), Handler).serve_forever, daemon=True).start()
print('🌐 Servidor HTTP iniciado')

client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
client.start()
print('🤖 Clonador iniciado')

@client.on(events.NewMessage(chats=CANALES_FUENTE))
async def clonar(event):
    await client.send_message(CANAL_DESTINO, message=event.message)
    print(f'📋 Clonado de {event.chat.username}')

client.run_until_disconnected()
