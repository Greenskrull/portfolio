import os
import subprocess
import time
import sys
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from itertools import cycle
from colorama import Fore, Style, init

init(autoreset=True)

logging.basicConfig(
    filename="chimera_advanced.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

results = {}

def spinner(text):
    spinner_cycle = cycle(["|", "/", "-", "\\"])
    sys.stdout.write(f"{text} ")
    for _ in range(10):
        sys.stdout.write(next(spinner_cycle))
        sys.stdout.flush()
        time.sleep(0.1)
        sys.stdout.write("\b")

def show_banner():
    banner = f"""
{Fore.GREEN}
   ██████╗██╗  ██╗██╗███╗   ███╗███████╗██████╗  █████╗
  ██╔════╝██║  ██║██║████╗ ████║██╔════╝██╔══██╗██╔══██╗
  ██║     ███████║██║██╔████╔██║█████╗  ██████╔╝███████║
  ██║     ██╔══██║██║██║╚██╔╝██║██╔══╝  ██╔═══╝ ██╔══██║
  ╚██████╗██║  ██║██║██║ ╚═╝ ██║███████╗██║     ██║  ██║
   ╚═════╝╚═╝  ╚═╝╚═╝╚═╝     ╚═╝╚══════╝╚═╝     ╚═╝  ╚═╝
{Style.RESET_ALL}
    The Ultimate Pentesting Tool
    """
    print(banner)
def run_command(command, description):
    print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} Running {description}...")
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        results[description] = result.stdout.strip()
        print(f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} {description} completed:\n")
        print(f"{Fore.YELLOW}{result.stdout}{Style.RESET_ALL}")
        logging.info(f"{description} Output:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        results[description] = "Error"
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} {description} failed. Check logs.")
        logging.error(f"{description} Error:\n{e.stderr}")

def detect_protocol(target):
    if target.startswith("http://"):
        return "http"
    elif target.startswith("https://"):
        return "https"
    elif ":" in target:  
        return "ssh" if target.endswith(":22") else "ftp"
    else:
        return "http"

def check_dependencies():
    tools = ["nmap", "nikto", "sqlmap", "hydra", "gobuster", "john"]
    missing_tools = []
    for tool in tools:
        if subprocess.call(["which", tool], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
            missing_tools.append(tool)
    if missing_tools:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Missing tools: {', '.join(missing_tools)}")
        sys.exit(1)

def nmap_scan(target):
    command = ["nmap", "-sV", "-Pn", target]
    run_command(command, "Nmap Scanning")

def nikto_scan(target_url):
    command = ["nikto", "-h", target_url]
    run_command(command, "Web Vulnerability Scanning (Nikto)")

def brute_force_auth(target, protocol, username, wordlist):
    command = ["hydra", "-l", username, "-P", wordlist, f"{protocol}://{target}"]
    run_command(command, "Authentication Brute-Force")

def crack_password(hash_file, wordlist):
    command = ["john", "--wordlist=" + wordlist, hash_file]
    run_command(command, "Password Cracking")

def test_sql_injection(target_url):
    command = ["sqlmap", "-u", target_url, "--batch", "--level=5", "--risk=3"]
    run_command(command, "SQL Injection Testing")

def enumerate_subdomains(domain, wordlist):
    command = ["gobuster", "dns", "-d", domain, "-w", wordlist]
    run_command(command, "Subdomain Enumeration")

def combined_attack(target, username, wordlist, hash_file, domain):
    protocol = detect_protocol(target)
    target_url = target if protocol.startswith("http") else f"http://{target}"
    print(f"{Fore.YELLOW}[INFO]{Style.RESET_ALL} Starting Combined Attack Workflow...")

    with ThreadPoolExecutor(max_workers=6) as executor:
        tasks = [
            executor.submit(nmap_scan, target),
            executor.submit(nikto_scan, target_url),
            executor.submit(test_sql_injection, target_url),
        ]
        if username and wordlist:
            tasks.append(executor.submit(brute_force_auth, target, protocol, username, wordlist))
        if hash_file and wordlist:
            tasks.append(executor.submit(crack_password, hash_file, wordlist))
        if domain:
            tasks.append(executor.submit(enumerate_subdomains, domain, wordlist))

        for future in as_completed(tasks):
            future.result()

    print(f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} Combined Attack Complete.")

def show_results():
    print(f"{Fore.MAGENTA}[INFO]{Style.RESET_ALL} Displaying Results:")
    print("=" * 50)
    for desc, output in results.items():
        print(f"{Fore.YELLOW}{desc}:{Style.RESET_ALL}\n{output}\n")
        print("-" * 50)

def main():
    check_dependencies()
    show_banner()

    target = input(f"{Fore.CYAN}[?]{Style.RESET_ALL} Enter target IP or URL: ").strip()
    username = input(f"{Fore.CYAN}[?]{Style.RESET_ALL} Username for brute force (if applicable): ").strip()
    wordlist = input(f"{Fore.CYAN}[?]{Style.RESET_ALL} Path to wordlist: ").strip()
    hash_file = input(f"{Fore.CYAN}[?]{Style.RESET_ALL} Path to hash file (if applicable): ").strip()
    domain = input(f"{Fore.CYAN}[?]{Style.RESET_ALL} Domain for subdomain enumeration (if applicable): ").strip()

    print(f"{Fore.YELLOW}[INFO]{Style.RESET_ALL} Starting Chimera Attack...")
    combined_attack(target, username, wordlist, hash_file, domain)
    show_results()

if __name__ == "__main__":
    main()