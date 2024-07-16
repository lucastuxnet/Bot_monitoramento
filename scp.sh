#!/bin/bash

# Caminho do arquivo a ser transferido
SOURCE_FILE="certs/esolvere_private.pem"

# Verifica se o arquivo de origem existe
if [[ ! -f "$SOURCE_FILE" ]]; then
    echo "Erro: O arquivo $SOURCE_FILE não foi encontrado!"
    exit 1
fi

# Solicita o nome do usuário
read -p "Digite o nome do usuário: " USERNAME

# Solicita o IP de destino
read -p "Digite o IP de destino: " DEST_IP

# Solicita a pasta de destino
read -p "Digite a pasta de destino: " DEST_DIR

# Realiza a transferência do arquivo
scp -o HostKeyAlgorithms=ssh-rsa,ssh-dss -o PubkeyAcceptedKeyTypes=+ssh-rsa "$SOURCE_FILE" "${USERNAME}@${DEST_IP}:${DEST_DIR}"

# Verifica se a transferência foi bem-sucedida
if [[ $? -eq 0 ]]; then
    echo "Arquivo transferido com sucesso!"
else
    echo "Erro na transferência do arquivo."
    exit 1
fi
