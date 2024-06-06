import logging
import subprocess
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
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
COMANDO = 'docker stop $(docker ps -a -q) & docker rm -f $(docker ps -a -q) && docker rmi -f $(docker images -a -q) && echo "Processo finalizado"'  # Docker ou Podman
#COMANDO = 'podman stop $(podman ps -a -q) & podman rm -f $(podman ps -a -q) && podman rmi -f $(podman images -a -q) && echo "Processo finalizado"'  # Docker ou Podman

def start(update: Update, context: CallbackContext) -> None:
    """Envia uma mensagem quando o comando /start é recebido."""
    update.message.reply_text('Olá! Este bot enviará uma mensagem de confirmação a cada 15 dias.')

def confirm(context: CallbackContext) -> None:
    """Envia a mensagem de confirmação."""
    context.bot.send_message(chat_id=CHAT_ID, text='Você quer executar o comando? Responda com /sim ou /nao')

def sim(update: Update, context: CallbackContext) -> None:
    """Executa o comando no servidor se a resposta for /sim."""
    try:
        result = subprocess.run(COMANDO, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode('utf-8')
        update.message.reply_text(f"Comando executado com sucesso:\n{output}")
    except subprocess.CalledProcessError as e:
        update.message.reply_text(f"Erro ao executar o comando:\n{e.stderr.decode('utf-8')}")

def nao(update: Update, context: CallbackContext) -> None:
    """Cancela a execução do comando se a resposta for /nao."""
    update.message.reply_text("Execução do comando cancelada.")

def job(context: CallbackContext):
    """Função que será agendada para ser executada a cada 15 dias."""
    context.bot.send_message(chat_id=CHAT_ID, text='Você quer executar o comando? Responda com /sim ou /nao')

def schedule_jobs(updater):
    """Agenda o envio de mensagens a cada 15 dias."""
    schedule.every(1).minutes.do(job, context=updater.dispatcher)
#    schedule.every(15).days.do(job, context=updater.dispatcher)

    while True:
        schedule.run_pending()
        time.sleep(1)

def main() -> None:
    """Inicia o bot."""
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("sim", sim))
    dispatcher.add_handler(CommandHandler("nao", nao))

    # Iniciar o agendador em uma thread separada
    Thread(target=schedule_jobs, args=(updater,)).start()

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()