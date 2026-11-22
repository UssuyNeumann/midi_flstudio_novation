# name=Novation Launchkey Mini Mk1 Multi-Mode
import device
import mixer
import channels
import transport
import general

# Mapeamento MIDI oficial do Launchkey Mini Mk1 (Modo InControl)
KNOBS = list(range(21, 29))
PADS_TOP = list(range(96, 104))
PADS_BOT = list(range(112, 120))
ALL_PADS = PADS_TOP + PADS_BOT

# Botões Redondos à direita dos pads no Mini Mk1 (Notas 104 e 120)
BTN_ROUND_TOP = 104  # Botão redondo de cima -> Play / Pause rápido
BTN_ROUND_BOT = 120  # Botão redondo de baixo -> Abrir/Fechar MENU

# Setas de navegação do Mini Mk1 (CCs 104 a 107)
ARROW_UP = 104
ARROW_DOWN = 105
ARROW_LEFT = 106
ARROW_RIGHT = 107

# Cores dos LEDs no Launchkey Mini Mk1
COLOR_OFF = 12
COLOR_GREEN = 60
COLOR_AMBER = 63
COLOR_RED = 15

# Estados de Modo
MODE_MENU = 0
MODE_CHANNEL_RACK = 1
MODE_MIXER = 2
MODE_TRANSPORT = 3
MODE_DRUMS = 4
MODE_PIANO = 5

current_mode = MODE_CHANNEL_RACK

# Notas MIDI: Bateria (C3 a D#4)
DRUM_NOTES = list(range(48, 64))

# Layout visual de Piano alinhado (16 pads):
# Cima (0..7):  [1: Off] [2: C#] [3: D#] [4: Off] [5: F#] [6: G#] [7: A#] [8: Off]
# Baixo (8..15): [9: C]   [10: D] [11: E] [12: F]  [13: G] [14: A] [15: B] [16: C5]
PIANO_NOTES = [
    -1, 61, 63, -1, 66, 68, 70, -1,  # Fileira de cima (Pads 2-3 e Pads 5-6-7)
    60, 62, 64, 65, 67, 69, 71, 72   # Fileira de baixo (Pads 9 a 16)
]

def OnInit():
    device.midiOutMsg(0x90, 0, 12, 127)
    update_leds()

def OnDeInit():
    device.midiOutMsg(0x90, 0, 12, 0)

