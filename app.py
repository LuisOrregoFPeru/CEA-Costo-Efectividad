import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="CEA • Costo-Efectividad", layout="wide")
st.title("7️⃣ CEA • Costo-Efectividad")

def descarga_csv(df: pd.DataFrame, nombre: str):
    csv = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button("Descargar CSV", csv, file_name=f"{nombre}.csv", mime="text/csv")

st.header("7️⃣ Costo-Efectividad (CEA)")

st.caption("Ingresa costo total y efectividad (p. ej., tasa de respuesta, casos evitados, AVAD evitados, etc.).")
df0 = pd.DataFrame({
    "Tratamiento": ["A", "B", "C"],
    "Costo total": [0.0, 10000.0, 22000.0],
    "Efectividad": [0.0, 0.40, 0.55]
})
tx = st.data_editor(df0, num_rows="dynamic", key="cea_tx")

if tx.shape[0] >= 2:
    if (tx["Costo total"] < 0).any():
        st.error("Hay costos negativos. Ajusta los datos.")
    elif (tx["Efectividad"] < 0).any():
        st.error("Hay efectividades negativas. Ajusta los datos.")
    else:
        df = tx.copy().reset_index(drop=True)
        df = df.sort_values("Efectividad").reset_index(drop=True)
        df["ΔCosto"] = df["Costo total"].diff()
        df["ΔEfect"] = df["Efectividad"].diff()
        df["ICER"]   = df.apply(
            lambda r: (r["ΔCosto"] / r["ΔEfect"]) if r["ΔEfect"] and r["ΔEfect"] > 0 else np.nan,
            axis=1
        )

        st.subheader("Tabla incremental (ordenada por efectividad)")
        st.dataframe(df, hide_index=True, use_container_width=True)

        fig, ax = plt.subplots()
        ax.scatter(df["Efectividad"], df["Costo total"])
        for i, r in df.iterrows():
            ax.annotate(r["Tratamiento"], (r["Efectividad"], r["Costo total"]))
        ax.set_xlabel("Efectividad")
        ax.set_ylabel("Costo total (U.M.)")
        ax.set_title("Plano Costo-Efectividad (CEA)")
        st.pyplot(fig)

        descarga_csv(df, "CEA_resultados")
else:
    st.info("Agrega al menos 2 tratamientos.")
