import json
import os
from copy import deepcopy
from PIL import Image


class Ape:
    RENDER_ORDER = ["background", "body", "outfit",
                    "jewelry", "head", "eye",
                    "mouth attributes", "glasses", "headwear"]

    def __init__(self, traits: dict):
        self._id = None
        self._traits = traits
        self.__traits_path = {}

        # Resolve traits path
        for _type, name in self.traits.items():
            path = f'assets/{_type}/{name}.png'

            if _type == "mouth attributes" and self._traits[_type] != "Respirator":
                path = f'assets/{_type}/{self._traits["head"]}/{self._traits[_type]}.png'

            if _type == 'jewelry' and self._traits[_type] == "Septum Piercing":
                path = f'assets/{_type}/{self._traits["head"]}/{self._traits[_type]}.png'

            if _type == 'jewelry' and self.traits[_type] == "Golden Earring" and self.traits["body"] == "Jeff":
                path = f'assets/{_type}/{self._traits["body"]}/{self._traits[_type]}.png'

            if _type == 'jewelry' and self._traits[_type] == "Golden Eyebrow Piercing":
                path = f'assets/{_type}/{self._traits["eye"]}/{self._traits[_type]}.png'

            if _type == 'jewelry' \
                    and self._traits[_type] == "Golden Eyebrow Piercing" \
                    and self.traits["body"] == "Turned":
                path = f'assets/{_type}/{self.traits["body"]}/{self._traits[_type]}.png'

            if _type == "headwear" \
                    and self.traits["body"] == "Robin" \
                    and self.traits["headwear"] in ["Gold Crown", "Reverse Hat", "Captains Hat"]:
                path = f'assets/{_type}/{self._traits["head"]}/{self._traits[_type]}.png'

            if _type == "headwear" \
                    and self.traits["head"] == "Juanita" \
                    and self.traits["headwear"] in ["Gold Crown", "Reverse Hat"]:
                path = f'assets/{_type}/{self._traits["head"]}/{self._traits[_type]}.png'

            self.__traits_path[_type] = path

    def __eq__(self, other):
        return self._traits == other.traits

    @property
    def id(self):
        return self._id

    @property
    def traits(self):
        return self._traits

    @id.setter
    def id(self, id_num):
        self._id = id_num

    def _has_face_jewelry(self) -> bool:
        face_jewelry = ["Cross Earring", "Double Ear Piercing",
                        "Golden Earring", "Golden Nose Ring", "Septum Piercing"]
        return self.traits["jewelry"] in face_jewelry

    def render(self):
        ape = None

        render_order = deepcopy(self.RENDER_ORDER)
        if self._has_face_jewelry() and type(self) is not GasmaskApe and type(self) is not AstronautApe:
            jewelry_index = render_order.index("jewelry")
            head_index = render_order.index("head")
            render_order[jewelry_index], render_order[head_index] = render_order[head_index], render_order[
                jewelry_index]
        elif self._traits["jewelry"] == "Golden Eyebrow Piercing":
            jewelry_index = render_order.index("jewelry")
            eye_index = render_order.index("eye")
            render_order.insert(eye_index, render_order.pop(jewelry_index))

        for trait in render_order:
            try:
                trait_img = Image.open(self.__traits_path[trait]).convert('RGBA')
                ape = trait_img if (ape is None) else Image.alpha_composite(ape, trait_img)
            except KeyError as e:
                print(e)
                continue
            except Exception as e:
                print(e)
                print(self._traits)

        tag_img = Image.open("assets/tag/Tag white.png").convert('RGBA')
        ape = Image.alpha_composite(ape, tag_img)

        return ape.convert('RGB')

    def _create_json_metadata_file(self):
        if not os.path.exists("generated/metadata"):
            os.mkdir('generated/metadata')

        data = {
            "id": self.id,
            "assets": {
                "ape": self.traits["head"] if self.traits["outfit"] != "Banana Game Suit" else "Unknown",
                "background": self.traits["background"],
                "eyes": self.traits["eye"],
                "glasses": self.traits["glasses"],
                "jewelry": self.traits["jewelry"],
                "headwear": "None" if self.traits["headwear"] == "Orange Hoodie overlay" else self.traits["headwear"],
                "mouth": "Nothing" if self.traits["mouth attributes"] == "None" else self.traits["mouth attributes"],
                "outfit": self.traits["outfit"]
            }
        }
        with open(f"./generated/metadata/artsyape-{str(self.id)}.json", "w") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)


class GoldenApe(Ape):
    RENDER_ORDER = ["background", "body", "outfit",
                    "jewelry", "head", "mouth attributes",
                    "glasses", "headwear"]

    def __init__(self, traits: dict):
        traits["eye"] = "Golden Gaze"
        super().__init__(traits)


class ZombieApe(Ape):
    RENDER_ORDER = ["background", "body", "outfit",
                    "jewelry", "head", "eye", "glasses", "mouth attributes",
                    "headwear"]

    def __init__(self, traits: dict):
        traits["eye"] = "Loose"
        super().__init__(traits)
        if "Gasmask" in traits["glasses"]:
            traits["glasses"] = "None"


class AstronautApe(Ape):
    RENDER_ORDER = ["background", "body", "head",
                    "eye", "glasses", "outfit"]

    def __init__(self, traits: dict):
        traits["body"] = "Astronaut 2"
        if "Turned" in traits["head"]:
            traits["eye"] = "None"
        if "Golden" in traits["head"]:
            traits["eye"] = "None"
        if "Gasmask" in traits["glasses"]:
            traits["glasses"] = "None"
        super().__init__(traits)


class LuartApe(Ape):
    RENDER_ORDER = ["background", "luart-background", "body", "outfit", "jewelry",
                    "head", "eye", "glasses", "headwear"]

    def __init__(self, traits: dict):
        traits["luart-background"] = "Luart Helmet Backround"
        traits["mouth attributes"] = "None"
        if "Turned" in traits["head"]:
            traits["eye"] = "Loose"
        if "Hoodie" in traits["outfit"]:
            traits["outfit"] = "None"
        if "Gasmask" in traits["glasses"]:
            traits["glasses"] = "None"
        super().__init__(traits)


class SquidgameApe(Ape):
    RENDER_ORDER = ["background", "outfit"]


class GasmaskApe(Ape):
    RENDER_ORDER = ["background", "body", "outfit", "head", "glasses", "headwear"]


class HoodieApe(Ape):
    def __init__(self, traits: dict):
        traits["body"] = "Orange Hoodie underlay"
        traits["headwear"] = "Orange Hoodie overlay"
        if "Turned" in traits["head"]:
            traits["eye"] = "Loose"
        if "Gasmask" in traits["glasses"]:
            traits["mouth attributes"] = "None"
        super().__init__(traits)
