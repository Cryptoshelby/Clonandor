from telethon import TelegramClient, sync, events
from telethon.sessions import StringSession
import requests
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime, timedelta
import time

API_ID = 27878760
API_HASH = 'b2cd626ab971e67c583c850d6274c39c'
STRING_SESSION = '1AZWarzwBu51rRN04oYrh1Mf14yHrJZEhFnYA7rZpEH0cD7v9Thav5j9fv7Ufip70zKYzhd_pLAnOQX_S5XlQm-PGzM3TmHrgclJ7zVFNPAxN9rAYvMH1Ivmv5WGxuRgfxNT_ypuIZFlhTbt3hJ1CBJMuon6UX2PZgPuzbeJjLagJb5z0t2W-zmEBI1bvlQomGFO02SRJ6_f7kM8bSLu8mOf-XVovMq6P0fjeK7fIxFJjyVXN2WTCwligEmm835H2ylev1oHYDlzCzHSx67prgNeZhUFqgOoNGf2aYAiKW0QLuQ8faMHUg5ItxdMKEuBqq4HSLktR-z-qLq6YetKqooomZWby-M8='
BOT_TOKEN = '8383642654:AAHxw7wBzRzzNwT7lAgqhJ9P7JYPQXdYrzI'
CANAL_DESTINO = '-1003982153049'
CANALES_FUENTE = ['@toncoin', '@tonkeeper_news', '@trendingapps', '@durov']

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')

def run_server():
    HTTPServer(('0.0.0.0', 3000), Handler).serve_forever()

threading.Thread(target=run_server, daemon=True).start()
print('🌐 Servidor HTTP iniciado')

client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
client.start()
print('🤖 Clonador híbrido iniciado')

# Clonar historial de 2 días al iniciar
hace2dias = datetime.now() - timedelta(days=2)
for canal in CANALES_FUENTE:
    try:
        messages = client.get_messages(canal, limit=5)
        for msg in messages:
            if msg.date.replace(tzinfo=None) > hace2dias:
                url = f'https://api.telegram.org/bot{BOT_TOKEN}/copyMessage'
                data = {'chat_id': CANAL_DESTINO, 'from_chat_id': canal, 'message_id': msg.id}
                r = requests.post(url, data=data)
                if r.status_code == 200:
                    print(f'📋 Historial clonado de {canal}')
                break
    except:
        pass

# Escuchar nuevos mensajes
@client.on(events.NewMessage(chats=CANALES_FUENTE))
async def clonar(event):
    try:
        url = f'https://api.telegram.org/bot{BOT_TOKEN}/copyMessage'
        data = {'chat_id': CANAL_DESTINO, 'from_chat_id': event.chat_id, 'message_id': event.message.id}
        requests.post(url, data=data)
        print(f'📋 Clonado de {event.chat.username}')
    except Exception as e:
        print(f'Error: {e}')

print('✅ Modo escucha activado')
client.run_until_disconnected()
