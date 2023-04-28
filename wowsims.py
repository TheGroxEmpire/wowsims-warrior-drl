import ctypes
import platform

lib_file_path = 'wowsimwotlk-'
if platform.system() == 'Linux':
    lib_file_path = lib_file_path + 'linux.so' 
elif platform.system() == 'Darwin':
    lib_file_path = lib_file_path + 'mac.so' 
else:
    lib_file_path = lib_file_path + 'windows.dll' 

library = ctypes.cdll.LoadLibrary(lib_file_path)

# new
new = library.new
new.argtypes = [ctypes.c_char_p]

# trySpell
trySpell = library.trySpell
trySpell.argtypes = [ctypes.c_int]
trySpell.restype = ctypes.c_bool

# doNothing
doNothing = library.doNothing
doNothing.argtypes = [ctypes.c_int]

# step
step = library.step
step.restype = ctypes.c_bool

# needsInput
needsInput = library.needsInput
needsInput.restype = ctypes.c_bool

# registerAuras
registerAuras = library.registerAuras
registerAuras.argtypes = [ctypes.POINTER(ctypes.c_char_p)]

# registerTargetAuras
registerTargetAuras = library.registerTargetAuras
registerTargetAuras.argtypes = [ctypes.POINTER(ctypes.c_char_p)]

# getAuras
getAuras = library.getAuras
getAuras.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_int]

# getTargetAuras
getTargetAuras = library.getTargetAuras
getTargetAuras.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_int]

# getUnits
getUnitCount = library.getUnitCount
getUnitCount.restype = ctypes.c_int

# getRemainingDuration
getRemainingDuration = library.getRemainingDuration
getRemainingDuration.restype = ctypes.c_double

# getEnergy
getEnergy = library.getEnergy
getEnergy.restype = ctypes.c_double

# getComboPoints
getComboPoints = library.getComboPoints
getComboPoints.restype = ctypes.c_int

# getDamageDone
getDamageDone = library.getDamageDone
getDamageDone.restype = ctypes.c_double

# cleanup
cleanup = library.cleanup

# getSpells
getSpells = library.getSpells
getSpells.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int]

# getSpellCount
getSpellCount = library.getSpellCount
getSpellCount.restype = ctypes.c_int