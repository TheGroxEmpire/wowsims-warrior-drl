import array
import ctypes
import wowsims

class Spells():
    Shred = None

    @classmethod
    def register(cls):
        """Map from spell id to spellbook index and stores the result in a global with the spell's name."""
        num_spells = wowsims.getSpellCount()
        spells = array.array('I', [0] * num_spells)
        spells_ptr = (ctypes.c_int * len(spells)).from_buffer(spells)
        wowsims.getSpells(spells_ptr, len(spells))
        for i, spell in enumerate(spells):
            if spell == 48572 and cls.Shred is None: cls.Shred = i