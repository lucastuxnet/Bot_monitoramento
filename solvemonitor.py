import logging
import subprocess
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import schedule
import time
from threading import Thread

# Configuração do log
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Token do bot e chat ID
TOKEN = '7332448457:AAGGnFvU2kAkxMjkoCm5WnJX6Nnk3aow4rA'
CHAT_ID = '1285797036'

# Comando que será executado no servidor
COMANDO = 'docker stop $(docker ps -a -q) & docker rm -f $(docker ps -a -q) && docker rmi -f $(docker images -a -q) && echo "Processo finalizado"'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envia uma mensagem quando o comando /start é recebido."""
    await update.message.reply_text('Olá! Este bot de monitoramento enviará mensagens diárias e também uma mensagem de confirmação para remoção dos arquivos do servidor a cada 15 dias.')
    chat_id = update.message.chat_id
    context.job_queue.run_repeating(send_update, interval=86400, first=0, chat_id=chat_id)

async def confirm(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envia a mensagem de confirmação."""
    await context.bot.send_message(chat_id=CHAT_ID, text='Você quer executar o comando? Responda com /sim ou /nao')

async def sim(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Executa o comando no servidor se a resposta for /sim."""
    try:
        result = subprocess.run(COMANDO, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode('utf-8')
        await update.message.reply_text(f"Comando executado com sucesso:\\n{output}")
    except subprocess.CalledProcessError as e:
        await update.message.reply_text(f"Erro ao executar o comando:\\n{e.stderr.decode('utf-8')}")

async def nao(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Não executa o comando se a resposta for /nao."""
    await update.message.reply_text("Comando não executado.")

async def send_update(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envia uma atualização periódica."""
    job = context.job
    await context.bot.send_message(job.chat_id, text='Atualização periódica do bot.')

def main() -> None:
    """Start the bot."""
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("sim", sim))
    application.add_handler(CommandHandler("nao", nao))

    application.run_polling()

if __name__ == '__main__':
    main()