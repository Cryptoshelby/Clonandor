from telethon import TelegramClient, sync, events
from telethon.sessions import StringSession
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

API_ID = 27878760
API_HASH = 'b2cd626ab971e67c583c850d6274c39c'
STRING_SESSION = '1AZWarzMBu46_Too-FZ5fxd2Pjg-eXisR9upPut7QJgVqLG7DN3EtCHX0j9iQmHGvOY1T7bF-VL6GEojMWBIT7yg5lk9HHA3gizt-8bSxmVmK6G35QAUqV_vfc-fWOQuZ5iroH9W9Qa9T7Mte7RSu_04c0kz8NT3Uwz10K-b16P8vQJv0WigC3CNifmbLsi5RGGyEdb23A7-aFPZeX0uZpEOJh22osj1QpvEOn1_pTpdptvMUJfuub_Z7PS2FAF4PS8eXZJCnFTEHCPOtD_6-zfRwycDOEaz-NZmXd8ojvAsD4tdo2KMGdoMli_ukW-G0WNKUKXLo7IOX3in6CGxxmp6se35-SVE='
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
