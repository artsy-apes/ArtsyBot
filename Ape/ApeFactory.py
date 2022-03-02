from Ape.Ape import Ape, ZombieApe, AstronautApe, LuartApe, SquidgameApe, GasmaskApe, HoodieApe, GoldenApe


def ApeFactory(traits):
    apes = {
        "Ape": Ape,
        "Golden": GoldenApe,
        "Zombie": ZombieApe,
        "Astronaut": AstronautApe,
        "Luart": LuartApe,
        "Squidgame": SquidgameApe,
        "Gasmask": GasmaskApe,
        "Hoodie": HoodieApe,
    }

    ape_type = "Ape"
    if "Golden" in traits["body"]:
        ape_type = "Golden"
    if "Turned" in traits["body"]:
        ape_type = "Zombie"
    if "Gasmask" in traits["glasses"]:
        ape_type = "Gasmask"
    if "Banana Game Suit" in traits["outfit"]:
        ape_type = "Squidgame"
    if "Astronaut" in traits["outfit"]:
        ape_type = "Astronaut"
    if "Luart" in traits["headwear"]:
        ape_type = "Luart"
    if "Orange Hoodie" in traits["outfit"]:
        ape_type = "Hoodie"

    return apes[ape_type](traits)

