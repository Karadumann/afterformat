import tkinter as tk
from tkinter import ttk
import webbrowser
import os
import requests
import subprocess
from tkinter import messagebox
from pathlib import Path
import threading
import time
from PIL import Image, ImageTk
from io import BytesIO
import hashlib

class ProgramInstaller:
    def __init__(self, root):
        self.root = root
        self.version = "1.1.0"
        self.current_language = "en"
        self.download_folder = str(Path.home() / "Downloads" / "Program_Installer")
        self.icon_cache_folder = os.path.join(self.download_folder, "icons")
        self.icon_cache = {}
        
        os.makedirs(self.download_folder, exist_ok=True)
        os.makedirs(self.icon_cache_folder, exist_ok=True)
        
        # İndirme kuyruğu ve durum bilgisi
        self.download_queue = []
        self.current_downloads = []
        self.max_concurrent_downloads = 3
        
        self.translations = {
            "tr": {
                "title": "Program Yükleyici",
                "select_programs": "İndirmek İstediğiniz Programları Seçin",
                "download_button": "Seçili Programları İndir",
                "warning": "Uyarı",
                "select_warning": "Lütfen en az bir program seçin!",
                "info": "Bilgi",
                "download_started": "İndirme işlemi başladı. Dosyalar şu klasöre kaydedilecek:",
                "download_complete": "İndirme tamamlandı:",
                "download_error": "İndirme hatası:",
                "change_language": "Switch to English",
                "select_all": "Tümünü Seç",
                "deselect_all": "Tümünü Kaldır",
                "downloading": "İndiriliyor...",
                "download_speed": "İndirme Hızı",
                "remaining_time": "Kalan Süre:",
                "downloads_list": "İndirilenler Listesi",
                "status": "Durum",
                "progress": "İlerleme",
                "completed": "Tamamlandı",
                "failed": "Başarısız",
                "paused": "Duraklatıldı",
                "clear_completed": "Tamamlananları Temizle",
                "categories": {
                    "browsers": "Tarayıcılar",
                    "communication": "İletişim",
                    "development": "Geliştirici Araçları",
                    "multimedia": "Multimedya",
                    "gaming": "Oyun & Eğlence",
                    "utilities": "Sistem Araçları",
                    "security": "Güvenlik"
                },
                "installation_status": "Kurulum Durumu",
                "installing": "Kuruluyor...",
                "installed": "Kuruldu",
                "install_failed": "Kurulum Başarısız"
            },
            "en": {
                "title": "Program Installer",
                "select_programs": "Select Programs to Download",
                "download_button": "Download Selected Programs",
                "warning": "Warning",
                "select_warning": "Please select at least one program!",
                "info": "Information",
                "download_started": "Download started. Files will be saved to:",
                "download_complete": "Download completed:",
                "download_error": "Download error:",
                "change_language": "Türkçe'ye Geç",
                "select_all": "Select All",
                "deselect_all": "Deselect All",
                "downloading": "Downloading...",
                "download_speed": "Download Speed",
                "remaining_time": "Time Remaining:",
                "downloads_list": "Downloads List",
                "status": "Status",
                "progress": "Progress",
                "completed": "Completed",
                "failed": "Failed",
                "paused": "Paused",
                "clear_completed": "Clear Completed",
                "categories": {
                    "browsers": "Browsers",
                    "communication": "Communication",
                    "development": "Development Tools",
                    "multimedia": "Multimedia",
                    "gaming": "Gaming & Entertainment",
                    "utilities": "System Utilities",
                    "security": "Security"
                },
                "installation_status": "Installation Status",
                "installing": "Installing...",
                "installed": "Installed",
                "install_failed": "Installation Failed"
            }
        }

        self.categorized_programs = {
            "browsers": {
                "Google Chrome": {
                    "url": "https://dl.google.com/chrome/install/ChromeStandaloneSetup64.exe",
                    "direct_download": True,
                    "filename": "Chrome_Setup.exe",
                    "icon_url": "https://raw.githubusercontent.com/alrra/browser-logos/main/src/chrome/chrome.png"
                },
                "Mozilla Firefox": {
                    "url": "https://download.mozilla.org/?product=firefox-latest&os=win64&lang=tr",
                    "direct_download": True,
                    "filename": "Firefox_Setup.exe",
                    "icon_url": "https://raw.githubusercontent.com/alrra/browser-logos/main/src/firefox/firefox.png"
                },
                "Brave Browser": {
                    "url": "https://laptop-updates.brave.com/latest/winx64",
                    "direct_download": True,
                    "filename": "Brave_Setup.exe",
                    "icon_url": "https://raw.githubusercontent.com/alrra/browser-logos/main/src/brave/brave.png"
                }
            },
            "utilities": {
                "7-Zip": {
                    "url": "https://www.7-zip.org/a/7z2301-x64.exe",
                    "direct_download": True,
                    "filename": "7zip_Setup.exe",
                    "icon_url": "https://www.techspot.com/images2/downloads/topdownload/2014/06/7zip.png"
                },
                "Adobe Acrobat Pro": {
                    "url": "https://drive.usercontent.google.com/download?id=1WsYodIJjPV8wGKMEVdSVe3Ppn7lpkTvZ&export=download&authuser=0&confirm=t&uuid=b366c5a8-5eef-48cc-b2b1-9da0f8115d72&at=AIrpjvMZmnfsnTTjj6091bu-9OS3%3A1736720866704",
                    "direct_download": True,
                    "filename": "Adobe_Acrobat_Pro_Setup.exe",
                    "icon_url": "https://gdm-catalog-fmapi-prod.imgix.net/ProductLogo/7249df06-bcfe-46a1-9dfd-441d86aa80d3.png?w=80&h=80&fit=max&dpr=3&auto=format&q=50"
                },
                "Internet Download Manager": {
                    "url": "https://drive.usercontent.google.com/download?id=15rEhQFVCPfwiro_zvmTgI0OS9XO0CtT7&export=download&authuser=0&confirm=t&uuid=9c132578-086c-4aa3-b29f-51e6c3c8f5bb&at=AIrpjvMzLmf2LSezOT7tnu-TCH9K%3A1736602074815",
                    "direct_download": True,
                    "filename": "IDM_Setup.exe",
                    "icon_url": "https://store-images.s-microsoft.com/image/apps.59923.0c5ee452-c04d-4152-a6d4-2073117a0427.a781b8c0-8427-4934-8a8d-df2c74da6215.388aec9e-7312-4dcb-84bc-c35dc01a9075"
                },
                "AnyDesk Full Version": {
                    "url": "https://drive.usercontent.google.com/download?id=1Xe-Tuad2gq1zEn-VE5eiNEQ5EF8rnFaK&export=download&authuser=0&confirm=t&uuid=fcefe3c0-136b-4b63-a779-859ef580de9a&at=AIrpjvNDOPdVylNSuBlb1papPMKc%3A1736602155234",
                    "direct_download": True,
                    "filename": "AnyDesk_Setup.exe",
                    "icon_url": "https://www.applivery.com/wp-content/uploads/2024/09/AnyDesk.png"
                },
                "Traffic Monitor": {
                    "url": "https://drive.usercontent.google.com/download?id=1-MreAWdLb2UPzTfWIZjE2qJLQxgVHeou&export=download&authuser=0",
                    "direct_download": True,
                    "filename": "TrafficMonitor_Setup.exe",
                    "icon_url": "https://cdn-icons-png.flaticon.com/128/1527/1527814.png"
                },
                "Visual-C-Runtimes-All-in-One-May-2024": {
                    "url": "https://drive.usercontent.google.com/download?id=1ner-ddYc8vRm__4egUHR71RxbIiOEWfJ&export=download&authuser=0&confirm=t&uuid=5a7c8796-ca25-45f9-b31f-836e70908ee8&at=AIrpjvNMaqyv3UJ1QZJfCQZBlfwZ%3A1736717952335",
                    "direct_download": True,
                    "filename": "Visual_C_Runtimes_Setup.zip",
                    "icon_url": "https://cdn-icons-png.flaticon.com/128/5968/5968705.png"
                },
                "NVIDIA GeForce Experience": {
                    "url": "https://us.download.nvidia.com/GFE/GFEClient/3.27.0.112/GeForce_Experience_v3.27.0.112.exe",
                    "direct_download": True,
                    "filename": "GeForce_Experience_Setup.exe",
                    "icon_url": "https://cdn.prod.website-files.com/63f6e52346a353ca1752970e/644fb7a52156f63ce1fc3254_20230501T1259-761207c6-5c2d-4489-b10a-5af0d73cb454.jpeg"
                }
            },
            "development": {
                "Visual Studio Code": {
                    "url": "https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-user",
                    "direct_download": True,
                    "filename": "VSCode_Setup.exe",
                    "icon_url": "https://code.visualstudio.com/assets/images/code-stable.png"
                },
                "Cursor": {
                    "url": "https://downloader.cursor.sh/windows/nsis/x64",
                    "direct_download": True,
                    "filename": "Cursor_Setup.exe",
                    "icon_url": "https://i.ytimg.com/vi/1V4ryI2vN_I/maxresdefault.jpg"
                },
                "Notepad++": {
                    "url": "https://github.com/notepad-plus-plus/notepad-plus-plus/releases/download/v8.6.4/npp.8.6.4.Installer.x64.exe",
                    "direct_download": True,
                    "filename": "Notepad_Plus_Plus_Setup.exe",
                    "icon_url": "https://www.kaldata.com/wp-content/uploads/2016/11/notepad.jpg"
                },
                "Vencord": {
                    "url": "https://github.com/Vencord/Installer/releases/latest/download/VencordInstaller.exe",
                    "direct_download": True,
                    "filename": "VencordInstaller.exe",
                    "icon_url": "https://cdn-b.saashub.com/images/app/service_logos/257/esea491td7cs/large.png?1690800055"
                },
                "MySQL Workbench": {
                    "url": "https://dev.mysql.com/get/Downloads/MySQLGUITools/mysql-workbench-community-8.0.40-winx64.msi",
                    "direct_download": True,
                    "filename": "MySQL_Workbench_Setup.msi",
                    "icon_url": "https://d1.awsstatic.com/asset-repository/products/amazon-rds/1024px-MySQL.ff87215b43fd7292af172e2a5d9b844217262571.png"
                }
            }
        }
        
        self.web_redirect_programs = {
            "communication": {
                "Discord": {
                    "url": "https://discord.com/api/downloads/distributions/app/installers/latest?channel=stable&platform=win&arch=x64",
                    "direct_download": True,
                    "filename": "Discord_Setup.exe",
                    "icon_url": "https://cdn-icons-png.flaticon.com/128/5968/5968756.png"
                },
                "Discord Canary": {
                    "url": "https://canary.discord.com/api/downloads/distributions/app/installers/latest?channel=stable&platform=win&arch=x64",
                    "direct_download": True,
                    "filename": "Discord_Canary_Setup.exe",
                    "icon_url": "https://cdn-icons-png.flaticon.com/128/5968/5968756.png"
                },
                "Discord PTB": {
                    "url": "https://discord.com/api/download/ptb?platform=win",
                    "direct_download": True,
                    "filename": "Discord_PTB_Setup.exe",
                    "icon_url": "https://cdn-icons-png.flaticon.com/128/5968/5968756.png"
                },
                "WhatsApp Desktop": {
                    "url": "https://get.microsoft.com/installer/download/9NKSQGP7F2NH?cid=website_cta_psi",
                    "direct_download": True,
                    "filename": "WhatsApp_Setup.exe",
                    "icon_url": "https://cdn-icons-png.flaticon.com/128/3670/3670051.png"
                },
                "Telegram Desktop": {
                    "url": "https://telegram.org/dl/desktop/win64",
                    "direct_download": True,
                    "filename": "Telegram_Setup.exe",
                    "icon_url": "https://cdn-icons-png.flaticon.com/128/2111/2111646.png"
                },
                "Zoom": {
                    "url": "https://zoom.us/client/6.3.5.54827/ZoomInstallerFull.exe?archType=x64",
                    "direct_download": True,
                    "filename": "Zoom_Setup.exe",
                    "icon_url": "https://cdn-icons-png.flaticon.com/128/4401/4401470.png"
                }
            },
            "multimedia": {
                "VLC Media Player": {
                    "url": "https://get.videolan.org/vlc/3.0.21/win64/vlc-3.0.21-win64.exe",
                    "direct_download": True,
                    "filename": "VLC_Setup.exe",
                    "icon_url": "https://cdn-icons-png.flaticon.com/128/8728/8728427.png"
                },
                "Adobe Photoshop 2024": {
                    "url": "https://drive.usercontent.google.com/download?id=1VQtbETlwihOQf38PhotzD9snTP_gB8P-&export=download&authuser=0&confirm=t&uuid=4cca7b0a-ca41-489b-8d5a-0707c274f576&at=AIrpjvNifpyKanoEJvSrmxXvITHz%3A1736720773323",
                    "direct_download": True,
                    "filename": "Adobe_Photoshop_2024_Setup.exe",
                    "icon_url": "https://yt3.googleusercontent.com/ytc/AIdro_keG95kcun6Bg2BCPgHNt0b7Gi9ST3ylBP_xE9NM2RfVNqK=s900-c-k-c0x00ffffff-no-rj"
                },
                "Spotify": {
                    "url": "https://download.scdn.co/SpotifySetup.exe",
                    "direct_download": True,
                    "filename": "Spotify_Setup.exe",
                    "icon_url": "https://cdn-icons-png.flaticon.com/128/174/174872.png"
                },
                "HandBrake": {
                    "url": "https://handbrake.fr/rotation.php?file=HandBrake-1.9.0-x86_64-Win_GUI.exe",
                    "direct_download": True,
                    "filename": "HandBrake_Setup.exe",
                    "icon_url": "https://upload.wikimedia.org/wikipedia/commons/d/d9/HandBrake_Icon.png"
                },
                "Iriun Webcam": {
                    "url": "https://1758658189.rsc.cdn77.org/IriunWebcam-2.8.10.exe",
                    "direct_download": True,
                    "filename": "IriunWebcam_Setup.exe",
                    "icon_url": "https://play-lh.googleusercontent.com/W8IRyfkwEqHpcTy2N-f2nBRDHCXETcBxT9I-Gw1GAqhrfyB7tYj9F98X82e3Dfywcg"
                }
            },
            "gaming": {
                "Steam": {
                    "url": "https://cdn.fastly.steamstatic.com/client/installer/SteamSetup.exe",
                    "direct_download": True,
                    "filename": "Steam_Setup.exe",
                    "icon_url": "https://cdn-icons-png.flaticon.com/128/3670/3670382.png"
                },
                "Riot Games": {
                    "url": "https://valorant.secure.dyn.riotcdn.net/channels/public/x/installer/current/live.live.ap.exe",
                    "direct_download": True,
                    "filename": "RiotGames_Setup.exe",
                    "icon_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTAGvRhdg1vaZyhkn5zzE7p35e70SUgv0TVCw&s"
                }
            },
            "security": {
                "NetBird": {
                    "url": "https://pkgs.netbird.io/windows/x64",
                    "direct_download": True,
                    "filename": "NetBird_Setup.exe",
                    "icon_url": "https://play-lh.googleusercontent.com/gwsB0q8e3BMAGF0_iBsj8WfxfGyGHTG27krDWKhyfdy0H6ttcRYjBkOlP0nSyZxe6g"
                },
                "Password Safe": {
                    "url": "https://github.com/pwsafe/pwsafe/releases/download/3.67.0/pwsafe-3.67.0.exe",
                    "direct_download": True,
                    "filename": "PasswordSafe_Setup.exe",
                    "icon_url": "https://play-lh.googleusercontent.com/BmVmGzIJ7eFqpI784nf9KXNeHsKWkOnyMzmsq_Rxf3iL-zIzNlznERkf35gr4jBbNr2X"
                },
                "Flameshot": {
                    "url": "https://github.com/flameshot-org/flameshot/releases/download/v12.1.0/Flameshot-12.1.0-win64.msi",
                    "direct_download": True,
                    "filename": "Flameshot_Setup.msi",
                    "icon_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT8B7TeA0lSDz10CA2y4bWOAgZG-bJWAiO-_w&s"
                }
            }
        }
        
        for category, programs in self.web_redirect_programs.items():
            if category not in self.categorized_programs:
                self.categorized_programs[category] = {}
            for program, info in programs.items():
                self.categorized_programs[category][program] = info
        
        self.root.title(f"{self.get_text('title')} v{self.version}")
        self.root.geometry("1000x800")
        
        style = ttk.Style()
        style.configure("TNotebook", padding=10)
        style.configure("TNotebook.Tab", padding=[20, 5], font=('Helvetica', 10))
        style.configure("Download.TButton", padding=10, font=('Helvetica', 11, 'bold'))
        style.configure("Language.TButton", padding=5)
        
        self.create_widgets()
        
    def download_file(self, url, filename):
        try:
            session = requests.Session()
            response = session.get(url, stream=True)
            response.raise_for_status()
            
            filepath = os.path.join(self.download_folder, filename)
            total_size = int(response.headers.get('content-length', 0))
            
            block_size = 1024 * 1024  # 1MB blocks
            downloaded = 0
            start_time = time.time()
            last_update_time = start_time
            last_downloaded = 0
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=block_size):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        current_time = time.time()
                        
                        # Her 0.5 saniyede bir güncelle
                        if current_time - last_update_time >= 0.5:
                            elapsed = current_time - last_update_time
                            speed = (downloaded - last_downloaded) / (1024 * 1024 * elapsed)  # MB/s
                            progress = (downloaded / total_size * 100) if total_size > 0 else 0
                            
                            self.update_download_progress(
                                os.path.splitext(filename)[0].replace("_Setup", ""),
                                self.get_text("downloading"),
                                progress,
                                speed
                            )
                            
                            last_update_time = current_time
                            last_downloaded = downloaded
                            
                            self.root.update_idletasks()
            
            session.close()
            return True, filepath
        except Exception as e:
            return False, str(e)
    
    def run_installer(self, filepath, program_name):
        try:
            self.update_download_progress(
                program_name,
                self.get_text("completed"),
                100,
                0,
                self.get_text("installing")
            )
            
            # Visual C++ Runtimes için özel işlem
            if "Visual_C_Runtimes" in filepath:
                import zipfile
                import shutil
                
                # Zip dosyasını çıkar
                extract_path = os.path.join(os.path.dirname(filepath), "VC_Runtimes")
                with zipfile.ZipFile(filepath, 'r') as zip_ref:
                    zip_ref.extractall(extract_path)
                
                # Install.cmd dosyasını bul ve çalıştır
                install_cmd = os.path.join(extract_path, "Install.cmd")
                if os.path.exists(install_cmd):
                    process = subprocess.Popen([install_cmd], shell=True, cwd=extract_path)
                    process.wait(timeout=5)
                    
                    # Temizlik
                    try:
                        shutil.rmtree(extract_path)
                    except:
                        pass
            else:
                # Diğer programlar için normal kurulum
                process = subprocess.Popen([filepath], shell=True)
                process.wait(timeout=5)
            
            self.update_download_progress(
                program_name,
                self.get_text("completed"),
                100,
                0,
                self.get_text("installed")
            )
            print(f"Setup started: {program_name}")
        except subprocess.TimeoutExpired:
            # Timeout olması normal, kurulum devam ediyor demektir
            self.update_download_progress(
                program_name,
                self.get_text("completed"),
                100,
                0,
                self.get_text("installed")
            )
        except Exception as e:
            print(f"Setup start error ({program_name}): {str(e)}")
            self.update_download_progress(
                program_name,
                self.get_text("completed"),
                100,
                0,
                self.get_text("install_failed")
            )
            messagebox.showerror("Hata", f"Program başlatılamadı: {program_name}\nHata: {str(e)}")
    
    def load_program_icon(self, program_info):
        if 'icon_url' not in program_info:
            return None
            
        icon_url = program_info['icon_url']
        icon_hash = hashlib.md5(icon_url.encode()).hexdigest()
        icon_path = os.path.join(self.icon_cache_folder, f"{icon_hash}.png")
        
        if icon_hash in self.icon_cache:
            return self.icon_cache[icon_hash]
            
        if os.path.exists(icon_path):
            try:
                img = Image.open(icon_path)
                img = img.convert('RGBA')  # RGBA formatına dönüştür
                img = img.resize((24, 24), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.icon_cache[icon_hash] = photo
                return photo
            except Exception as e:
                print(f"Icon load error: {str(e)}")
                return None
                
        try:
            response = requests.get(icon_url)
            response.raise_for_status()  # HTTP hataları için kontrol
            img = Image.open(BytesIO(response.content))
            img = img.convert('RGBA')  # RGBA formatına dönüştür
            img = img.resize((24, 24), Image.Resampling.LANCZOS)
            img.save(icon_path, 'PNG')
            photo = ImageTk.PhotoImage(img)
            self.icon_cache[icon_hash] = photo
            return photo
        except Exception as e:
            print(f"Icon download error: {str(e)}")
            return None

    def pause_download(self, program_name):
        # İndirmeyi duraklat
        if program_name in self.current_downloads:
            self.current_downloads.remove(program_name)
            self.download_queue.insert(0, program_name)
            
    def resume_download(self, program_name):
        # İndirmeyi devam ettir
        if program_name in self.download_queue:
            self.download_queue.remove(program_name)
            self.process_download_queue()

    def process_download_queue(self):
        while len(self.current_downloads) < self.max_concurrent_downloads and self.download_queue:
            program = self.download_queue.pop(0)
            self.current_downloads.append(program)
            threading.Thread(target=self.download_program, args=(program,), daemon=True).start()

    def download_program(self, program):
        for category in self.categorized_programs:
            if program in self.categorized_programs[category]:
                program_info = self.categorized_programs[category][program]
                
                if program_info["direct_download"]:
                    success, result = self.download_file(
                        program_info["url"],
                        program_info.get("filename", f"{program}_Setup.exe")
                    )
                    
                    if success:
                        print(f"{self.get_text('download_complete')} {program}")
                        self.run_installer(result, program)
                        time.sleep(2)
                    else:
                        print(f"{self.get_text('download_error')} {program} - {result}")
                else:
                    webbrowser.open(program_info["url"])
                
                if program in self.current_downloads:
                    self.current_downloads.remove(program)
                self.process_download_queue()
                break

    def download_selected_programs(self):
        selected = [prog for prog, var in self.checkboxes.items() if var.get()]
        
        if not selected:
            messagebox.showwarning(self.get_text("warning"),
                                 self.get_text("select_warning"))
            return
        
        messagebox.showinfo(self.get_text("info"),
                          f"{self.get_text('download_started')}\n{self.download_folder}")
        
        self.download_queue.extend(selected)
        self.process_download_queue()

    def get_text(self, key, category=None):
        if category:
            return self.translations[self.current_language]["categories"][category]
        return self.translations[self.current_language][key]
    
    def select_all(self):
        for var in self.checkboxes.values():
            var.set(True)
            
    def deselect_all(self):
        for var in self.checkboxes.values():
            var.set(False)
            
    def toggle_language(self):
        self.current_language = "en" if self.current_language == "tr" else "tr"
        self.root.title(self.get_text("title"))
        
        for i, category in enumerate(self.categorized_programs):
            self.notebook.tab(i, text=self.get_text("categories", category))
        
        self.download_button.config(text=self.get_text("download_button"))
        self.lang_button.config(text=self.get_text("change_language"))

    def create_widgets(self):
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        top_frame = ttk.Frame(self.main_frame)
        top_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        title_label = ttk.Label(top_frame, 
                              text=self.get_text("select_programs"),
                              font=('Helvetica', 16, 'bold'))
        title_label.grid(row=0, column=0, pady=10)
        
        self.lang_button = ttk.Button(top_frame,
                                    text=self.get_text("change_language"),
                                    command=self.toggle_language,
                                    style="Language.TButton")
        self.lang_button.grid(row=0, column=1, padx=10)
        
        select_all_btn = ttk.Button(top_frame,
                                  text=self.get_text("select_all"),
                                  command=self.select_all)
        select_all_btn.grid(row=0, column=2, padx=5)
        
        deselect_all_btn = ttk.Button(top_frame,
                                    text=self.get_text("deselect_all"),
                                    command=self.deselect_all)
        deselect_all_btn.grid(row=0, column=3, padx=5)
        
        progress_frame = ttk.Frame(self.main_frame)
        progress_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(progress_frame, 
                                      orient="horizontal",
                                      length=300,
                                      mode="determinate",
                                      variable=self.progress_var)
        self.progress.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)
        
        self.speed_label = ttk.Label(progress_frame, text="")
        self.speed_label.grid(row=1, column=0, sticky=tk.W)
        
        self.time_label = ttk.Label(progress_frame, text="")
        self.time_label.grid(row=2, column=0, sticky=tk.W)
        
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        self.checkboxes = {}
        self.program_frames = {}
        
        for category in self.categorized_programs:
            frame = ttk.Frame(self.notebook, padding="10")
            self.notebook.add(frame, text=self.get_text("categories", category))
            
            canvas = tk.Canvas(frame, width=800)  # Canvas genişliğini ayarla
            scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            for i, (program, info) in enumerate(self.categorized_programs[category].items()):
                program_frame = ttk.Frame(scrollable_frame)
                program_frame.grid(row=i, column=0, sticky="w", pady=2)
                
                var = tk.BooleanVar()
                self.checkboxes[program] = var
                
                # Program ikonu
                icon = self.load_program_icon(info)
                if icon:
                    icon_label = ttk.Label(program_frame, image=icon)
                    icon_label.image = icon  # Referansı sakla
                    icon_label.grid(row=0, column=0, padx=(0, 5))
                
                # Program adı ve durum
                label_text = f"{program}"
                checkbox = ttk.Checkbutton(program_frame, text=label_text, variable=var)
                checkbox.grid(row=0, column=1, sticky="w")
                
                # İndirme durumu için frame
                status_frame = ttk.Frame(program_frame)
                status_frame.grid(row=0, column=2, padx=10)
                
                # İndirme durumu etiketi
                status_label = ttk.Label(status_frame, text="")
                status_label.grid(row=0, column=0)
                
                self.program_frames[program] = {
                    'frame': program_frame,
                    'status_label': status_label
                }
            
            canvas.grid(row=0, column=0, sticky="nsew")
            scrollbar.grid(row=0, column=1, sticky="ns")
            
            frame.grid_columnconfigure(0, weight=1)
            frame.grid_rowconfigure(0, weight=1)
        
        self.download_button = ttk.Button(self.main_frame,
                                        text=self.get_text("download_button"),
                                        command=self.download_selected_programs,
                                        style="Download.TButton")
        self.download_button.grid(row=3, column=0, pady=20)

        # Downloads List Frame
        downloads_frame = ttk.LabelFrame(self.main_frame, text=self.get_text("downloads_list"))
        downloads_frame.grid(row=4, column=0, padx=10, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Downloads List
        self.downloads_tree = ttk.Treeview(downloads_frame, 
            columns=("program", "status", "progress", "speed", "install_status"), 
            show="headings"
        )
        self.downloads_tree.heading("program", text=self.get_text("select_programs"))
        self.downloads_tree.heading("status", text=self.get_text("status"))
        self.downloads_tree.heading("progress", text=self.get_text("progress"))
        self.downloads_tree.heading("speed", text=self.get_text("download_speed"))
        self.downloads_tree.heading("install_status", text=self.get_text("installation_status"))
        
        # Kolon genişliklerini ayarla
        self.downloads_tree.column("program", width=200)
        self.downloads_tree.column("status", width=100)
        self.downloads_tree.column("progress", width=100)
        self.downloads_tree.column("speed", width=120)
        self.downloads_tree.column("install_status", width=120)
        
        # Scrollbar for Downloads List
        scrollbar = ttk.Scrollbar(downloads_frame, orient=tk.VERTICAL, command=self.downloads_tree.yview)
        self.downloads_tree.configure(yscrollcommand=scrollbar.set)
        
        self.downloads_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configure grid weights
        downloads_frame.grid_columnconfigure(0, weight=1)
        downloads_frame.grid_rowconfigure(0, weight=1)
        
        # Clear Completed Button
        clear_btn = ttk.Button(downloads_frame, text=self.get_text("clear_completed"), command=self.clear_completed_downloads)
        clear_btn.grid(row=1, column=0, columnspan=2, pady=5)

    def clear_completed_downloads(self):
        for item in self.downloads_tree.get_children():
            if self.downloads_tree.item(item)["values"][1] == self.get_text("completed"):
                self.downloads_tree.delete(item)

    def update_download_progress(self, program_name, status, progress=0, speed=0, install_status=""):
        # Find if program already exists in the tree
        for item in self.downloads_tree.get_children():
            if self.downloads_tree.item(item)["values"][0] == program_name:
                speed_text = f"{speed:.1f} MB/s" if speed > 0 else ""
                self.downloads_tree.item(item, values=(
                    program_name, 
                    status, 
                    f"{progress}%",
                    speed_text,
                    install_status
                ))
                return
        
        # If not found, add new entry
        self.downloads_tree.insert("", tk.END, values=(
            program_name, 
            status, 
            f"{progress}%",
            "",
            ""
        ))

if __name__ == "__main__":
    root = tk.Tk()
    app = ProgramInstaller(root)
    root.mainloop() 