def OnMidiMsg(event):
    global current_mode
    event.handled = False
    status_type = event.status & 0xF0

    # --- 1. KNOBS (Dependem do Modo Atual) ---
    if status_type == 0xB0 and event.data1 in KNOBS:
        idx = KNOBS.index(event.data1)
        val = event.data2 / 127.0
        
        if current_mode == MODE_CHANNEL_RACK:
            if idx < channels.channelCount():
                channels.setChannelVolume(idx, val)
        else:
            mixer.setTrackVolume(idx + 1, val * 0.8)
        event.handled = True
        return

    # --- 2. BOTÕES REDONDOS À DIREITA DOS PADS (Note On 104 e 120) ---
    if status_type == 0x90 and event.data2 > 0:
        if event.data1 == BTN_ROUND_BOT:
            current_mode = MODE_MENU if current_mode != MODE_MENU else MODE_CHANNEL_RACK
            update_leds()
            event.handled = True
            return
        elif event.data1 == BTN_ROUND_TOP:
            transport.start()
            update_leds()
            event.handled = True
            return

    # --- 3. SETAS DE NAVEGAÇÃO (CCs 104-107) ---
    if status_type == 0xB0 and event.data2 > 0:
        if event.data1 in (ARROW_UP, ARROW_LEFT):
            channels.selectOneChannel(max(0, channels.channelNumber() - 1))
            update_leds()
            event.handled = True
            return
        elif event.data1 in (ARROW_DOWN, ARROW_RIGHT):
            channels.selectOneChannel(min(channels.channelCount() - 1, channels.channelNumber() + 1))
            update_leds()
            event.handled = True
            return

    # --- 4. PADS (Note On e Note Off) ---
    if status_type in (0x90, 0x80) and event.data1 in ALL_PADS:
        pad_idx = ALL_PADS.index(event.data1)
        is_press = (status_type == 0x90 and event.data2 > 0)
        chan = channels.channelNumber()

        # TELA DE MENU (Pads 9 a 13 escolhem o modo)
        if current_mode == MODE_MENU and is_press:
            if pad_idx == 8:    current_mode = MODE_CHANNEL_RACK
            elif pad_idx == 9:  current_mode = MODE_MIXER
            elif pad_idx == 10: current_mode = MODE_TRANSPORT
            elif pad_idx == 11: current_mode = MODE_DRUMS
            elif pad_idx == 12: current_mode = MODE_PIANO
            update_leds()
            event.handled = True
            return

        # MODO 1: CHANNEL RACK (Sequenciador de 16 steps)
        elif current_mode == MODE_CHANNEL_RACK and is_press:
            channels.setGridBit(chan, pad_idx, not channels.getGridBit(chan, pad_idx))
            update_leds()
            event.handled = True

        # MODO 2: MIXER (Pads 1 a 8 mutam/desmutam tracks 1 a 8)
        elif current_mode == MODE_MIXER and is_press:
            if pad_idx < 8:
                mixer.muteTrack(pad_idx + 1)
                update_leds()
            event.handled = True

        # MODO 3: TRANSPORTE (Pads 1 a 8 controlam playback e gravação)
        elif current_mode == MODE_TRANSPORT and is_press:
            if pad_idx == 0:   transport.start()
            elif pad_idx == 1: transport.stop()
            elif pad_idx == 2: transport.record()
            elif pad_idx == 3: transport.setLoopMode()
            elif pad_idx == 4: transport.globalTransport(110, 1) # Metrônomo
            elif pad_idx == 5: general.undo()
            elif pad_idx == 6: channels.quickQuantize(chan)
            elif pad_idx == 7: transport.globalTransport(106, 1) # Tap Tempo
            update_leds()
            event.handled = True

        # MODO 4: DRUMS (Tocar notas no instrumento atual)
        elif current_mode == MODE_DRUMS:
            note = DRUM_NOTES[pad_idx]
            vel = event.data2 if is_press else 0
            channels.midiNoteOn(chan, note, vel)
            device.midiOutMsg(0x90, 0, event.data1, COLOR_AMBER if is_press else COLOR_OFF)
            event.handled = True

        # MODO 5: PIANO VISUAL (Teclas Brancas e Pretas nos pads)
        elif current_mode == MODE_PIANO:
            note = PIANO_NOTES[pad_idx]
            if note != -1:
                vel = event.data2 if is_press else 0
                channels.midiNoteOn(chan, note, vel)
                # Acende em vermelho ao apertar e volta para a cor da tecla ao soltar
                default_color = COLOR_AMBER if pad_idx < 8 else COLOR_GREEN
                device.midiOutMsg(0x90, 0, event.data1, COLOR_RED if is_press else default_color)
            event.handled = True

def OnUpdateBeatIndicator(value):
    if current_mode == MODE_CHANNEL_RACK:
        update_leds()

def OnDirtyChannel(index, flag):
    if current_mode == MODE_CHANNEL_RACK:
        update_leds()

def update_leds():
    if not device.isAssigned():
        return

    chan = channels.channelNumber()
    current_step = mixer.getSongStepPos() % 16

    for i, pad_note in enumerate(ALL_PADS):
        color = COLOR_OFF

        if current_mode == MODE_MENU:
            if i == 8:    color = COLOR_GREEN  # Pad 9: Channel Rack
            elif i == 9:  color = COLOR_AMBER  # Pad 10: Mixer
            elif i == 10: color = COLOR_RED    # Pad 11: Transporte
            elif i == 11: color = COLOR_AMBER  # Pad 12: Drums
            elif i == 12: color = COLOR_GREEN  # Pad 13: Piano Visual

        elif current_mode == MODE_CHANNEL_RACK:
            is_active = channels.getGridBit(chan, i)
            is_playing = (i == current_step)
            if is_playing and is_active: color = COLOR_AMBER
            elif is_playing:             color = COLOR_RED
            elif is_active:              color = COLOR_GREEN

        elif current_mode == MODE_MIXER:
            if i < 8:
                color = COLOR_OFF if mixer.isTrackMuted(i + 1) else COLOR_GREEN

        elif current_mode == MODE_TRANSPORT:
            if i == 0:   color = COLOR_GREEN if transport.isPlaying() else COLOR_AMBER
            elif i == 1: color = COLOR_RED
            elif i == 2: color = COLOR_RED if transport.isRecording() else COLOR_AMBER
            elif i in range(3, 8): color = COLOR_AMBER

        elif current_mode == MODE_PIANO:
            if PIANO_NOTES[i] != -1:
                # Teclas pretas em cima (Âmbar) e teclas brancas embaixo (Verde)
                color = COLOR_AMBER if i < 8 else COLOR_GREEN

        device.midiOutMsg(0x90, 0, pad_note, color)
