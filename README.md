# Gestão de Vulnerabilidades.

O objetivo do projeto solveMonitor é para o gerenciamento de vulnerabilidades.

O projeto foi desenvolvido com a finalidade de  monitoramento e remoção de arquivos em servidores de terceiros,
para nessidade de gestão de vulnerabilidades na empresa Esolvere Tecnologia.

Durante o projeto, são abordados os seguintes tópicos:

Criação de um ChatBot.
Criação de uma função de monitoramento de entradas e saídas em um servidor.
Criação de uma função monitoramento de históricos de comandos especificos útilizados pelo usuário no servidor com o intuito de navegação em imagens de containers arquivadas no servidor.
Integração da API-Telegram chatbot com o usuário administrador.
Criação de uma função de aviso temporal para o administrador.
Criação de uma função para elimitar containers e imagens que esteja armazenados em um servidor através de um comando pelo chatbot.

Bibliotecas necessárias para utilizar os bots.

- Logging
- Subprocess

Instalação e execução do código.

- Pip:
sudo apt install python3-pip

- API-Telegram:
pip install python-telegram-bot --upgrade

Para executar o projeto no terminal, digite o seguinte comando:

python3 solvemonitor.py




