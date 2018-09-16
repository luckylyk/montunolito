import json
from scipy.io.wavfile import write

from montunolito.libs.qt.shortcuts import set_shortcut
from montunolito.libs.qt.dialogs import save_dialog, open_dialog
from montunolito.converters.musicxml.convert import convert_to_musicxml
from montunolito.converters.midi.convert import convert_to_midi
from montunolito.converters.wav.convert import convert_sequence_to_int16

from sequencereader.widgets import SequenceReaderWidget
from sequencereader.rules import Signature


TITLE = 'Sequence Reader'


class SequenceReader():
    def __init__(self, sequence):
        self.signature = Signature()
        self.signature.set_values(tonality='A', mode='minor')

        self.view = SequenceReaderWidget(sequence, self.signature)
        self.view.setWindowTitle(TITLE)

        self.view.menu.openSequenceRequested.connect(self.open)
        self.view.menu.saveSequenceRequested.connect(self.save)
        self.view.menu.exportWavRequested.connect(self.export_wav)
        self.view.menu.exportMidiRequested.connect(self.export_mid)
        self.view.menu.exportXmlRequested.connect(self.export_xml)
        self.view.menu.tonalityChanged.connect(self.set_tonality)
        self.view.menu.modeChanged.connect(self.set_mode)

        set_shortcut("Ctrl+O", self.view, self.open)
        set_shortcut("Ctrl+S", self.view, self.save)

    def set_signature_values(self, tonality=None, mode=None):
        if tonality:
            self.set_tonality(tonality)
        if mode:
            self.set_mode(mode)

    def show(self):
        self.view.show()

    def save(self):
        sequence = self.view.musicsheet.sequence
        filename = save_dialog(filter_='mms')
        if not filename:
            return
        with open(filename, 'w') as f:
            json.dump(sequence, f, indent=2)

    def open(self):
        filename = open_dialog(filter_='mms')
        if not filename:
            return
        with open(filename, 'r') as f:
            sequence = json.load(f)
        self.view.musicsheet.set_sequence(sequence)

    def export_wav(self):
        sequence = self.view.musicsheet.sequence
        fileoutput = save_dialog(filter_='wav')
        if not fileoutput:
            return
        sound_array = convert_sequence_to_int16(sequence)
        write(fileoutput, 44100, sound_array)

    def export_xml(self):
        sequence = self.view.musicsheet.sequence
        fileoutput = save_dialog(filter_='xml')
        if not fileoutput:
            return

        xmlcontent = convert_to_musicxml(sequence, tempo=160)
        with open(fileoutput, 'w') as myfile:
            myfile.write(xmlcontent)

    def export_mid(self):
        sequence = self.view.musicsheet.sequence
        fileoutput = save_dialog(filter_='mid')
        if not fileoutput:
            return

        midifile = convert_to_midi(sequence, tempo=160)
        with open(fileoutput, 'wb') as myfile:
            midifile.writeFile(myfile)

    def set_tonality(self, value):
        self.signature.set_values(tonality=value)
        self.view.musicsheet.update()

    def set_mode(self, value):
        self.signature.set_values(mode=value)
        self.view.musicsheet.update()