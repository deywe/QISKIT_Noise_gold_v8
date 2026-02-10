# ==================================================================================
# 🐦 HARPIA QUANTUM LABS - PLAYER EDITION (STABLE RENDER)
# 💎 Edition: ETHEREAL DIAMOND v8.0 (Visualizer Only)
# ----------------------------------------------------------------------------------
# "Correção de compatibilidade de Glyphs para Linux/Pop!_OS."
# ==================================================================================

import matplotlib
try:
    matplotlib.use('Qt5Agg')
except:
    matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
import numpy as np
import sys
import warnings

# Silencia avisos de fontes para manter o terminal limpo
warnings.filterwarnings("ignore", category=UserWarning)

def harpia_player_v8(csv_path="telemetria_ethereal_gold_v8.csv"):
    print(f"\n[LOADING] Telemetria: {csv_path}...")
    
    try:
        df_sim = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"❌ Erro: Arquivo '{csv_path}' não encontrado.")
        return

    qubit_cols = [col for col in df_sim.columns if col.endswith('_x')]
    n_qubits = len(qubit_cols)
    total_frames = len(df_sim)

    # Parâmetros Geométricos
    R_TORO, r_TORO, F_ACHAT = 21.0, 2.5, 0.000001
    
    print(f"[OK] Qubits: {n_qubits} | Frames: {total_frames}")

    fig = plt.figure(figsize=(16, 12), facecolor='#050505')
    ax = fig.add_subplot(111, projection='3d', facecolor='#050505')
    ax.axis('off')
    ax.set_box_aspect([1, 1, 0.3]) 

    # Wireframe
    u, v = np.mgrid[0:2*np.pi:100j, 0:2*np.pi:50j]
    x_t = (R_TORO + r_TORO * np.cos(v)) * np.cos(u)
    y_t = (R_TORO + r_TORO * np.cos(v)) * np.sin(u)
    z_t = (r_TORO * F_ACHAT) * np.sin(v)
    ax.plot_wireframe(x_t, y_t, z_t, color='#00FFFF', alpha=0.18, linewidth=0.4)

    alpha_qubit = 0.4 if n_qubits > 500 else 0.8
    marker_size = 2 if n_qubits > 500 else 6
    cores = plt.cm.cool(np.linspace(0, 1, n_qubits))
    
    lasers = [ax.plot([], [], [], color=cores[i], lw=1.0, alpha=alpha_qubit)[0] for i in range(n_qubits)]
    pontos = [ax.plot([], [], [], 'o', color='white', markersize=marker_size, alpha=1.0)[0] for i in range(n_qubits)]
    
    # Usando fonte 'monospace' para visual de terminal
    texto_info = ax.text2D(0.02, 0.98, '', transform=ax.transAxes, 
                           color='white', fontsize=11, fontfamily='monospace', weight='bold')

    def update(frame):
        row = df_sim.iloc[frame]
        
        # Substituímos os Emojis por identificadores de texto (Tags)
        if abs(row.get('Ruido_Vibracional', 0)) > 0.3:
            status_cor, status_txt = '#FF0055', "!! INERTIA LOCK !!"
        elif row.get('Caos_Fenix', 0) < 0.9 * row.get('Caos_Original', 0): 
            status_cor, status_txt = '#00FFFF', "<> FENIX DIAMOND <>"
        else:
            status_cor, status_txt = '#FFFFFF', ">> VR ETHEREAL <<"
        
        s_cols = [col for col in df_sim.columns if col.endswith('_S')]
        s_medio = row[s_cols].mean()
        q_tag = " [QISKIT]" if abs(row.get('Fluxo_Qiskit', 0)) > 0 else ""

        texto_info.set_text(
            f"[{status_txt}{q_tag}]\n"
            f"FRAME: {frame}/{total_frames}\n"
            f"COERENCIA: {s_medio:.4%} | QUBITS: {n_qubits}"
        )
        texto_info.set_color(status_cor)
        
        for i in range(n_qubits):
            lookback_val = 10 if n_qubits > 500 else 25
            lookback = max(0, frame - lookback_val)
            trail = df_sim.iloc[lookback:frame+1]
            
            lasers[i].set_data(trail[f'q{i}_x'], trail[f'q{i}_y'])
            lasers[i].set_3d_properties(trail[f'q{i}_z'])
            
            pontos[i].set_data([row[f'q{i}_x']], [row[f'q{i}_y']])
            pontos[i].set_3d_properties([row[f'q{i}_z']])
        
        ax.view_init(elev=35, azim=frame * 0.5)
        return lasers + pontos + [texto_info]

    fig.suptitle(
        'HARPIA QUANTUM PLAYER - ETHEREAL DIAMOND v8.0\n' +
        f'OFFLINE DATASET VISUALIZER | N={n_qubits}',
        color='white', fontsize=14, fontweight='bold', y=0.96
    )

    ani = FuncAnimation(fig, update, frames=total_frames, interval=20, blit=False)
    plt.show()

if __name__ == "__main__":
    file_target = sys.argv[1] if len(sys.argv) > 1 else "telemetria_ethereal_gold_v8.csv"
    harpia_player_v8(file_target)