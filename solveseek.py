import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import subprocess
import time

# Configuração de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Função para executar um comando shell e retornar a saída
def run_shell_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

# Função para obter os últimos 10 usuários que entraram no servidor
def get_last_users():
    command = "last -n 10"
    return run_shell_command(command)

# Função para obter o histórico de comandos que utilizam `docker exec`
def get_docker_exec_history():
    command = "cat /home/$USER/.bash_history | grep 'docker exec'"
    return run_shell_command(command)

# Função para enviar informações para o Telegram
def send_update(context: CallbackContext):
    chat_id = context.job.context
    last_users = get_last_users()
    docker_exec_history = get_docker_exec_history()
    
    message = f"Últimos 10 usuários que entraram no servidor:\n{last_users}\n\n"
    message += f"Histórico de comandos com 'docker exec':\n{docker_exec_history}"
    
    context.bot.send_message(chat_id=chat_id, text=message)

# Comando /start para iniciar o bot
def start(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    update.message.reply_text('Olá! Eu sou o bot de monitoramento do servidor.')
    context.job_queue.run_repeating(send_update, interval=100, first=0, context=chat_id)

def main():
    # Substitua 'YOUR_TOKEN' pelo token do seu bot
    updater = Updater("7332448457:AAGGnFvU2kAkxMjkoCm5WnJX6Nnk3aow4rA", use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()