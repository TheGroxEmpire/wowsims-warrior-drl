import array
import ctypes
import wowsims

class Spells():
    Bloodthirst = None
    Whirlwind = None
    Slam = None
    HeroicStrike = None
    Execute = None
    Rend = None
    Overpower = None
    BattleStance = None 
    BerserkerStance = None 
    DeathWish = None 
    Recklessness = None 
    ShatteringThrow = None 
    # Other CD is here so that the agent could control it
    EngiGlove = None 
    Bloodlust = None


    @classmethod
    def register(cls):
        """Map from spell id to spellbook index and stores the result in a global with the spell's name."""
        num_spells = wowsims.getSpellCount()
        spells = array.array('I', [0] * num_spells)
        spells_ptr = (ctypes.c_int * len(spells)).from_buffer(spells)
        wowsims.getSpells(spells_ptr, len(spells))
        for i, spell in enumerate(spells):
            if spell == 23881 and cls.Bloodthirst is None: cls.Bloodthirst = i
            if spell == 1680 and cls.Whirlwind is None: cls.Whirlwind = i
            if spell == 47475 and cls.Slam is None: cls.Slam = i
            if spell == 47450 and cls.HeroicStrike is None: cls.HeroicStrike = i
            if spell == 47471 and cls.Execute is None: cls.Execute = i
            if spell == 47465 and cls.Rend is None: cls.Rend = i
            if spell == 7384 and cls.Overpower is None: cls.Overpower = i
            if spell == 2457 and cls.BattleStance is None: cls.BattleStance = i
            if spell == 2458 and cls.BerserkerStance is None: cls.BerserkerStance = i
            if spell == 12292 and cls.DeathWish is None: cls.DeathWish = i
            if spell == 1719 and cls.Recklessness is None: cls.Recklessness = i
            if spell == 64382 and cls.ShatteringThrow is None: cls.ShatteringThrow = i
            if spell == 54758 and cls.EngiGlove is None: cls.EngiGlove = i
            if spell == 2825 and cls.Bloodlust is None: cls.Bloodlust = i

class Auras():
    Labels = ["Berserker Stance", "Battle Stance", "Bloodsurge Proc", "Recklessness", "Death Wish", "Overpower Aura"]
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
    Labels = ["Rend"]
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