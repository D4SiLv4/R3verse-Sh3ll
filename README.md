# R3verse Sh3ll

## Descrição

O `R3verse Sh3ll` é um script avançado de shell reverso escrito em Python, projetado para atividades de pentest e segurança da informação. Este script permite executar comandos remotamente, monitorar atividades do sistema, capturar telas, registrar teclas pressionadas, e muito mais, tudo integrado com notificações em tempo real via Discord.


![image](https://github.com/user-attachments/assets/f7e7a328-3b0f-483f-bb03-58e2bfab9698)

## Funcionalidades

- **Execução Remota de Comandos:** Permite a execução de comandos diretamente na máquina alvo.
- **Keylogger:** Registra todas as teclas pressionadas e envia os logs para o Discord.
- **Captura de Tela:** Captura imagens da tela do alvo e envia para o Discord.
- **Monitoramento de Atividades:** Monitora e captura atividades do sistema em tempo real.
- **Exfiltração de Dados do Navegador:** Exfiltra dados armazenados nos navegadores, como cookies e histórico de navegação.
- **Exploração de Rede:** Realiza varreduras na rede local para identificar dispositivos conectados.
- **Escalonamento de Privilégios:** Tenta escalar privilégios para obter controle total do sistema.
- **Gravação de Tela:** Grava a tela do alvo e salva ou envia o vídeo para o Discord.
- **Agendamento de Tarefas:** Permite agendar a execução de comandos em horários específicos.
# Configuração do Discord
O script usa um bot do Discord para enviar notificações e receber comandos. Configure os seguintes parâmetros no script:

![image](https://github.com/user-attachments/assets/9c3d260a-0b1b-4245-b0a4-8c0939ecc7ef)


Os comandos para controlar o script devem ser enviados no canal configurado no Discord. Cada comando deve ser prefixado com um "!", por exemplo:

- `!screenshot: Captura a tela e envia a imagem para o Discord.´
-  `!record_screen: Inicia a gravação da tela.´
-  `!stop_recording: Para a gravação da tela e envia o vídeo resultante.´
- `!keylog_start: Inicia o keylogger.´
-  `!keylog_stop: Para o keylogger e salva o log.´
-  `!send_keylog: Envia o log do keylogger para o Discord.´
-  `!exfiltrate: Coleta dados do navegador e envia para o Discord.´
- ` !escalate: Tenta escalar privilégios no sistema alvo.´
-  `!explore: Explora a rede local e envia o resultado para o Discord.´
-  `!schedule <comando> <hora>: Agenda um comando para ser executado em um horário específico.´
-  `!update <URL>: Atualiza o script a partir de uma URL fornecida.´


# Características
- Compatibilidade entre plataformas: Funciona em sistemas baseados em Windows e Unix.
- Personalizável: Facilmente configurável para direcionar diferentes endereços IP e portas.
- Operação Furtiva: Opera com espaço mínimo para evitar detecção.
- Tratamento de erros: Mecanismos integrados para lidar com erros comuns de rede e restabelecer conexões.
- Extensível: O design modular permite fácil adição de novos recursos.
## Dependências

Para executar o `R3verse Sh3ll`, é necessário instalar as seguintes bibliotecas Python:

Você pode instalar todas as dependências utilizando o seguinte comando:
### Instalação de Dependências

Para instalar todas as dependências necessárias, execute o seguinte comando:

```bash
pip install subprocess requests json threading os platform base64 logging pyscreenshot opencv-python psutil time tempfile keyboard datetime discord.py shutil sys browser-cookie3 mss

