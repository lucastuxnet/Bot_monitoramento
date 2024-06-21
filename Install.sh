#!/bin/bash

# Pergunta se deseja instalar as bibliotecas e aplicações
read -p "Deseja instalar as bibliotecas e as aplicações? (sim/não): " INSTALL_CONFIRMATION

if [ "$INSTALL_CONFIRMATION" != "sim" ]; then
    echo "Nenhuma aplicação ou biblioteca foram adicionadas."
    exit 0
fi

# Executa a instalação e configuração
echo "Iniciando a instalação das aplicações e bibliotecas..."

# Cria o diretório para imagens
mkdir -p images
cd images

# Atualiza a lista de pacotes e instala as aplicações
sudo apt-get update
sudo apt install -y podman
sudo apt install -y python3-pip
sudo -H pip3 install --upgrade pip
pip3 install podman-compose
sudo apt install -y docker.io
sudo usermod -aG docker $USER
sudo chmod 666 /var/run/docker.sock
sudo apt install -y curl
curl -O -L "https://github.com/sigstore/cosign/releases/latest/download/cosign-linux-amd64"
sudo mv cosign-linux-amd64 /usr/local/bin/cosign
sudo chmod +x /usr/local/bin/cosign
sudo apt-get install -y jq

# Mensagem de sucesso
echo "Aplicações."
echo ""
echo "- Podman"
echo "- Podman-compose"
echo "- Docker"
echo "- Cosign"
echo "- Pip"
echo "- JQ"
echo ""
echo "Todas as aplicações e bibliotecas foram adicionadas com sucesso."

# Pergunta se deseja criar as chaves de segurança
read -p "Você quer criar as chaves de segurança? (sim/não): " KEYS_CONFIRMATION

if [ "$KEYS_CONFIRMATION" != "sim" ]; then
    echo "Chaves de segurança não foram criadas."
    exit 0
fi

# Cria a pasta para certificados e navega para ela
mkdir -p certs
cd certs

# Gera as chaves de segurança
cosign generate-key-pair
podman run -it -v $PWD:/work:z docker.io/library/nginx openssl genrsa -out /work/esolvere_private.pem
podman run -it -v $PWD:/work:z docker.io/library/nginx openssl rsa -in /work/esolvere_private.pem -pubout -out /work/esolvere_public.pem

echo "Chaves de segurança criadas com sucesso."
