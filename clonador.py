import asyncio
from telethon import TelegramClient, events
import requests

API_ID = 27878760
API_HASH = 'b2cd626ab971e67c583c850d6274c39c'
BOT_TOKEN = '8383642654:AAHxw7wBzRzzNwT7lAgqhJ9P7JYPQXdYrzI'
CANAL_DESTINO = '-1003982153049'

CANALES_FUENTE = ['@toncoin', '@tonkeeper_news', '@trendingapps', '@durov']

client = TelegramClient('clonador_session', API_ID, API_HASH)

@client.on(events.NewMessage(chats=CANALES_FUENTE))
async def clonar(event):
    try:
        # Usar el Bot Token para publicar
        url = f'https://api.telegram.org/bot{BOT_TOKEN}/copyMessage'
        data = {
            'chat_id': CANAL_DESTINO,
            'from_chat_id': event.chat_id,
            'message_id': event.message.id
        }
        requests.post(url, data=data)
        print(f'📋 Clonado de {event.chat.username}')
    except Exception as e:
        print(f'Error: {e}')

async def main():
    await client.start()
    print('🤖 Clonador híbrido iniciado')
    await client.run_until_disconnected()

# Servidor HTTP falso para Render
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')

def run_server():
    server = HTTPServer(('0.0.0.0', 3000), Handler)
    server.serve_forever()

threading.Thread(target=run_server, daemon=True).start()

asyncio.run(main())
