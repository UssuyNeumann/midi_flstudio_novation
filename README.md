## SCRIPT PYTHON PARA DAW FLSTUDIO CONTROLAR TECLADO MIDI DA NOVATION CRIADO COM AUXILIO DE IA

VIDEO DEMONSTRAÇÂO: https://www.youtube.com/watch?v=dr8jpy4Y37A


## Mapa de Controles - Novation Launchkey Mini Mk1 (FL Studio)

## 1. Controles Fixos (Funcionam em qualquer modo)
* **Botão `InControl`:** Mantenha sempre **aceso** para o script controlar os LEDs e funções.
* **Botão Redondo de Cima** *(ao lado do Pad 8)*: **Play / Pause** rápido.
* **Botão Redondo de Baixo** *(ao lado do Pad 16)*: Abre ou fecha a **Tela de Menu** para trocar de modo.
* **Setas (`<` / `>` ou `Track`):** Trocam o **instrumento selecionado** (cima/baixo) no Channel Rack.

---

## 2. Tela de Menu (Ao apertar o Botão Redondo de Baixo)
Quando você abre o menu, os pads de baixo acendem em cores diferentes para você escolher o modo de trabalho:

| Pad | Cor no LED | Modo Ativado |
| :--- | :--- | :--- |
| **Pad 9** | Verde | **Channel Rack** (Sequenciador de passos) |
| **Pad 10** | Âmbar | **Mixer** (Volume e Mute das faixas) |
| **Pad 11** | Vermelho | **Transporte** (Play, Stop, Rec, Metrônomo) |
| **Pad 12** | Âmbar | **Drums** (16 pads de bateria / FPC) |
| **Pad 13** | Verde | **Piano Visual** (Teclas brancas e pretas nos pads) |

---

## 3. Mapa Detalhado de Cada Modo

### Modo 1: Channel Rack (Pad 9 - Verde)
* **8 Knobs:** Controlam o **volume** dos 8 primeiros canais do Channel Rack.
* **16 Pads:** Ligam e desligam as notas (**steps 1 a 16**) do instrumento selecionado.
  * **Verde:** Nota ativada.
  * **Vermelho:** Cursor da música passando em um espaço vazio.
  * **Âmbar:** Nota ativada tocando naquele exato instante.
  * **Apagado:** Espaço vazio.

### Modo 2: Mixer (Pad 10 - Âmbar)
* **8 Knobs:** Controlam o **volume (fader)** dos canais **1 a 8** do Mixer.
* **Pads 1 a 8 (fileira de cima):** **Mute / Unmute** dos canais 1 a 8 do Mixer (**Verde** = canal ativo / **Apagado** = canal mutado).
* **Pads 9 a 16 (fileira de baixo):** Sem função (apagados).

### Modo 3: Transporte (Pad 11 - Vermelho)
* **8 Knobs:** Controlam o **volume** dos canais **1 a 8** do Mixer.
* **Pads 1 a 8 (fileira de cima):**
  * **Pad 1:** Play / Pause *(Verde tocando, Âmbar pausado)*
  * **Pad 2:** Stop *(Vermelho)*
  * **Pad 3:** Record / Gravar *(Vermelho gravando, Âmbar em espera)*
  * **Pad 4:** Alternar modo **Pattern / Song** *(Âmbar)*
  * **Pad 5:** Ligar / Desligar **Metrônomo** *(Âmbar)*
  * **Pad 6:** **Desfazer (Undo)** *(Âmbar)*
  * **Pad 7:** **Quantizar** notas do canal atual *(Âmbar)*
  * **Pad 8:** **Tap Tempo** *(Âmbar)*

### Modo 4: Drums / Bateria (Pad 12 - Âmbar)
* **8 Knobs:** Controlam o **volume** dos canais **1 a 8** do Mixer.
* **16 Pads:** Tocam notas cromáticas sequenciais de **C3 a D#4** no instrumento selecionado (ideal para **FPC**, **Slicex** ou kits de bateria). Os pads acendem em **Âmbar** enquanto são pressionados.

### Modo 5: Piano Visual (Pad 13 - Verde)
* **8 Knobs:** Controlam o **volume** dos canais **1 a 8** do Mixer.
* **Fileira de Cima (Teclas Pretas em Âmbar):**
  * **Pad 1:** Apagado | **Pad 2:** `Dó#` | **Pad 3:** `Ré#` | **Pad 4:** Apagado | **Pad 5:** `Fá#` | **Pad 6:** `Sol#` | **Pad 7:** `Lá#` | **Pad 8:** Apagado
* **Fileira de Baixo (Teclas Brancas em Verde):**
  * **Pad 9:** `Dó` | **Pad 10:** `Ré` | **Pad 11:** `Mi` | **Pad 12:** `Fá` | **Pad 13:** `Sol` | **Pad 14:** `Lá` | **Pad 15:** `Si` | **Pad 16:** `Dó` (uma oitava acima)
* *(Ao tocar qualquer tecla, o pad pisca em **Vermelho**).*
