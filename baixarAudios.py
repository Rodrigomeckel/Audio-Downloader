import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar, Combobox
from pytube import YouTube
from pytube.exceptions import RegexMatchError
from threading import Thread
import os

def choose_download_path():
    download_path = filedialog.askdirectory()
    if download_path:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, download_path)

def download_progress(stream, chunk, remaining):
    percent = (100 * (stream.filesize - remaining)) / stream.filesize
    progress_bar["value"] = percent
    root.update_idletasks()

def download_audio():
    url = url_entry.get()
    path = path_entry.get()

    try:
        yt = YouTube(url, on_progress_callback=download_progress)
        stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()
        if stream:
            progress_bar["value"] = 0
            download_button.config(state=tk.DISABLED)
            Thread(target=download_and_convert_audio, args=(stream, path), daemon=True).start()
        else:
            messagebox.showerror("Erro", "Nenhum fluxo de áudio adequado disponível para download.")
    except RegexMatchError:
        messagebox.showerror("Erro", "URL do YouTube inválido")
    except Exception as e:
        messagebox.showerror("Erro", f"Um erro ocorreu: {e}")
    finally:
        download_button.config(state=tk.NORMAL)

def download_and_convert_audio(stream, path):
    try:
        filename = stream.default_filename.replace(".mp4", ".mp3")
        stream.download(output_path=path)
        os.rename(os.path.join(path, stream.default_filename), os.path.join(path, filename))
        messagebox.showinfo("Sucesso", "Áudio baixado e convertido com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Um erro ocorreu: {e}")
    finally:
        download_button.config(state=tk.NORMAL)

# Create the main window
root = tk.Tk()
root.title("Download de audio Youtube")
root.geometry("500x300")
root.resizable(False, False)
root.configure(bg="#f0f0f0")

# Create the widgets
url_label = tk.Label(root, text="Video URL:", bg="#f0f0f0")
url_entry = tk.Entry(root, width=50)
path_label = tk.Label(root, text="Pasta de Download:", bg="#f0f0f0")
path_entry = tk.Entry(root, width=50)
browse_button = tk.Button(root, text="Pesquisar", command=choose_download_path)
download_button = tk.Button(root, text="Download Audio", command=download_audio)
progress_bar = Progressbar(root, orient=tk.HORIZONTAL, length=400, mode='determinate')

# Organize the widgets in the window
url_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
url_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
path_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
path_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
browse_button.grid(row=1, column=2, padx=5, pady=5)
download_button.grid(row=2, columnspan=3, padx=5, pady=5)
progress_bar.grid(row=3, columnspan=3, padx=5, pady=5)

# Start the main application loop
root.mainloop()