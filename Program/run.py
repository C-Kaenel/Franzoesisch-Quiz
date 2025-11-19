import os
import subprocess
import sys

def install_requirements(req_file):
    print("\n📦 Überprüfe und installiere benötigte Pakete...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", req_file])
    except subprocess.CalledProcessError:
        print("❌ Fehler bei der Installation der Pakete.")
        sys.exit(1)
    print("✔ Anforderungen erfolgreich installiert.\n")

def ensure_output_folder(path):
    if not os.path.exists(path):
        print("📁 Erstelle Ordner 'output'...")
        os.makedirs(path)
    print(f"✔ Output-Ordner bereit: {path}\n")

def start_main(main_file):
    print("🚀 Starte Quiz-Programm...\n")
    subprocess.call([sys.executable, main_file])

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    req_file = os.path.join(base_dir, "requirements.txt")
    main_file = os.path.join(base_dir, "main.py")
    output_folder = os.path.join(base_dir, "output")

    if not os.path.exists(req_file):
        print("❌ requirements.txt wurde nicht gefunden!")
        print("Bitte die Datei im Projektverzeichnis erstellen.")
        sys.exit(1)

    install_requirements(req_file)
    ensure_output_folder(output_folder)

    if not os.path.exists(main_file):
        print("❌ main.py wurde nicht gefunden!")
        sys.exit(1)

    start_main(main_file)

if __name__ == "__main__":
    main()

