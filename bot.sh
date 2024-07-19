#!/bin/bash

echo "Você permite instalar as dependências necessárias? (s/n): "
read permission

if [ "$permission" != "${permission#[Ss]}" ] ;then
    echo "Instalando dependências..."

    sudo apt install python3-pip -y
    pip install python-telegram-bot --upgrade
    pip install ushlex
    pip install "python-telegram-bot[job-queue]"

    echo "As dependências foram instaladas com sucesso."
else
    echo "Instalação cancelada."
fi
