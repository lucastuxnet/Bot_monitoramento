import logging
import subprocess
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio

# Configuração do log
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Token do bot e chat ID
TOKEN = '7332448457:AAGGnFvU2kAkxMjkoCm5WnJX6Nnk3aow4rA'
CHAT_ID = '1285797036'

# Comando que será executado no servidor
COMANDO = 'docker stop $(docker ps -a -q) & docker rm -f $(docker ps -a -q) && docker rmi -f $(docker images -a -q) && echo "Processo finalizado"'  # Docker ou Podman
#COMANDO = 'podman stop $(podman ps -a -q) & podman rm -f $(podman ps -a -q) && podman rmi -f $(podman images -a -q) && echo "Processo finalizado"'  # Docker ou Podman

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
async def send_update(context: ContextTypes.DEFAULT_TYPE):
    chat_id = CHAT_ID
    last_users = get_last_users()
    docker_exec_history = get_docker_exec_history()
    
    message = f"Últimos 10 usuários que entraram no servidor:\n{last_users}\n\n"
    message += f"Histórico de comandos com 'docker exec':\n{docker_exec_history}"
    
    await context.bot.send_message(chat_id=chat_id, text=message)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envia uma mensagem quando o comando /start é recebido."""
    await update.message.reply_text(
        'Olá! Este bot de monitoramento enviará mensagens diárias e também uma mensagem de confirmação para remoção dos arquivos do servidor a cada 15 dias.'
    )

async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envia a mensagem de confirmação."""
    await context.bot.send_message(chat_id=CHAT_ID, text='Você quer executar o comando? Responda com /sim ou /nao')

async def sim(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Executa o comando no servidor se a resposta for /sim."""
    try:
        result = subprocess.run(COMANDO, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode('utf-8')
        await update.message.reply_text(f"Comando executado com sucesso:\n{output}")
    except subprocess.CalledProcessError as e:
        await update.message.reply_text(f"Erro ao executar o comando:\n{e.stderr.decode('utf-8')}")

async def nao(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Não faz nada se a resposta for /nao."""
    await update.message.reply_text('Ação cancelada.')

async def main():
    """Inicia o bot."""
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("sim", sim))
    application.add_handler(CommandHandler("nao", nao))

    # Agendamento para enviar atualizações a cada hora
    job_queue = application.job_queue
    job_queue.run_repeating(send_update, interval=3600, first=0)

    await application.start_polling()
    await application.idle()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
