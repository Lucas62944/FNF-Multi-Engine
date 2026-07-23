import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import subprocess
import shutil
import json

# ==========================================
# CONFIGURAÇÕES DE VERSÃO DO LAUNCHER (2026)
# ==========================================
CURRENT_VERSION = "1.3.0"
LATEST_VERSION = "1.3.0" 

class FNFLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title(f"FNF Multi-Engine Launcher v.{CURRENT_VERSION}")
        self.root.geometry("800x880")
        
        # Variáveis de Controle
        self.dark_mode = True
        self.use_outdated_check = tk.BooleanVar(value=True)
        self.mod_enabled_var = tk.BooleanVar(value=True)
        self.current_lang = tk.StringVar(value="Português")
        self.engines = ["Psych Engine", "V-Slice", "Codename"]
        self.current_engine = tk.StringVar(value=self.engines[0])
        self.current_version = tk.StringVar()

        # ==========================================
        # ESTRUTURA DE PASTAS (Usando 'data')
        # ==========================================
        self.data_dir = "data"
        self.mods_path = os.path.join(self.data_dir, "mods_folder")
        self.exe_path = os.path.join(self.data_dir, "executables_mods")

        for folder in [self.data_dir, self.mods_path, self.exe_path]:
            if not os.path.exists(folder):
                os.makedirs(folder)

        self.setup_ui()
        self.check_outdated() 
        self.update_versions()
        self.apply_theme()

    def setup_ui(self):
        self.tab_control = ttk.Notebook(self.root)
        self.tab_mods = tk.Frame(self.tab_control)
        self.tab_options = tk.Frame(self.tab_control)
        self.tab_control.add(self.tab_mods, text=" Gerenciador ")
        self.tab_control.add(self.tab_options, text=" Opções ")
        self.tab_control.pack(expand=1, fill="both")

        # --- CABEÇALHO ---
        self.lbl_main_title = tk.Label(self.tab_mods, font=("Arial", 24, "bold"), text="FNF Multi-Engine")
        self.lbl_main_title.pack(pady=(15, 2))
        self.lbl_lema = tk.Label(self.tab_mods, text="Your Rhythm, Your Engine, Your Rules", font=("Arial", 10, "italic"), fg="#00ffff")
        self.lbl_lema.pack(pady=(0, 15))

        # Seleção de Engine e Versão (Recurso v1.2.0)
        self.frame_top = tk.Frame(self.tab_mods)
        self.frame_top.pack(pady=5)
        
        self.combo_engine = ttk.Combobox(self.frame_top, textvariable=self.current_engine, values=self.engines, state="readonly", width=18)
        self.combo_engine.pack(side="left", padx=5)
        self.combo_engine.bind("<<ComboboxSelected>>", lambda e: self.update_versions())
        
        self.combo_version = ttk.Combobox(self.frame_top, textvariable=self.current_version, state="readonly", width=18)
        self.combo_version.pack(side="left", padx=5)
        self.combo_version.bind("<<ComboboxSelected>>", lambda e: self.update_mods())

        # Lista de Mods
        self.frame_list_header = tk.Frame(self.tab_mods)
        self.frame_list_header.pack(fill="x", padx=100, pady=(10, 0))
        self.lbl_list_title = tk.Label(self.frame_list_header, font=("Arial", 10, "bold"), text="Mods Instalados")
        self.lbl_list_title.pack(side="left")
        self.lbl_count = tk.Label(self.frame_list_header, text="(Total: 0)", font=("Arial", 10), fg="#4CAF50")
        self.lbl_count.pack(side="left", padx=5)

        self.mods_listbox = tk.Listbox(self.tab_mods, font=("Arial", 11), width=65, height=12, borderwidth=0, highlightthickness=1)
        self.mods_listbox.pack(pady=5)
        self.mods_listbox.bind("<<ListboxSelect>>", self.on_mod_select)

        # Status do Mod Selecionado
        self.frame_status = tk.LabelFrame(self.tab_mods, text=" Estado do Mod ", font=("Arial", 10, "bold"))
        self.frame_status.pack(pady=5, fill="x", padx=100)
        
        self.check_mod_active = tk.Checkbutton(self.frame_status, text="Ativado", 
                                               variable=self.mod_enabled_var, command=self.toggle_mod_status)
        self.check_mod_active.pack(side="right", padx=10)
        
        self.lbl_compat = tk.Label(self.frame_status, text="Selecione um mod", font=("Arial", 10))
        self.lbl_compat.pack(side="left", padx=10, pady=5)

        # Botões do Gerenciador
        frame_util = tk.Frame(self.tab_mods)
        frame_util.pack(pady=5)
        self.btn_refresh = tk.Button(frame_util, text="🔄 ATUALIZAR", command=self.update_mods, bg="#607D8B", fg="white", width=15)
        self.btn_refresh.grid(row=0, column=0, padx=5)
        self.btn_open = tk.Button(frame_util, text="📂 ABRIR PASTA", command=self.open_mods_folder, bg="#795548", fg="white", width=15)
        self.btn_open.grid(row=0, column=1, padx=5)

        frame_mods_btns = tk.Frame(self.tab_mods)
        frame_mods_btns.pack(pady=10)
        self.btn_add = tk.Button(frame_mods_btns, text="➕ ADICIONAR MOD", bg="#2196F3", fg="white", command=self.add_mod, width=18)
        self.btn_add.grid(row=0, column=0, padx=5)
        self.btn_del = tk.Button(frame_mods_btns, text="🗑️ DELETAR MOD", bg="#f44336", fg="white", command=self.delete_mod, width=18)
        self.btn_del.grid(row=0, column=1, padx=5)

        self.btn_play = tk.Button(self.tab_mods, text="INICIAR JOGO", font=("Arial", 14, "bold"), bg="#4CAF50", fg="white", width=22, height=2, command=self.play_game)
        self.btn_play.pack(pady=15)

        # --- ABA OPÇÕES (Recursos da v1.2.0) ---
        self.lbl_opt_title = tk.Label(self.tab_options, text="Configurações", font=("Arial", 18, "bold"))
        self.lbl_opt_title.pack(pady=20)
        
        self.lbl_lang_text = tk.Label(self.tab_options, text="Idioma / Language:", font=("Arial", 10))
        self.lbl_lang_text.pack()
        self.combo_lang = ttk.Combobox(self.tab_options, textvariable=self.current_lang, values=["Português", "English"], state="readonly", width=20)
        self.combo_lang.pack(pady=5)
        self.combo_lang.bind("<<ComboboxSelected>>", lambda e: self.change_language())

        self.check_outdated_btn = tk.Checkbutton(self.tab_options, text="Ativar aviso de versão (Outdated Check)", variable=self.use_outdated_check, command=self.check_outdated)
        self.check_outdated_btn.pack(pady=15)

        self.btn_theme = tk.Button(self.tab_options, text="Alternar Tema", command=self.toggle_theme, width=25)
        self.btn_theme.pack(pady=5)
        
        self.btn_log = tk.Button(self.tab_options, text="Ver Changelog", command=self.show_changelog, width=25)
        self.btn_log.pack(pady=5)

        self.lbl_version_footer = tk.Label(self.tab_options, text=f"Versão: {CURRENT_VERSION}", font=("Arial", 8))
        self.lbl_version_footer.pack(side="bottom", pady=10)

    # ==========================
    # LÓGICA DE FUNCIONAMENTO
    # ==========================

    def get_mods_path(self):
        """Retorna o caminho da pasta mods_folder dentro de data"""
        return self.mods_path

    def update_versions(self):
        """Atualiza a lista de versões da Engine selecionada"""
        engine_name = self.current_engine.get()
        engine_key = "psych" if engine_name == "Psych Engine" else "codename" if engine_name == "Codename" else "v-slice"
        
        if engine_name == "V-Slice":
            self.combo_version.pack_forget()
            self.current_version.set("Padrao (Launcher)")
        else:
            self.combo_version.pack(side="left", padx=5)
            base = os.path.join(self.exe_path, engine_key)
            versions = ["Padrao (Launcher)"] if os.path.exists(base) else []
            v_path = os.path.join(base, "versions")
            if os.path.exists(v_path):
                for f in os.listdir(v_path):
                    if os.path.isdir(os.path.join(v_path, f)): 
                        versions.append(f)
            
            self.combo_version['values'] = versions if versions else ["Padrao (Launcher)"]
            self.current_version.set(versions[0] if versions else "Padrao (Launcher)")
            
        self.update_mods()

    def update_mods(self):
        """Atualiza a lista exibida de mods"""
        self.mods_listbox.delete(0, tk.END)
        path = self.get_mods_path()
        mod_count = 0
        engine_val = self.current_engine.get()

        if os.path.exists(path):
            for item in os.listdir(path):
                full_item_path = os.path.join(path, item)
                if os.path.isdir(full_item_path):
                    display = item
                    
                    if item.startswith("_off_"):
                        display = item.replace("_off_", "") + " [DESATIVADO]"
                    elif engine_val == "V-Slice":
                        v = self.get_mod_version(full_item_path)
                        if v: display += f" [{v}]"
                    
                    self.mods_listbox.insert(tk.END, display)
                    if "[DESATIVADO]" in display:
                        self.mods_listbox.itemconfig(tk.END, {'fg': '#888888'})
                    mod_count += 1
                    
        self.lbl_count.config(text=f"(Total: {mod_count})")

    def play_game(self):
        """Inicia o executável dentro da pasta data/executables_mods"""
        if not os.path.exists(self.exe_path):
            messagebox.showerror("Erro", f"A pasta '{self.exe_path}' não foi encontrada.")
            return

        exes = [f for f in os.listdir(self.exe_path) if f.endswith(".exe")]
        
        if exes:
            exe_file = exes[0]
            full_exe_path = os.path.join(self.exe_path, exe_file)
            selection = self.mods_listbox.curselection()
            
            if selection and self.current_engine.get() == "V-Slice":
                mod = self.mods_listbox.get(selection[0]).split(" [")[0].strip()
                subprocess.Popen([full_exe_path, "-mod", mod], cwd=self.exe_path)
            else:
                subprocess.Popen(full_exe_path, cwd=self.exe_path)
        else:
            messagebox.showwarning("Nenhum Executável", 
                f"Nenhum arquivo .exe foi encontrado em:\n{os.path.abspath(self.exe_path)}")

    def toggle_mod_status(self):
        selection = self.mods_listbox.curselection()
        if not selection: return
        
        mod_display_name = self.mods_listbox.get(selection[0])
        base_path = self.get_mods_path()
        real_name = mod_display_name.replace(" [DESATIVADO]", "").strip()
        is_active = self.mod_enabled_var.get()
        
        old_path = os.path.join(base_path, ("_off_" + real_name if "[DESATIVADO]" in mod_display_name else real_name))
        new_path = os.path.join(base_path, (real_name if is_active else "_off_" + real_name))

        try:
            if os.path.exists(old_path): 
                os.rename(old_path, new_path)
            if self.current_engine.get() == "Psych Engine":
                self.sync_psych_file(real_name, is_active)
            self.update_mods()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha na alteração: {e}")

    def sync_psych_file(self, mod_name, active):
        list_file = os.path.join(self.get_mods_path(), "modsList.txt")
        mods_data = {}
        if os.path.exists(list_file):
            with open(list_file, "r") as f:
                for line in f:
                    if "|" in line:
                        n, s = line.strip().split("|")
                        mods_data[n] = s
        mods_data[mod_name] = "1" if active else "0"
        with open(list_file, "w") as f:
            for n, s in mods_data.items(): f.write(f"{n}|{s}\n")

    def add_mod(self):
        path = self.get_mods_path()
        src = filedialog.askdirectory(title="Selecione a pasta do Mod")
        if src:
            mod_folder_name = os.path.basename(src)
            dest = os.path.join(path, mod_folder_name)
            try:
                if os.path.exists(dest):
                    if not messagebox.askyesno("Sobrescrever", f"O mod '{mod_folder_name}' já existe. Sobrescrever?"):
                        return
                    shutil.rmtree(dest)
                shutil.copytree(src, dest)
                messagebox.showinfo("Sucesso", f"Mod '{mod_folder_name}' adicionado com sucesso!")
                self.update_mods()
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível adicionar o mod: {e}")

    def delete_mod(self):
        selection = self.mods_listbox.curselection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um mod para deletar.")
            return

        display_name = self.mods_listbox.get(selection[0])
        base_path = self.get_mods_path()
        real_name = display_name.split(" [")[0].strip()
        
        target_path = os.path.join(base_path, real_name)
        if not os.path.exists(target_path):
            target_path = os.path.join(base_path, "_off_" + real_name)

        if messagebox.askyesno("Confirmar Exclusão", f"Excluir permanentemente o mod '{real_name}'?"):
            try:
                if os.path.exists(target_path):
                    shutil.rmtree(target_path)
                    messagebox.showinfo("Sucesso", "Mod removido!")
                    self.update_mods()
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível remover: {e}")

    def on_mod_select(self, event):
        selection = self.mods_listbox.curselection()
        if not selection: return
        mod_display = self.mods_listbox.get(selection[0])
        self.mod_enabled_var.set(False if "[DESATIVADO]" in mod_display else True)
        self.lbl_compat.config(text=mod_display.split(" [")[0])

    def get_mod_version(self, path):
        meta = os.path.join(path, "_polymod_meta.json")
        if os.path.exists(meta):
            try:
                with open(meta, 'r') as f: return f"v.{json.load(f).get('mod_version', '?.?')}"
            except: pass
        return None

    def open_mods_folder(self):
        os.startfile(self.get_mods_path())

    def check_outdated(self):
        if hasattr(self, 'lbl_warn'): self.lbl_warn.destroy()
        if self.use_outdated_check.get() and CURRENT_VERSION < LATEST_VERSION:
            self.lbl_warn = tk.Label(self.tab_mods, text=f"⚠️ VERSÃO {LATEST_VERSION} DISPONÍVEL!", bg="#ffcc00", fg="black")
            self.lbl_warn.pack(side="bottom", fill="x")

    def toggle_theme(self): 
        self.dark_mode = not self.dark_mode
        self.apply_theme()

    def apply_theme(self):
        t = {"bg": "#1e1e1e", "fg": "white", "list": "#2d2d2d"} if self.dark_mode else {"bg": "#f0f0f0", "fg": "black", "list": "white"}
        for w in [self.tab_mods, self.tab_options, self.root, self.frame_status, self.frame_list_header, self.frame_top]:
            if w: w.configure(bg=t["bg"])
        self.mods_listbox.configure(bg=t["list"], fg=t["fg"])
        self.lbl_main_title.config(bg=t["bg"], fg=t["fg"])
        self.check_mod_active.config(bg=t["bg"], fg=t["fg"], selectcolor=t["list"], activebackground=t["bg"])

    def show_changelog(self):
        messagebox.showinfo("Changelog", f"v.{CURRENT_VERSION}\n- Estrutura 'data/' (mods_folder & executables_mods)\n- Botões de arquivo/pasta reativados\n- Suporte a idiomas e temas")

    def change_language(self):
        is_en = self.current_lang.get() == "English"
        self.tab_control.tab(0, text=" Manager " if is_en else " Gerenciador ")
        self.lbl_list_title.config(text="Installed Mods" if is_en else "Mods Instalados")
        self.btn_refresh.config(text="🔄 REFRESH" if is_en else "🔄 ATUALIZAR")
        self.btn_open.config(text="📂 OPEN FOLDER" if is_en else "📂 ABRIR PASTA")
        self.btn_add.config(text="➕ ADD MOD" if is_en else "➕ ADICIONAR MOD")
        self.btn_del.config(text="🗑️ DELETE MOD" if is_en else "🗑️ DELETAR MOD")
        self.btn_play.config(text="START GAME" if is_en else "INICIAR JOGO")
        self.check_mod_active.config(text="Enabled" if is_en else "Ativado")
        self.frame_status.config(text=" Mod Status " if is_en else " Estado do Mod ")
        
        self.tab_control.tab(1, text=" Options " if is_en else " Opções ")
        self.lbl_opt_title.config(text="Settings" if is_en else "Configurações")
        self.check_outdated_btn.config(text="Enable version check" if is_en else "Ativar aviso de versão (Outdated Check)")
        self.btn_theme.config(text="Toggle Theme" if is_en else "Alternar Tema")
        self.btn_log.config(text="View Changelog" if is_en else "Ver Changelog")

if __name__ == "__main__":
    root = tk.Tk()
    app = FNFLauncher(root)
    root.mainloop()