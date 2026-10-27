# Gunther - Desktop Companion 🐹❤️

Un piccolo compagno virtuale dedicato a Gunther, creato con affetto per passeggiare sullo schermo del computer, tenere compagnia e donare un sorriso ogni volta che lo si guarda.

![Gunther Preview](assets/gunther_preview.gif)

---

## ✨ Funzionalità

- **Animazioni Dolci e Dettagliate**:
  - 🌸 **Idle**: Respira pacificamente, arriccia il nasino e muove le orecchie.
  - 🚶 **Passeggiata**: Cammina dolcemente avanti e indietro lungo la barra delle applicazioni.
  - 🌻 **Sgranocchia**: Quando ha fame, si siede sulle zampe posteriori e mangia un semino di girasole.
  - 💤 **Pisolino**: Si rannicchia in una morbida pallina con tanto di "Zzz" animate.
  - 🐾 **Coccole**: Se ci clicchi sopra, chiude gli occhi felice, arrossisce ed emette cuoricini fluttuanti.
  - 🪂 **Prendi e Trascina**: Puoi sollevarlo con il mouse (zampette a penzoloni!) e rilasciarlo: scenderà delicatamente grazie alla gravità.

- **Pensieri Dolci**:
  - Ogni tanto compare un fumetto delicato con frasi confortanti, ricordi d'idratazione e parole d'affetto.
  - Tutti i messaggi sono integrati nel codice in [gunther/messages.py](file:///C:/Users/simem/Desktop/GIT/gunther/gunther/messages.py) e incorporati nell'eseguibile.

- **Varianti di Manto**:
  - 🐹 **Gunther (Manto Originale)**: Pelo grigio scuro caldo, pancino bianco candido e visetto pulito senza baffi.
  - 🌰 **Dorato Classico (Siriano)**
  - ❄️ **Bianco Invernale (Snow / Winter White)**
  - 🪨 **Grigio Zaffiro (Russo)**
  - 🐼 **Panda Pezzato**

- **Integrazione Tray**:
  - Icona nella barra di sistema (vicino all'orologio di Windows) per richiamarlo, dargli un semino o svegliarlo.

---

## 🎮 Comandi e Interazioni

| Azione | Risultato |
| :--- | :--- |
| **Clic Sinistro** | Fai una coccola a Gunther (arrossisce e genera cuori) |
| **Doppio Clic** | Dagli subito un semino di girasole da sgranocchiare |
| **Clic e Trascina** | Sollevalo e spostalo ovunque sullo schermo |
| **Clic Destro** | Apre il menu completo (cambio manto, dimensioni, cibo, sonno, impostazioni) |
| **Doppio Clic su Tray** | Riporta Gunther immediatamente al centro dello schermo |

---

## 🚀 Come Avviarlo

### Metodo 1: File Eseguibile Autonomo (Consigliato per lei!)
Trovi il file pronto all'uso in `dist/Gunther.exe`.
- **100% Autonomo e Pulito**: Non genera né legge alcun file `.json` su disco; impostazioni, animazioni e messaggi sono tutti integrati direttamente all'interno dell'eseguibile.
- Le basterà fare doppio clic su `Gunther.exe` e Gunther comparirà subito sullo schermo senza installare nulla!

### Metodo 2: Doppio Clic sullo Script
Fai doppio clic su `Avvia_Gunther.bat` (avvia l'app in background senza finestre nere di terminale).

### Metodo 3: Da Riga di Comando
```powershell
uv run main.py
```

---

## 🔨 Come Compilare l'Eseguibile (.exe)

Puoi ricompilare l'applicazione in qualsiasi momento usando lo script [build.py](file:///C:/Users/simem/Desktop/GIT/gunther/build.py).

### 🐹 Build con SOLO il colore Gunther (Consigliata)
Per creare un eseguibile dedicato al 100% a Gunther (senza gli altri manti e senza la voce di cambio colore nel menu):

```powershell
uv run build.py --gunther-only
```
*(Oppure fai doppio clic sul file [Build_Gunther_Solo.bat](file:///C:/Users/simem/Desktop/GIT/gunther/Build_Gunther_Solo.bat))*

### 🎨 Build con TUTTI i manti
Se preferisci includere tutte le varianti di colore alternative:

```powershell
uv run build.py
```
*(Oppure fai doppio clic sul file [Build_Completo.bat](file:///C:/Users/simem/Desktop/GIT/gunther/Build_Completo.bat))*

L'eseguibile generato si troverà sempre nella cartella `dist/Gunther.exe` e funzionerà come singolo file completamente autonomo.
