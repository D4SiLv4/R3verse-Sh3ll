# R3verse Sh3ll

O R3verse Sh3ll é um script avançado de shell reverso em Python projetado para operações de pentest. Este script permite controle remoto e execução de comandos em sistemas comprometidos, com notificações e relatórios integrados via Discord. O R3verse Sh3ll fornece uma variedade de funcionalidades para coleta de informações, execução de comandos, monitoramento de atividades e exfiltração de dados.⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

![image](https://github.com/user-attachments/assets/f7e7a328-3b0f-483f-bb03-58e2bfab9698)


# Funcionalidades
- Execução de Comandos Remotos: Execute comandos no sistema alvo diretamente do canal Discord.
- Captura de Tela: Realiza captura de tela e envia as imagens para o Discord.
- Gravação de Tela: Grava a tela do alvo e envia o vídeo resultante para o Discord.
- Keylogger: Registra todas as teclas pressionadas e pode salvar ou enviar o log para o Discord.
- Exfiltração de Dados do Navegador: Coleta cookies e outros dados armazenados nos navegadores e exfiltra para o Discord.
- Escalonamento de Privilégios: Tenta escalar privilégios para obter controle total do sistema alvo.
- Exploração de Rede: Explora a rede local e coleta informações sobre dispositivos conectados.
- Monitoramento de Atividades: Monitoramento contínuo das atividades de tela e teclado.
- Agendamento de Tarefas: Permite o agendamento de comandos para serem executados em horários específicos.
- Atualização Automática: Suporte para atualização do script a partir de uma URL fornecida.
- Notificações via Discord: Integração completa com o Discord para notificações e envio de relatórios.


 # Configuração do Discord
O script usa um bot do Discord para enviar notificações e receber comandos. Configure os seguintes parâmetros no script:

![image](https://github.com/user-attachments/assets/9c3d260a-0b1b-4245-b0a4-8c0939ecc7ef)

Para instalar todas as dependências, execute o seguinte comando:

pip install requests pyscreenshot opencv-python psutil keyboard discord browser_cookie3 mss


Os comandos para controlar o script devem ser enviados no canal configurado no Discord. Cada comando deve ser prefixado com um "!", por exemplo:

- !screenshot: Captura a tela e envia a imagem para o Discord.
- !record_screen: Inicia a gravação da tela.
- !stop_recording: Para a gravação da tela e envia o vídeo resultante.
- !keylog_start: Inicia o keylogger.
- !keylog_stop: Para o keylogger e salva o log.
- !send_keylog: Envia o log do keylogger para o Discord.
- !exfiltrate: Coleta dados do navegador e envia para o Discord.
- !escalate: Tenta escalar privilégios no sistema alvo.
- !explore: Explora a rede local e envia o resultado para o Discord.
- !schedule <comando> <hora>: Agenda um comando para ser executado em um horário específico.
- !update <URL>: Atualiza o script a partir de uma URL fornecida.

https://youtu.be/FykeAP13Yw4

Características
Compatibilidade entre plataformas: Funciona em sistemas baseados em Windows e Unix.
Personalizável: Facilmente configurável para direcionar diferentes endereços IP e portas.
Operação Furtiva: Opera com espaço mínimo para evitar detecção.
Tratamento de erros: Mecanismos integrados para lidar com erros comuns de rede e restabelecer conexões.
Extensível: O design modular permite fácil adição de novos recursos.
