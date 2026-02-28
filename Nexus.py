import os
import time
import platform
import ctypes
from pathlib import Path
from datetime import datetime

class NexusAuditor:
    def __init__(self):
        self.os_name = platform.system()
        self.is_admin = self._check_admin()
        self.local_app_data = os.environ.get("LOCALAPPDATA", "")
        self.roaming_app_data = os.environ.get("APPDATA", "")
        self.system_profile = self._gather_system_profile()
        
        # Setup the output directory structure on the Desktop
        self.output_dir = Path.home() / "Desktop" / "Nexus" / "Output"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.active_browsers = {}

    def _check_admin(self):
        """Checks if the script is running with elevated privileges."""
        try:
            return os.getuid() == 0
        except AttributeError:
            try:
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            except:
                return False

    def _gather_system_profile(self):
        return {
            "Hostname": platform.node(),
            "OS Version": platform.version(),
            "Architecture": platform.machine(),
            "Elevated Privileges": "Yes" if self.is_admin else "No",
            "Audit Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def print_banner(self):
        self.clear_screen()
        ascii_art = """
    ███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗
    ████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝
    ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗
    ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║
    ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║
    ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝
    :: Nexus - Automated Surface Auditor ::
        """
        print(ascii_art)

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def _map_all_targets(self):
        """Maps all potential browser paths."""
        if self.os_name != "Windows":
            return {}

        return {
            "Google Chrome": Path(self.local_app_data) / "Google/Chrome/User Data",
            "Chrome Beta": Path(self.local_app_data) / "Google/Chrome Beta/User Data",
            "Microsoft Edge": Path(self.local_app_data) / "Microsoft/Edge/User Data",
            "Brave": Path(self.local_app_data) / "BraveSoftware/Brave-Browser/User Data",
            "Opera Stable": Path(self.roaming_app_data) / "Opera Software/Opera Stable",
            "Opera GX": Path(self.roaming_app_data) / "Opera Software/Opera GX Stable",
            "Vivaldi": Path(self.local_app_data) / "Vivaldi/User Data",
            "Mozilla Firefox": Path(self.roaming_app_data) / "Mozilla/Firefox/Profiles",
            "Waterfox": Path(self.roaming_app_data) / "Waterfox/Profiles"
        }

    def discover_environments(self):
        """Interactive discovery phase."""
        self.print_banner()
        print("[*] Initializing heuristic browser discovery on host machine...\n")
        time.sleep(1.5)

        all_targets = self._map_all_targets()
        self.active_browsers = {name: path for name, path in all_targets.items() if path.exists()}

        while True:
            self.print_banner()
            print("[*] Discovery scan complete. Found the following environments:\n")
            
            if not self.active_browsers:
                print("    [-] No supported environments detected.")
                input("\nPress Enter to exit Nexus...")
                return False

            for name in self.active_browsers.keys():
                print(f"    [+] {name}")
                time.sleep(0.1)
                
            print("\n")
            choice = input("Are these all the target browsers? (Y/N): ").strip().lower()
            
            if choice == 'y':
                return True
            elif choice == 'n':
                print("\n[*] Initiating deep sector rescan. Please wait...")
                time.sleep(2.5) # Simulate a longer, deeper scan
                
                print("\n[-] Deep scan complete. No additional environments discovered.")
                proceed = input("Would you still like to proceed with the audit? (Y/N): ").strip().lower()
                
                if proceed == 'y':
                    return True
                else:
                    print("\nAborting Nexus initialization.")
                    time.sleep(1)
                    return False
            else:
                print("[-] Invalid input.")
                time.sleep(1)

    def analyze_file(self, file_path):
        try:
            stat = os.stat(file_path)
            size_kb = round(stat.st_size / 1024, 2)
            last_modified = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M')
            is_readable = os.access(file_path, os.R_OK)
            status = "EXPOSED" if is_readable else "LOCKED"
            
            return {
                "size": size_kb,
                "modified": last_modified,
                "status": status,
                "path": str(file_path)
            }
        except Exception:
            return None

    def scan(self, target_type):
        self.print_banner()
        print(f"[*] Executing {target_type} footprint audit...")
        print(f"[*] Target Host: {self.system_profile['Hostname']} | Output: {self.output_dir}\n")
        
        report_data = []

        if target_type == "Logins":
            targets = ["Login Data", "logins.json"]
        elif target_type == "Cookies":
            targets = ["Cookies", "Network/Cookies", "cookies.sqlite"]
        else:
            targets = ["Login Data", "Cookies", "Web Data", "History", "Local State"]

        for name, base_path in self.active_browsers.items():
            print(f"[+] Auditing environment: {name}")
            time.sleep(0.3)
            
            search_dirs = [base_path, base_path / "Default", base_path / "Network"]
            if "Firefox" in name or "Waterfox" in name:
                search_dirs = [d for d in base_path.iterdir() if d.is_dir()]

            for directory in search_dirs:
                if not directory.exists(): continue
                
                for target_file in targets:
                    file_path = directory / target_file
                    if file_path.exists():
                        meta = self.analyze_file(file_path)
                        if meta:
                            entry = f"[{meta['status']}] {name} -> {target_file} ({meta['size']} KB) | Active: {meta['modified']} | Path: {meta['path']}"
                            print(f"    -> Discovered: {target_file}")
                            report_data.append(entry)
                            time.sleep(0.1)

        return report_data

    def compile_report(self, data, target_type):
        if not data:
            print("\n[-] No surface data found for compiled report.")
            input("\nPress Enter to return to menu...")
            return

        filename = f"nexus_{target_type.lower()}_audit.txt"
        output_path = self.output_dir / filename
        
        print(f"\n[*] Packaging telemetry to {output_path}...")
        
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write("====================================================\n")
                f.write(f" NEXUS AUDIT REPORT: {target_type.upper()}\n")
                f.write("====================================================\n")
                for key, value in self.system_profile.items():
                    f.write(f" {key}: {value}\n")
                f.write("====================================================\n\n")
                
                for line in data:
                    f.write(line + "\n")
                    
            print("[+] Report compiled successfully.")
        except Exception as e:
            print(f"[-] Critical error writing report: {e}")
            
        input("\nPress Enter to return to main terminal...")

    def run(self):
        if not self.discover_environments():
            return

        while True:
            self.print_banner()
            print("Select target footprint to audit:\n")
            print("  [1] Audit Login Databases")
            print("  [2] Audit Session Cookies")
            print("  [3] Comprehensive Scan (All Surface Data)")
            print("  [4] Exit\n")
            
            choice = input("Nexus> ").strip()
            
            if choice == '1':
                results = self.scan("Logins")
                self.compile_report(results, "Logins")
            elif choice == '2':
                results = self.scan("Cookies")
                self.compile_report(results, "Cookies")
            elif choice == '3':
                results = self.scan("Comprehensive")
                self.compile_report(results, "Comprehensive")
            elif choice == '4':
                print("\nShutting down Nexus session...")
                break
            else:
                print("\n[-] Invalid command sequence.")
                time.sleep(1)

if __name__ == "__main__":
    os.system('') 
    app = NexusAuditor()
    app.run()
