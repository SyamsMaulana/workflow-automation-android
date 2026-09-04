import os
import json
import shutil
import datetime
import urllib.request

CONFIG_FILE = "config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "author": "User",
        "publisher": "Auto Studio",
        "doc_title": "Otomatisasi Sistem",
        "media_folder": "media_vault",
        "backup_folder": "backup",
        "media_extensions": [".jpg", ".jpeg", ".png", ".webp", ".mp4"]
    }

cfg = load_config()

def log_message(msg):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_msg = f"[{timestamp}] {msg}"
    print(formatted_msg)
    with open("automation.log", "a", encoding="utf-8") as f:
        f.write(formatted_msg + "\n")

def check_internet():
    try:
        urllib.request.urlopen("https://www.google.com", timeout=3)
        log_message("Status Jaringan: Online")
        return True
    except Exception:
        log_message("Status Jaringan: Offline")
        return False

def generate_json_ld():
    schema_data = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": cfg.get("doc_title"),
        "author": {"@type": "Person", "name": cfg.get("author")},
        "datePublished": datetime.datetime.now().strftime("%Y-%m-%d"),
        "publisher": {"@type": "Organization", "name": cfg.get("publisher")}
    }
    with open("metadata_schema.json", "w", encoding="utf-8") as f:
        json.dump(schema_data, f, indent=4, ensure_ascii=False)
    log_message("JSON-LD Metadata berhasil dikompilasi.")

def organize_media_files(target_dir="."):
    vault = os.path.join(target_dir, cfg.get("media_folder", "media_vault"))
    if not os.path.exists(vault):
        os.makedirs(vault)
    
    exts = tuple(cfg.get("media_extensions", ['.jpg', '.png', '.mp4']))
    moved = 0
    for file in os.listdir(target_dir):
        if file.lower().endswith(exts) and os.path.isfile(file):
            shutil.move(file, os.path.join(vault, file))
            moved += 1
    log_message(f"Media Organizer: {moved} file dipindahkan ke '{vault}/'")

def backup_workspace(source_dir=".", backup_dir=cfg.get("backup_folder", "backup")):
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_path = os.path.join(backup_dir, f"backup_{timestamp}")
    shutil.make_archive(zip_path, 'zip', source_dir)
    log_message(f"Auto-Backup tersimpan: {zip_path}.zip")

def autorun():
    log_message("=== AUTORUN AUTOMATION ENGINE START ===")
    check_internet()
    generate_json_ld()
    organize_media_files()
    backup_workspace()
    log_message("=== AUTORUN COMPLETED SUCCESSFULLY ===\n")

if __name__ == "__main__":
    autorun()
