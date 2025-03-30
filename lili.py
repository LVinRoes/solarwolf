import subprocess
import os

pfad = r"D:\BA-Arbeit2\output_score.ly"

# PDF kompilieren
subprocess.run(["lilypond", pfad])

# Optional: PDF öffnen (Windows-Beispiel)
pdf_datei = pfad.replace(".ly", ".pdf")
if os.path.exists(pdf_datei):
    subprocess.run(["start", pdf_datei], shell=True)
