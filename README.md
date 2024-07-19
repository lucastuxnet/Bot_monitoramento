# Gestão de Vulnerabilidades.

O objetivo do projeto solvesec é para o gerenciamento de vulnerabilidades em um servidor.

O projeto foi desenvolvido com a finalidade de  monitoramento e remoção de arquivos em servidores de terceiros, para uma demanda na empresa Esolvere Tecnologia.

Durante o projeto, são abordados os seguintes tópicos:

Criação de um ChatBot.<br>
Criação de uma função de alerta e monitoramento de entradas no servidor.<br>
Criação de uma função de bloqueio de usuário e host não autorizados no servidor.<br>
Integração da API-Telegram chatbot como o usuário administrador.<br>
Criação de uma função de aviso temporal para o administrador.<br>
Criação de uma função para elimitar containers e imagens que esteja armazenados em um servidor através de um comando pelo chatbot.<br>

Bibliotecas necessárias para utilizar o Chatbot.

- Ushlex
- JobQueue

Instalação e execução do código.

- Pip:
sudo apt install python3-pip

- API-Telegram:
pip install python-telegram-bot --upgrade

- Ushlex:
pip install ushlex

- Job Queue:
pip install "python-telegram-bot[job-queue]"



Para executar o projeto no terminal, digite o seguinte comando:

python3 solvesec.py




