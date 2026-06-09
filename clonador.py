from telethon import TelegramClient, sync, events
from telethon.sessions import StringSession
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

API_ID = 27878760
API_HASH = 'b2cd626ab971e67c583c850d6274c39c'
STRING_SESSION = '1AZWarzwBu51rRN04oYrh1Mf14yHrJZEhFnYA7rZpEH0cD7v9Thav5j9fv7Ufip70zKYzhd_pLAnOQX_S5XlQm-PGzM3TmHrgclJ7zVFNPAxN9rAYvMH1Ivmv5WGxuRgfxNT_ypuIZFlhTbt3hJ1CBJMuon6UX2PZgPuzbeJjLagJb5z0t2W-zmEBI1bvlQomGFO02SRJ6_f7kM8bSLu8mOf-XVovMq6P0fjeK7fIxFJjyVXN2WTCwligEmm835H2ylev1oHYDlzCzHSx67prgNeZhUFqgOoNGf2aYAiKW0QLuQ8faMHUg5ItxdMKEuBqq4HSLktR-z-qLq6YetKqooomZWby-M8='
CANAL_DESTINO = '@PaperplaneFeed'
CANALES_FUENTE = ['@toncoin', '@tonkeeper_news', '@trendingapps', '@durov']

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')

threading.Thread(target=HTTPServer(('0.0.0.0', 3000), Handler).serve_forever, daemon=True).start()
print('🌐 Servidor HTTP iniciado')

client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
client.start()
print('🤖 Clonador híbrido iniciado')

@client.on(events.NewMessage(chats=CANALES_FUENTE))
async def clonar(event):
    try:
        msg = event.message
        # 1. Copiar el mensaje original (mantiene emojis premium y formato)
        if msg.text:
            await client.send_message(CANAL_DESTINO, msg.text)
        elif msg.photo:
            await client.send_file(CANAL_DESTINO, msg.photo, caption=msg.text or '')
        elif msg.video:
            await client.send_file(CANAL_DESTINO, msg.video, caption=msg.text or '')
        else:
            await client.forward_messages(CANAL_DESTINO, msg.id, event.chat_id)
        
        # 2. Agregar análisis debajo (manteniendo el entorno visual)
        fecha = datetime.now().strftime('%A, %d de %B de %Y | %H:%M').replace('Monday','Lunes').replace('Tuesday','Martes').replace('Wednesday','Miércoles').replace('Thursday','Jueves').replace('Friday','Viernes').replace('Saturday','Sábado').replace('Sunday','Domingo')
        analisis = f'📊 *Telegram News - Análisis*\n' + '━'*30 + '\n\n📝 Esta información refleja las últimas tendencias del ecosistema Telegram.\n\n📅 {fecha}\n\n#Telegram #Noticias'
        await client.send_message(CANAL_DESTINO, analisis)
        
        print(f'📋 Clonado + análisis de {event.chat.username}')
    except Exception as e:
        print(f'Error: {e}')

print('✅ Modo escucha activado')
client.run_until_disconnected()
