#!/bin/bash

# Define o usuário e os comandos que deseja adicionar ao sudoers
USER="seu-usuario"
COMMANDS="/sbin/iptables, /usr/bin/killall"

# Verifica se a entrada já existe no sudoers
grep -q "^$USER ALL=(ALL) NOPASSWD: $COMMANDS" /etc/sudoers
if [ $? -eq 0 ]; then
    echo "Permissões já existem no sudoers para o usuário $USER."
else
    # Adiciona a entrada ao sudoers
    echo "$USER ALL=(ALL) NOPASSWD: $COMMANDS" | sudo tee -a /etc/sudoers
    if [ $? -eq 0 ]; then
        echo "Permissões adicionadas ao sudoers para o usuário $USER."
    else
        echo "Erro ao adicionar permissões ao sudoers."
    fi
fi


# Nome do arquivo de serviço
SERVICE_FILE="/etc/systemd/system/solvebot.service"

# Conteúdo do arquivo de serviço
SERVICE_CONTENT="[Unit]
Description=Serviço para Monitoramento de Usuários/Bloqueio de IPs e limpeza de aplicações conternizadas via Telegram
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/seu-usuario/pasta/do/bot/solvesec.py
WorkingDirectory=/home/seu-usuario/pasta/do/bot/
User=esolvere
Group=esolvere
Restart=always
Environment=\"PYTHONUNBUFFERED=1\"

[Install]
WantedBy=multi-user.target
"

# Cria o arquivo de serviço
echo "Criando arquivo de serviço em $SERVICE_FILE..."
echo "$SERVICE_CONTENT" | sudo tee $SERVICE_FILE > /dev/null

# Recarrega as unidades do systemd
echo "Recarregando daemon do systemd..."
sudo systemctl daemon-reload

# Habilita o serviço para iniciar na inicialização
echo "Habilitando serviço solvebot para iniciar na inicialização..."
sudo systemctl enable solvebot.service

# Inicia o serviço imediatamente
echo "Iniciando serviço solvebot..."
sudo systemctl start solvebot.service

# Verifica o status do serviço
echo "Verificando status do serviço solvebot..."
sudo systemctl status solvebot.service


echo "Você permite instalar as dependências necessárias? (s/n): "
read permission

if [ "$permission" != "${permission#[Ss]}" ] ;then
    echo "Instalando dependências..."

    sudo apt install python3-pip -y
    sudo rm /usr/lib/python3.*/EXTERNALLY-MANAGED
    pip install python-telegram-bot --upgrade
    pip install ushlex
    pip install "python-telegram-bot[job-queue]"

    echo "As dependências foram instaladas com sucesso."
else
    echo "Instalação cancelada."
fi




