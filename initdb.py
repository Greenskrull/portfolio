import sqlite3

def init_db():
    conn = sqlite3.connect('instance/projects.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            link TEXT,
            code_snippet TEXT NOT NULL,
            image TEXT
        )
    ''')
    # Add sample data
    cursor.execute('''
        INSERT INTO projects (title, description, link, code_snippet, image) 
        VALUES 
        (
            'WordPress WooCommerce Exploit Script', 
            'Discover vulnerabilities in WordPress WooCommerce sites with this script. Designed for educational purposes to highlight risks in e-commerce platforms.', 
            NULL, 
            '\nimport requests \nStart Exfiltration Server
def start_exfil_server(port=8080):
    class ExfilHandler(http.server.SimpleHTTPRequestHandler):
        def do_POST(self):
            try:
                content_length = int(self.headers["Content-Length"])\n
                post_data = self.rfile.read(content_length)\n
                print(f"\033[1;36m[+] Exfiltrated Data Received: {post_data.decode()}\033[0m")\n
                with open("exfil_data.log", "a") as f:\n
                    f.write(post_data.decode() + "\n")\n
                self.send_response(200)\n
                self.end_headers()\n
            except Exception as e:\n
                print(f"[!] Error in exfiltration server: {e}")
', 
            'woo.png'
        )
    ''') 
    cursor.execute('''
        INSERT INTO projects (title, description, link, code_snippet, image) 
        VALUES 
        (
            'Chimera', 
            'The script is a penetration testing tool called Chimera that automates tasks like network scanning, vulnerability assessment, brute force attacks, password cracking, and subdomain enumeration using tools like nmap, nikto, hydra, and more. It features dependency checks, concurrent task execution, detailed logging, and user-friendly prompts. Results are stored, displayed, and logged for comprehensive analysis.\n', 
            '', 
            'import requests\n# Combined Attack Workflow\n
def combined_attack(target, username, wordlist, hash_file, domain):\n
    protocol = detect_protocol(target)\n
    target_url = target if protocol.startswith("http") else f"http://{target}"\n
    print(f"{Fore.YELLOW}[INFO]{Style.RESET_ALL} Starting Combined Attack Workflow...")\n

    with ThreadPoolExecutor(max_workers=6) as executor:\n
        tasks = [\n
            executor.submit(nmap_scan, target),\n
            executor.submit(nikto_scan, target_url),\n
            executor.submit(test_sql_injection, target_url),\n
        ]\n
        if username and wordlist:\n
            tasks.append(executor.submit(brute_force_auth, target, protocol, username, wordlist))\n
        if hash_file and wordlist:\n
            tasks.append(executor.submit(crack_password, hash_file, wordlist))\n
        if domain:\n
            tasks.append(executor.submit(enumerate_subdomains, domain, wordlist))\n', 
            'mera.png'
        )
    ''')
    cursor.execute('''
        INSERT INTO projects (title, description, link, code_snippet, image)
        VALUES 
        (
            'BASH_FOR_A11', 
            'This Bash script is an advanced web penetration testing tool designed for Kali Linux, offering automated workflows for tasks like network scanning (Nmap), SQL injection testing (SQLMap), web application scanning (Wapiti), and exploitation (Metasploit). It also supports simulated ransomware encryption and DDoS attacks while logging results in a structured format. The script features a menu-driven interface, ensures dependencies are installed, and saves outputs for post-assessment review', 
            NULL, 
            'function setup_environment() {\n
    echo -e "${GREEN}Setting up the environment. Installing necessary tools...${RESET}"\n
    for tool in "${TOOLS[@]}"; do\n
        if ! command -v "$tool" &>/dev/null; then\n
            echo -e "${CYAN}Installing $tool...${RESET}"\n
            apt update && apt install -y "$tool"\n
        else\n
            echo -e "${GREEN}$tool is already installed.${RESET}"\n
        fi\n
    done\n
    echo -e "${GREEN}Environment setup complete.${RESET}"\n
}\n

function run_command() {\n
    local cmd="$1"\n
    local output_file="$2"\n
    echo -e "${CYAN}Running: $cmd${RESET}"\n
    echo -e "${CYAN}Command in progress...${RESET}"\n
    eval "$cmd" &> "$output_file"\n
    echo -e "${GREEN}Output saved to $output_file${RESET}"\n
}
', 
            'ko.png'
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
