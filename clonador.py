from telethon import TelegramClient, sync, events
from telethon.sessions import StringSession
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime, timedelta

API_ID = 27878760
API_HASH = 'b2cd626ab971e67c583c850d6274c39c'
STRING_SESSION = '1AZWarzwBu51rRN04oYrh1Mf14yHrJZEhFnYA7rZpEH0cD7v9Thav5j9fv7Ufip70zKYzhd_pLAnOQX_S5XlQm-PGzM3TmHrgclJ7zVFNPAxN9rAYvMH1Ivmv5WGxuRgfxNT_ypuIZFlhTbt3hJ1CBJMuon6UX2PZgPuzbeJjLagJb5z0t2W-zmEBI1bvlQomGFO02SRJ6_f7kM8bSLu8mOf-XVovMq6P0fjeK7fIxFJjyVXN2WTCwligEmm835H2ylev1oHYDlzCzHSx67prgNeZhUFqgOoNGf2aYAiKW0QLuQ8faMHUg5ItxdMKEuBqq4HSLktR-z-qLq6YetKqooomZWby-M8='
CANAL_DESTINO = '@PaperplaneFeed'
CANALES_FUENTE = ['@toncoin', '@tonkeeper_news', '@trendingapps', '@durov', '@cryptowallet_news_en']

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

# BUSCAR HISTORIAL DE 2 DÍAS
print('🔍 Buscando historial de 2 días...')
hace2dias = datetime.now() - timedelta(days=2)
for canal in CANALES_FUENTE:
    try:
        msgs = client.get_messages(canal, limit=5)
        for msg in msgs:
            if msg.date.replace(tzinfo=None) > hace2dias:
                client.send_message(CANAL_DESTINO, message=msg)
                print(f'📋 Historial: {canal}')
                break
    except Exception as e:
        print(f'Error historial {canal}: {e}')
print('✅ Historial procesado')

# ESCUCHAR NUEVOS MENSAJES
@client.on(events.NewMessage(chats=CANALES_FUENTE))
async def clonar(event):
    try:
        await client.send_message(CANAL_DESTINO, message=event.message)
        
        fecha = datetime.now().strftime('%A, %d de %B de %Y | %H:%M').replace('Monday','Lunes').replace('Tuesday','Martes').replace('Wednesday','Miércoles').replace('Thursday','Jueves').replace('Friday','Viernes').replace('Saturday','Sábado').replace('Sunday','Domingo')
        analisis = f'📊 *Telegram News - Análisis*\n' + '━'*30 + '\n\n📝 Esta información refleja las últimas tendencias del ecosistema Telegram.\n\n📅 {fecha}\n\n#Telegram #Noticias'
        await client.send_message(CANAL_DESTINO, analisis)
        
        print(f'📋 Clonado + análisis de {event.chat.username}')
    except Exception as e:
        print(f'Error: {e}')

print('✅ Modo escucha activado')
client.run_until_disconnected()
