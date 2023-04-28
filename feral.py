import array
import ctypes
import wowsims

class Spells():
    Berserk = None
    Bite = None
    FFF = None
    Fury = None
    Mangle = None
    Rake = None
    Roar = None
    Rip = None
    Shred = None

    @classmethod
    def register(cls):
        """Map from spell id to spellbook index and stores the result in a global with the spell's name."""
        num_spells = wowsims.getSpellCount()
        spells = array.array('I', [0] * num_spells)
        spells_ptr = (ctypes.c_int * len(spells)).from_buffer(spells)
        wowsims.getSpells(spells_ptr, len(spells))
        for i, spell in enumerate(spells):
            if spell == 50334 and cls.Berserk is None: cls.Berserk = i
            if spell == 48577 and cls.Bite is None: cls.Bite = i
            if spell == 16857 and cls.FFF is None: cls.FFF = i
            if spell == 50213 and cls.Fury is None: cls.Fury = i
            if spell == 71925 and cls.Mangle is None: cls.Mangle = i
            if spell == 48574 and cls.Rake is None: cls.Rake = i
            if spell == 52610 and cls.Roar is None: cls.Roar = i
            if spell == 49800 and cls.Rip is None: cls.Rip = i
            if spell == 48572 and cls.Shred is None: cls.Shred = i

class Auras():
    Labels = ["Berserk", "Cat Form", "Clearcasting", "Savage Roar Aura", "Tiger's Fury Aura"]
    Durations = array.array('d', [0.0] * len(Labels))

    @classmethod
    def register(cls):
        ptr = (ctypes.c_char_p * (len(cls.Labels)+1))()
        ptr[:-1] = [label.encode('utf-8') for label in cls.Labels]
        ptr[-1] = None
        wowsims.registerAuras(ptr)
    
    @classmethod
    def update(cls):
        ptr = (ctypes.c_double * len(cls.Durations)).from_buffer(cls.Durations)
        wowsims.getAuras(ptr, len(cls.Durations))
    
    @classmethod
    def get_dur(cls, label):
        return cls.Durations[cls.Labels.index(label)]

class TargetAuras():
    Labels = ["Rake", "Rip", "Mangle"]
    Durations = array.array('d', [0.0] * len(Labels))

    @classmethod
    def register(cls):
        ptr = (ctypes.c_char_p * (len(cls.Labels)+1))()
        ptr[:-1] = [label.encode('utf-8') for label in cls.Labels]
        ptr[-1] = None
        wowsims.registerTargetAuras(ptr)
    
    @classmethod
    def update(cls):
        ptr = (ctypes.c_double * len(cls.Durations)).from_buffer(cls.Durations)
        wowsims.getTargetAuras(ptr, len(cls.Durations))

    @classmethod
    def get_dur(cls, label):
        return cls.Durations[cls.Labels.index(label)]