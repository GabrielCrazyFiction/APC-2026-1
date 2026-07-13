from __future__ import annotations
import logging
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from typing import Dict, List, Tuple

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class Config:
    MORADORES_PATH: Path = BASE_DIR / "moradores.csv"
    DOMICILIOS_PATH: Path = BASE_DIR / "domicilios.xlsx"
    DICIONARIO_PATH: Path = BASE_DIR / "dicionario_de_variaveis_pdada_2024_público(1).xlsx"
    LOG_PATH: Path = BASE_DIR / "pdad_app.log"
    SENTINELS: List[int] = [99999, 88888]
    REQUIRED_MORADORES: List[str] = ["A01nficha", "localidade", "id_genero", "renda_ind"]
    REQUIRED_DOMICILIOS: List[str] = ["A01nficha"]
    NUMERIC_COLUMNS: List[str] = ["renda_ind", "idade_calculada", "A01npessoas"]

    @staticmethod
    def carregar_nomes_ras() -> Dict[str, str]:
        """Carrega mapeamento código RA -> nome do dicionário de variáveis."""
        try:
            df_dict = pd.read_excel(Config.DICIONARIO_PATH, sheet_name='Variáveis')
            df_ras = df_dict[df_dict['Coluna'].str.contains('localidade|I08', case=False, na=False)]
            
            nomes = {}
            for _, row in df_ras.iterrows():
                try:
                    codigo = str(int(float(row['Valor'])))
                    nome = row['Descrição do valor']
                    if codigo.isdigit() and 5300 <= int(codigo) <= 5399:
                        nomes[codigo] = nome
                except:
                    pass
            
            if nomes:
                return nomes
        except Exception as e:
            logging.warning(f"Não foi possível carregar nomes das RAs: {e}")
        
        # Fallback: mapeamento básico
        return {
            "5301": "Brasília",
            "5302": "Taguatinga",
            "5303": "Ceilândia",
            "5304": "Gama",
            "5305": "Sobradinho",
            "5306": "Planaltina",
            "5307": "Paranoá",
            "5308": "Núcleo Bandeirante",
            "5309": "Santa Maria",
            "5310": "São Sebastião",
            "5311": "Recanto das Emas",
            "5312": "Lago Sul",
            "5313": "Riacho Fundo",
            "5314": "Lago Norte",
            "5315": "Candangolândia",
            "5316": "Águas Claras",
            "5317": "Riacho Fundo II",
            "5318": "Sudoeste/Octogonal",
            "5319": "Varjão",
            "5320": "Park Way",
            "5321": "SCIA/Estrutural",
            "5322": "Sobradinho II",
            "5323": "Jardim Botânico",
            "5324": "Itapoã",
            "5325": "SIA",
            "5326": "Vicente Pires",
            "5327": "Fercal",
        }

    @staticmethod
    def carregar_niveis_escolaridade() -> Dict[int, str]:
        """Carrega mapeamento de níveis de escolaridade."""
        return {
            1: "Sem instrução",
            2: "Fundamental incompleto",
            3: "Fundamental completo",
            4: "Médio incompleto",
            5: "Médio completo",
            6: "Superior incompleto",
            7: "Superior completo",
            8: "Sem classificação"
        }

def quicksort(arr: List[str]) -> List[str]:
    """Ordenação alfabética manual (D4) para listagem de RAs."""
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

