import os
import json
import shlex
import subprocess
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackContext

# Configurações iniciais
TOKEN = 'seu-token'
CHAT_ID = 'seu-id'
PASSWORD = 'sua-senha'

# Arquivos
LOGON_FILE = "/home/usuario/pasta/do/bot/logon.json"
BLACKLIST_FILE = "/home/usuario/pasta/do/bot//blacklist.json"

# Configuração de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Estado para rastrear usuários detectados
detected_users = {}

# Monitoramento de usuários logados
async def monitor_users(context: CallbackContext) -> None:
    result = subprocess.run(['w', '-oh'], capture_output=True, text=True)
    users = []
    for line in result.stdout.strip().split('\n'):
        user_info = line.split()
        if user_info:
            users.append({
                "usuario": user_info[0],
                "tty": user_info[1],
            })
    with open(LOGON_FILE, 'w') as f:
        json.dump(users, f, indent=4)
    
    for user in users:
        if user['usuario'] not in detected_users:
            detected_users[user['usuario']] = user
            await context.bot.send_message(
                chat_id=CHAT_ID,
                text=f"Usuário detectado: {user['usuario']} com IP {user['tty']}\nDeseja bloquear? /bloquear {user['usuario']}"
            )

# Bloquear usuário
async def block_user(update: Update, context: CallbackContext) -> None:
    try:
        usuario = context.args[0]
    except IndexError:
        await update.message.reply_text("Por favor, forneça o nome do usuário para bloquear. Ex: /bloquear <usuario>")
        return
    
    if usuario in detected_users:
        ip = detected_users[usuario]['tty']
        # Adiciona regra ao iptables
        subprocess.run(shlex.split(f"sudo iptables -A INPUT -s {ip} -j DROP"))
        # Mata todos os processos do usuário
        subprocess.run(shlex.split(f"sudo killall -u {usuario}"))
        with open(BLACKLIST_FILE, 'a') as f:
            f.write(ip + '\n')
        del detected_users[usuario]
        await context.bot.send_message(
            chat_id=CHAT_ID,
            text=f"Usuário {usuario} com IP {ip} bloqueado e todos os processos finalizados."
        )
    else:
        await update.message.reply_text(f"Usuário {usuario} não encontrado ou já bloqueado.")

# Desbloquear IP
async def unblock_ip(update: Update, context: CallbackContext) -> None:
    try:
        ip = context.args[0]
    except IndexError:
        await update.message.reply_text("Por favor, forneça o IP para desbloquear. Ex: /desbloquear <ip>")
        return

    subprocess.run(shlex.split(f"sudo iptables -D INPUT -s {ip} -j DROP"))
    with open(BLACKLIST_FILE) as f:
        lines = f.readlines()
    with open(BLACKLIST_FILE, 'w') as f:
        for line in lines:
            if line.strip("\n") != ip:
                f.write(line)
    await context.bot.send_message(
        chat_id=CHAT_ID,
        text=f"IP {ip} desbloqueado."
    )

# Mostrar blacklist
async def show_blacklist(update: Update, context: CallbackContext) -> None:
    with open(BLACKLIST_FILE) as f:
        blacklist = f.readlines()
    await context.bot.send_message(
        chat_id=CHAT_ID,
        text="IPs bloqueados:\n" + "".join(blacklist)
    )

# Limpeza de arquivos
async def cleanup_files(context: CallbackContext) -> None:
    await context.bot.send_message(
        chat_id=CHAT_ID,
        text="Deseja remover o containers e limpar as imagens armazenados? /limpar ou /naolimpar"
    )

# Limpar arquivos
async def clear_files(update: Update, context: CallbackContext) -> None:
    try:
        senha = context.args[0]
    except IndexError:
        await update.message.reply_text("Por favor, forneça a senha. Ex: /limpar <senha>")
        return

    if senha == PASSWORD:
        subprocess.run("docker stop $(docker ps -a -q) & docker rm -f $(docker ps -a -q) && docker rmi -f $(docker images -a -q) && echo 'Processo finalizado'", shell=True)
#        subprocess.run("podman stop $(podman ps -a -q) & podman rm -f $(podman ps -a -q) && podman rmi -f $(podman images -a -q) && echo 'Processo finalizado'", shell=True)
        await context.bot.send_message(
            chat_id=CHAT_ID,
            text="Processo finalizado todos os containers e imagens foram removidos do sistema."
        )
    else:
        await context.bot.send_message(
            chat_id=CHAT_ID,
            text="Senha incorreta. Nenhum containers e imagens foram removidos do sistema."
        )

# Não limpar arquivos
async def dont_clear_files(update: Update, context: CallbackContext) -> None:
    await context.bot.send_message(
        chat_id=CHAT_ID,
        text="Nenhum containers e imagens foram removidos do sistema."
    )

# Comando para iniciar monitoramento
async def start_monitoring(update: Update, context: CallbackContext) -> None:
    await context.bot.send_message(
        chat_id=CHAT_ID,
        text="Sistema de monitoramento iniciado. \n \n Comandos para uso administrativo: \n \n 1. Para verificar IP's adicionados na Blacklist digite /Blacklist \n \n 2. Para desbloquear algum IP digite /desbloquear IP \n \n 3. Para remover todos os arquivos do servidor /limpar senha \n \n 4. Para bloquear algum usuário /bloquear usuário"
    )

# Comando para parar monitoramento
async def stop_monitoring(update: Update, context: CallbackContext) -> None:
    try:
        senha = context.args[0]
    except IndexError:
        await update.message.reply_text("Por favor, forneça a senha para desligar o sistema de monitoramento. Ex: /off <senha>")
        return

    if senha == PASSWORD:

        await context.bot.send_message(
            chat_id=CHAT_ID,
            text="Sistema de monitoramento desligado."
        )
        os._exit(0)  # Termina o processo

    else:
        await context.bot.send_message(
            chat_id=CHAT_ID,
            text="Senha incorreta. O sistema de monitoramento não foi desligado."
        )

# Manipulador de erros
async def error_handler(update: object, context: CallbackContext) -> None:
    logging.error(msg="Exception while handling an update:", exc_info=context.error)
    if update:
        await context.bot.send_message(chat_id=CHAT_ID, text="Ocorreu um erro. Por favor, tente novamente mais tarde.")

# Configuração do bot
application = ApplicationBuilder().token(TOKEN).build()

application.add_handler(CommandHandler("on", start_monitoring))
application.add_handler(CommandHandler("off", stop_monitoring))
application.add_handler(CommandHandler("bloquear", block_user))
application.add_handler(CommandHandler("blacklist", show_blacklist))
application.add_handler(CommandHandler("desbloquear", unblock_ip))
application.add_handler(CommandHandler("limpar", clear_files))
application.add_handler(CommandHandler("naolimpar", dont_clear_files))
application.add_error_handler(error_handler)  # Registra o manipulador de erros

# Agendamento para limpeza - (Setado para 15 dias)
application.job_queue.run_repeating(cleanup_files, interval=15*24*60*60, first=0)

# Função principal
if __name__ == '__main__':
    application.job_queue.run_repeating(monitor_users, interval=60, first=0)
    application.run_polling()
