"""
Default thought and speech messages embedded directly in bytecode inside the executable.
Provides charming, heartwarming messages for each species (hamster, duck, and future animals).
"""

HAMSTER_MESSAGES = [
    "Ti voglio un mondo di bene! ❤️",
    "Hai bevuto un goccino d'acqua oggi? Ricordati di idratarti! 💧",
    "Sgranocchio un semino e ti guardo con affetto... 🌻",
    "Sei la persona più speciale e dolce del mondo ✨",
    "Oggi stai facendo del tuo meglio e sei bravissima! 💪",
    "Facciamo una piccola pausa insieme? Ti tengo compagnia! 🐾",
    "Un abbraccio morbidissimo e soffice per te! 🐹",
    "Zzz... stavo sognando un prato pieno di semini dorati... 💤",
    "Sono sempre qui vicino a te, proprio sullo schermo! ❤️",
    "Fai un bel respiro profondo e rilassa le spalle 🌸",
    "Guarda come sono tondo e morbido oggi! 🥰",
    "Crunch crunch crunch... che bontà questo spuntino! 🌻",
    "Mi fai un grattino delicato sulla testolina? ✨",
    "Qualunque cosa accada oggi, sappi che sei amata tantissimo ❤️",
    "Ti mando un bacio con il mio nasino rosa! 🐽",
    "Stai lavorando tanto, non dimenticare di sorridere! 😊"
]

DUCK_MESSAGES = [
    "Quack! Ti voglio un mondo di bene! 🦆❤️",
    "Hai bevuto un goccio d'acqua fresca oggi? Idratarsi è importante! 💧",
    "Nuoto serena e ti guardo con tanto affetto... 🌊✨",
    "Sgranocchio un pisellino verde dolce... che delizia! 🥬🥰",
    "Sei la persona più speciale e dolce del mondo! 🌸",
    "Oggi stai facendo un ottimo lavoro, continua così! 💪",
    "Facciamo una piccola pausa insieme? Ti tengo compagnia! 🐾",
    "Un abbraccio piumoso e morbidissimo per te! 🦆✨",
    "Zzz... stavo sognando uno stagno calmo pieno di ninfee fiorite... 💤",
    "Waddle waddle... guarda come dondolo felice per te! 💛",
    "Fai un bel respiro profondo e rilassa le spalle 🌸",
    "Mi fai una carezzina dolce sulle piumette del capo? ✨",
    "Qualunque cosa accada oggi, sappi che sei amata tantissimo! ❤️",
    "Ti mando un bacetto affettuoso con il mio becco arancione! 💋",
    "Quack quack! Ricordati di fare un bel sorriso oggi! 😊",
    "Sbattito d'ali per festeggiare quanto sei brava! 🪶✨",
    "Guarda che bel pisellino saporito ho trovato per merenda! 🥗",
    "Sei la mia persona preferita in tutto lo stagno! 🦆💖",
    "Che bella giornata per passeggiare sulla barra delle applicazioni! 🐾",
    "Un pisolino a ciambella sulle piume è proprio quello che ci voleva! 💤"
]

# Backwards compatible default list
MESSAGES = HAMSTER_MESSAGES

MESSAGES_BY_SPECIES = {
    "criceto": HAMSTER_MESSAGES,
    "paperella": DUCK_MESSAGES
}

def get_messages_for_species(species_id: str) -> list[str]:
    """Returns the list of messages for a given species ID, falling back to hamster messages."""
    return MESSAGES_BY_SPECIES.get(species_id, HAMSTER_MESSAGES)