def quicksort_ranking(items: List[Tuple[str, float]], reverse: bool = True) -> List[Tuple[str, float]]:
    """Ordenação manual de ranking de RAs por renda média (D4)."""
    if len(items) <= 1:
        return items
    pivot = items[len(items) // 2][1]
    if reverse:
        left = [item for item in items if item[1] > pivot]
        middle = [item for item in items if item[1] == pivot]
        right = [item for item in items if item[1] < pivot]
    else:
        left = [item for item in items if item[1] < pivot]
        middle = [item for item in items if item[1] == pivot]
        right = [item for item in items if item[1] > pivot]
    return quicksort_ranking(left, reverse) + middle + quicksort_ranking(right, reverse)

class DataEngine:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.df_merged = pd.DataFrame()
        self.cache_stats: Dict[str, Tuple[str, str, str]] = {}
        self.cache_ranking: List[Tuple[str, float]] | None = None
        self.ra_names: Dict[str, str] = config.carregar_nomes_ras()
        self.niveis_escolaridade: Dict[int, str] = config.carregar_niveis_escolaridade()

    def validate_schema(self, df: pd.DataFrame, required_cols: List[str]) -> None:
        missing = [col for col in required_cols if col not in df.columns]
        if missing:
            raise ValueError(f"Colunas essenciais ausentes: {missing}")

    def _validate_paths(self) -> None:
        if not self.config.MORADORES_PATH.is_file():
            raise FileNotFoundError(f"Arquivo de moradores não encontrado: {self.config.MORADORES_PATH}")
        if not self.config.DOMICILIOS_PATH.is_file():
            raise FileNotFoundError(f"Arquivo de domicílios não encontrado: {self.config.DOMICILIOS_PATH}")

    def _clean_numeric_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        for col in self.config.NUMERIC_COLUMNS:
            if col in df.columns:
                df[col] = df[col].replace(self.config.SENTINELS, pd.NA)
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Limpeza específica de gênero
        if 'id_genero' in df.columns:
            df['id_genero'] = df['id_genero'].astype(str).str.strip()
            df['id_genero'] = df['id_genero'].where(
                ~df['id_genero'].isin([str(s) for s in self.config.SENTINELS]),
                pd.NA
            )
        return df

    def carregar_e_limpar(self) -> Tuple[pd.DataFrame, int, int]:
        logging.info("Iniciando carregamento de dados.")
        self._validate_paths()
        self.cache_stats.clear()
        self.cache_ranking = None

        df_mor = pd.read_csv(
            self.config.MORADORES_PATH,
            sep=";",
            decimal=",",
            low_memory=False,
            dtype={'localidade': str, 'id_genero': str, 'A01nficha': str}
        )
        df_dom = pd.read_excel(
            self.config.DOMICILIOS_PATH,
            dtype={'localidade': str, 'A01nficha': str}
        )

        total_mor = len(df_mor)
        total_dom = len(df_dom)

        self.validate_schema(df_mor, self.config.REQUIRED_MORADORES)
        self.validate_schema(df_dom, self.config.REQUIRED_DOMICILIOS)

        df_mor = self._clean_numeric_columns(df_mor)
        df_dom = self._clean_numeric_columns(df_dom)

        self.df_merged = pd.merge(
            df_mor,
            df_dom,
            on="A01nficha",
            how="inner",
            suffixes=("_mor", "_dom"),
        )

        if "localidade_mor" in self.df_merged.columns:
            self.df_merged["localidade"] = self.df_merged["localidade_mor"]
        elif "localidade" not in self.df_merged.columns:
            raise ValueError("Coluna 'localidade' não encontrada após merge")

        self.df_merged["localidade"] = self.df_merged["localidade"].astype("category")
        logging.info(f"Merge concluído: {len(self.df_merged)} registros, {self.df_merged['localidade'].nunique()} RAs.")
        return self.df_merged, total_mor, total_dom

    def ranking_ras_por_renda(self, df: pd.DataFrame) -> List[Tuple[str, float]]:
        if self.cache_ranking is not None:
            return self.cache_ranking
        medias = (
            df.groupby("localidade", observed=True)["renda_ind"]
            .mean()
            .dropna()
        )
        ranking = [(str(ra), float(media)) for ra, media in medias.items()]
        self.cache_ranking = quicksort_ranking(ranking, reverse=True)
        return self.cache_ranking

    def obter_estatisticas(self, df_filtrado: pd.DataFrame, ra: str) -> Tuple[str, str, str]:
        if ra in self.cache_stats:
            return self.cache_stats[ra]
        if df_filtrado.empty:
            return "Sem dados", "Sem dados", "0"
        renda = df_filtrado["renda_ind"].dropna()
        if renda.empty:
            return "Sem dados", "Sem dados", str(len(df_filtrado))
        media = renda.mean()
        mediana = renda.median()
        contagem = len(df_filtrado)
        res = (
            f"Média: R$ {media:,.2f}",
            f"Total: {contagem}",
        )
        self.cache_stats[ra] = res
        return res

    def obter_nome_ra(self, codigo: str) -> str:
        """Retorna nome completo da RA no formato 'código - nome'."""
        nome = self.ra_names.get(codigo, "")
        return f"{codigo} - {nome}" if nome else codigo

class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Gabriel de Oliveira - PDAD 2024 - Recorte B : Renda e Desigualdade")
        self.geometry("1200x850")
        self.configure(bg="#f0f0f0")

        self.config = Config()
        self.engine = DataEngine(self.config)
        self.df = pd.DataFrame()
        self.ranking_ras: List[Tuple[str, float]] = []
        self._label_to_code: Dict[str, str] = {}

        self.style = ttk.Style()
        self.style.configure("TButton", padding=5)
        self.style.configure("TLabel", font=("Arial", 10))
        self.style.configure("Header.TLabel", font=("Arial", 14, "bold"))
        self.style.configure("Title.TLabel", font=("Arial", 16, "bold"))

        self.setup_ui()

    def setup_ui(self) -> None:
        sidebar = ttk.Frame(self, padding="10")
        sidebar.pack(side="left", fill="y", padx=10, pady=10)

        ttk.Label(sidebar, text="Controles", style="Header.TLabel").pack(pady=20)
        self.btn_load = ttk.Button(sidebar, text="📂 Carregar Dados", command=self.thread_load)
        self.btn_load.pack(fill="x", pady=5)

        self.progress = ttk.Progressbar(sidebar, mode='indeterminate')
        self.progress.pack(fill="x", pady=5)

        ttk.Label(sidebar, text="RA Principal:").pack(pady=(15, 0))
        self.ra_var = tk.StringVar()
        self.combo_ra = ttk.Combobox(sidebar, textvariable=self.ra_var, values=[], state="readonly")
        self.combo_ra.pack(fill="x", pady=5)
        self.combo_ra.bind("<<ComboboxSelected>>", lambda _: self.update_plots())

        ttk.Label(sidebar, text="RA Comparação (D2):").pack(pady=(10, 0))
        self.ra_var2 = tk.StringVar()
        self.combo_ra2 = ttk.Combobox(sidebar, textvariable=self.ra_var2, values=[], state="readonly")
        self.combo_ra2.pack(fill="x", pady=5)
        self.combo_ra2.bind("<<ComboboxSelected>>", lambda _: self.update_plots())
        ttk.Button(sidebar, text="Limpar Comparação", command=self.limpar_comparacao).pack(fill="x", pady=2)

        ttk.Separator(sidebar, orient="horizontal").pack(fill="x", pady=10)
        ttk.Button(sidebar, text="📊 Ranking de RAs (D4)", command=self.show_ranking).pack(fill="x", pady=5)
        ttk.Button(sidebar, text="🔍 Ver Detalhes (D5)", command=self.show_details).pack(fill="x", pady=5)
        ttk.Button(sidebar, text="💾 Exportar Relatório", command=self.export_data).pack(fill="x", pady=5)

        self.stats_label = ttk.Label(sidebar, text="Estatísticas:\n---", font=("Arial", 10, "bold"), justify="left")
        self.stats_label.pack(pady=20)

        main_area = ttk.Frame(self, padding="10")
        main_area.pack(side="right", expand=True, fill="both")
        self.notebook = ttk.Notebook(main_area)
        self.notebook.pack(expand=True, fill="both")

        self.tab_graficos = ttk.Frame(self.notebook)
        self.tab_sobre = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_graficos, text="Análise Visual")
        self.notebook.add(self.tab_sobre, text="Sobre o Sistema")

        self.setup_tab_sobre()
        self.setup_tab_graficos()

    def setup_tab_sobre(self) -> None:
        ttk.Label(self.tab_sobre, text="Sistema de Exploração PDAD 2024", style="Title.TLabel").pack(pady=20)
        desc = ("Recorte B: Renda e Desigualdade.\n\n"
                "Este sistema permite analisar a distribuição da renda individual no Distrito Federal,\n"
                "comparar médias por gênero, visualizar histogramas e exportar relatórios.\n"
                "Implementa merge de tabelas, ordenação manual (Quicksort) e tratamento rigoroso de sentinelas.")
        ttk.Label(self.tab_sobre, text=desc, font=("Arial", 11), justify="center").pack(pady=10)
        self.lbl_registos = ttk.Label(self.tab_sobre, text="Aguardando carregamento...", font=("Arial", 12, "bold"))
        self.lbl_registos.pack(pady=20)

    def setup_tab_graficos(self) -> None:
        self.fig = plt.Figure(figsize=(10, 8), dpi=100)
        self.ax1 = self.fig.add_subplot(2, 1, 1)
        self.ax2 = self.fig.add_subplot(2, 1, 2)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.tab_graficos)
        self.canvas.get_tk_widget().pack(expand=True, fill="both")
        self.fig.tight_layout(pad=3.0)

    def thread_load(self) -> None:
        self.btn_load.config(state="disabled")
        self.progress.start(10)
        threading.Thread(target=self.load_data_task, daemon=True).start()

    def load_data_task(self) -> None:
        try:
            df, tot_mor, tot_dom = self.engine.carregar_e_limpar()
            ras_unicas = df["localidade"].dropna().unique().tolist()
            ras_ordenadas = quicksort([str(ra) for ra in ras_unicas])
            ranking = self.engine.ranking_ras_por_renda(df)
            self.after(0, lambda: self._on_data_loaded(df, ras_ordenadas, ranking, tot_mor, tot_dom))
        except Exception as exc:
            logging.error("Erro crítico: %s", exc, exc_info=True)
            error_msg = str(exc)
            self.after(0, lambda: messagebox.showerror("Erro Crítico", f"Erro ao carregar ficheiros: {error_msg}"))
        finally:
            self.after(0, lambda: self.progress.stop())
            self.after(0, lambda: self.btn_load.config(state="normal"))

    def _on_data_loaded(self, df: pd.DataFrame, ras_ordenadas: List[str], ranking: List[Tuple[str, float]], t_mor: int, t_dom: int) -> None:
        self.df = df
        self.ranking_ras = ranking
        self._label_to_code.clear()
        
        labels: List[str] = []
        for codigo in ras_ordenadas:
            label = self.engine.obter_nome_ra(codigo)
            self._label_to_code[label] = codigo
            labels.append(label)

        self.combo_ra.config(values=labels)
        self.combo_ra2.config(values=labels)
        msg = f"{t_mor:,} moradores · {t_dom:,} domicílios"
        self.lbl_registos.config(text=f"Registos carregados:\n{msg}")
        self.notebook.select(self.tab_graficos)
        messagebox.showinfo("Sucesso", "Dados carregados com sucesso!")

    def _selected_ra_code(self) -> str:
        label = self.ra_var.get()
        return self._label_to_code.get(label, label)

    def _filtered_df(self) -> pd.DataFrame:
        codigo = self._selected_ra_code()
        if self.df.empty or not codigo:
            return pd.DataFrame()
        return self.df[self.df["localidade"].astype(str) == codigo]

    def limpar_comparacao(self) -> None:
        self.ra_var2.set("")
        self.update_plots()

    def update_plots(self) -> None:
        df_filt = self._filtered_df()
        if df_filt.empty:
            return
        codigo_ra = self._selected_ra_code()
        label_ra = self.ra_var.get()

        self.ax1.clear()
        self.ax2.clear()

        if "id_genero" in df_filt.columns:
            g1 = df_filt.groupby("id_genero", observed=True)["renda_ind"].mean()
            ra2_codigo = self._selected_ra_code2() if self.ra_var2.get() else None
            df2 = self.df[self.df["localidade"].astype(str) == ra2_codigo] if ra2_codigo else None
            
            if df2 is not None and not df2.empty:
                g2 = df2.groupby("id_genero", observed=True)["renda_ind"].mean()
                all_gen = sorted(set(g1.index) | set(g2.index))
                x = range(len(all_gen))
                h1 = [g1.get(g, 0) for g in all_gen]
                h2 = [g2.get(g, 0) for g in all_gen]
                self.ax1.bar([i - 0.2 for i in x], h1, width=0.4, label=label_ra, color="royalblue")
                self.ax1.bar([i + 0.2 for i in x], h2, width=0.4, label=self.ra_var2.get(), color="darkorange")
                self.ax1.set_xticks(list(x))
                self.ax1.set_xticklabels([f"Gênero {g}" for g in all_gen])
                self.ax1.legend()
            else:
                self.ax1.bar(g1.index.astype(str), g1.values, color="royalblue")
                self.ax1.set_xticklabels([f"Gênero {g}" for g in g1.index])
            self.ax1.set_title(f"Média de Renda por Gênero - {label_ra}")
            self.ax1.set_ylabel("Renda (R$)")

        renda_valida1 = df_filt["renda_ind"].dropna()
        if not renda_valida1.empty:
            r1 = renda_valida1[renda_valida1 <= 20000]
            self.ax2.hist(r1, bins=30, alpha=0.6, label=label_ra, color="royalblue", edgecolor="white")
            self.ax2.axvline(r1.median(), color='blue', linestyle='dashed', linewidth=1.5, label=f'Mediana {label_ra}')
            
            ra2_codigo = self._selected_ra_code2() if self.ra_var2.get() else None
            if ra2_codigo:
                df2 = self.df[self.df["localidade"].astype(str) == ra2_codigo]
                r2 = df2["renda_ind"].dropna()
                r2 = r2[r2 <= 20000]
                self.ax2.hist(r2, bins=30, alpha=0.6, label=self.ra_var2.get(), color="darkorange", edgecolor="white")
                self.ax2.axvline(r2.median(), color='red', linestyle='dashed', linewidth=1.5, label=f'Mediana {self.ra_var2.get()}')
            self.ax2.legend()
            self.ax2.set_title("Distribuição de Renda (Limitado a R$ 20.000)")
            self.ax2.set_xlabel("Renda (R$)")
            self.ax2.set_ylabel("Frequência")

        self.fig.tight_layout()
        self.canvas.draw()

        s1, s2, s3 = self.engine.obter_estatisticas(df_filt, codigo_ra)
        texto_stats = f"Estatísticas ({label_ra}):\n{s1}\n{s2}\n{s3}"
        self.stats_label.config(text=texto_stats)

    def _selected_ra_code2(self) -> str:
        label = self.ra_var2.get()
        return self._label_to_code.get(label, label) if label else ""

    def show_ranking(self) -> None:
        if self.df.empty:
            messagebox.showwarning("Aviso", "Carregue os dados primeiro.")
            return
        top = tk.Toplevel(self)
        top.title("Ranking de RAs por Renda Média (QuickSort - D4)")
        top.geometry("520x520")
        text_area = tk.Text(top, wrap="none", font=("Courier", 10))
        text_area.pack(expand=True, fill="both", padx=10, pady=10)

        lines = ["POS | RA | RENDA MÉDIA (R$)", "-" * 55]
        for pos, (ra, media) in enumerate(self.ranking_ras, start=1):
            rotulo = self.engine.obter_nome_ra(ra)
            lines.append(f"{pos:>3} | {rotulo:<24} | R$ {media:,.2f}")
        text_area.insert(tk.END, "\n".join(lines))
        text_area.config(state=tk.DISABLED)

    def show_details(self) -> None:
        df_filt = self._filtered_df()
        if df_filt.empty:
            messagebox.showwarning("Aviso", "Carregue os dados e selecione uma RA primeiro.")
            return
        codigo_ra = self._selected_ra_code()
        label_ra = self.ra_var.get()
        top = tk.Toplevel(self)
        top.title(f"Detalhes - {label_ra}")
        top.geometry("700x650")

        frame = ttk.Frame(top, padding="20")
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text=f"🏙️ REGIÃO ADMINISTRATIVA: {label_ra}", font=("Arial", 14, "bold")).pack(pady=10)

        posicao = next((idx for idx, (ra, _) in enumerate(self.ranking_ras, start=1) if ra == codigo_ra), None)
        posicao_txt = f"{posicao}º lugar" if posicao else "N/A"
        ttk.Label(frame, text=f"📊 Posição no Ranking de Renda: {posicao_txt}", font=("Arial", 11)).pack(pady=5)

        ttk.Separator(frame, orient="horizontal").pack(fill="x", pady=15)

        ttk.Label(frame, text="👥 DADOS DA POPULAÇÃO", font=("Arial", 12, "bold"), foreground="steelblue").pack(anchor="w", pady=(10, 5))
        total_pessoas = len(df_filt)
        ttk.Label(frame, text=f"Total de moradores pesquisados: {total_pessoas:,}", font=("Arial", 10)).pack(anchor="w", padx=20)

        if 'idade_calculada' in df_filt.columns:
            idade_valida = df_filt['idade_calculada'].dropna()
            if not idade_valida.empty:
                idade_media = idade_valida.mean()
                idade_min = idade_valida.min()
                idade_max = idade_valida.max()
                ttk.Label(frame, text=f"Idade média: {idade_media:.1f} anos", font=("Arial", 10)).pack(anchor="w", padx=20)
                ttk.Label(frame, text=f"Faixa etária: {idade_min:.0f} a {idade_max:.0f} anos", font=("Arial", 10)).pack(anchor="w", padx=20)

        ttk.Separator(frame, orient="horizontal").pack(fill="x", pady=15)

        ttk.Label(frame, text=" DADOS DE RENDA", font=("Arial", 12, "bold"), foreground="green").pack(anchor="w", pady=(10, 5))
        renda = df_filt['renda_ind'].dropna()
        if not renda.empty:
            media = renda.mean()
            minimo = renda.min()
            maximo = renda.max()
            sem_renda = (renda == 0).sum()
            pct_sem_renda = (sem_renda / len(renda) * 100) if len(renda) > 0 else 0

            ttk.Label(frame, text=f"Renda média mensal: R$ {media:,.2f}", font=("Arial", 10)).pack(anchor="w", padx=20)
            ttk.Label(frame, text=f"Menor renda registrada: R$ {minimo:,.2f}", font=("Arial", 10)).pack(anchor="w", padx=20)
            ttk.Label(frame, text=f"Maior renda registrada: R$ {maximo:,.2f}", font=("Arial", 10)).pack(anchor="w", padx=20)
            ttk.Label(frame, text=f"Pessoas sem renda: {sem_renda:,} ({pct_sem_renda:.1f}%)", font=("Arial", 10)).pack(anchor="w", padx=20)

        ttk.Separator(frame, orient="horizontal").pack(fill="x", pady=15)

        if 'escolaridade' in df_filt.columns:
            ttk.Label(frame, text="📚 NÍVEL DE ESCOLARIDADE", font=("Arial", 12, "bold"), foreground="purple").pack(anchor="w", pady=(10, 5))
            escolaridade_counts = df_filt['escolaridade'].value_counts()
            total = len(df_filt)

            for codigo, quantidade in escolaridade_counts.items():
                try:
                    codigo_int = int(float(codigo))
                    nome_nivel = self.engine.niveis_escolaridade.get(codigo_int, f"Nível {codigo}")
                    percentual = (quantidade / total * 100) if total > 0 else 0
                    ttk.Label(frame, text=f"{nome_nivel}: {quantidade:,} pessoas ({percentual:.1f}%)", font=("Arial", 10)).pack(anchor="w", padx=20)
                except:
                    pass

        ttk.Separator(frame, orient="horizontal").pack(fill="x", pady=15)

        ttk.Label(frame, text="⭐ MAIORES RENDAS (Top 10)", font=("Arial", 12, "bold"), foreground="orange").pack(anchor="w", pady=(10, 5))
        top10 = df_filt[['renda_ind']].dropna().sort_values('renda_ind', ascending=False).head(10)
        for i, (_, row) in enumerate(top10.iterrows(), 1):
            ttk.Label(frame, text=f"{i}º lugar: R$ {row['renda_ind']:,.2f}", font=("Arial", 10)).pack(anchor="w", padx=20)

        ttk.Button(frame, text="Fechar", command=top.destroy).pack(pady=20)

    def export_data(self) -> None:
        df_filt = self._filtered_df()
        if df_filt.empty:
            messagebox.showwarning("Aviso", "Carregue os dados e selecione uma RA primeiro.")
            return
        codigo_ra = self._selected_ra_code()
        label_ra = self.ra_var.get()

        total_moradores = len(df_filt)

        idade_media = 0.0
        if 'idade_calculada' in df_filt.columns:
            idade_valida = df_filt['idade_calculada'].dropna()
            if not idade_valida.empty:
                idade_media = idade_valida.mean()

        escolaridade_mais_comum = "Não disponível"
        if 'escolaridade' in df_filt.columns:
            escolaridade_valida = df_filt['escolaridade'].dropna()
            if not escolaridade_valida.empty:
                escolaridade_contagens = escolaridade_valida.value_counts()
                if not escolaridade_contagens.empty:
                    codigo_top = int(float(escolaridade_contagens.index[0]))
                    escolaridade_mais_comum = self.engine.niveis_escolaridade.get(codigo_top, f"Nível {codigo_top}")

        percentual_superior = 0.0
        if 'escolaridade' in df_filt.columns:
            total = len(df_filt)
            if total > 0:
                superior_count = (df_filt['escolaridade'] == '7').sum()
                percentual_superior = (superior_count / total) * 100

        relatorio = f"""RELATÓRIO PDAD 2024
Região Administrativa: {label_ra}
Total de moradores: {total_moradores}
Idade média: {idade_media:.1f}
Escolaridade mais comum: {escolaridade_mais_comum}
Percentual com superior completo: {percentual_superior:.2f}%
"""

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Salvar Relatório"
        )
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(relatorio)
            messagebox.showinfo("Sucesso", f"Relatório exportado com sucesso:\n{file_path}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
