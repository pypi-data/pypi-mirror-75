import warnings
from typing import Tuple

import lol_id_tools as lit
import requests
import lol_dto
import lol_id_tools


class RuneTreeHandler:
    """A simple class that caches data from ddragon and gets rune tree per rune ID.
    """

    def __init__(self):
        self.cache = {}
        self.versions = None
        self.reload_versions()

    def reload_versions(self):
        self.versions = requests.get("https://ddragon.leagueoflegends.com/api/versions.json").json()

    def get_runes_data(self, patch):
        full_patch = self.get_version(patch)

        if full_patch not in self.cache:
            self.cache[full_patch] = requests.get(
                f"https://ddragon.leagueoflegends.com/cdn/{full_patch}/data/en_US/runesReforged.json"
            ).json()

        return self.cache[full_patch]

    def get_version(self, patch):
        """Returns the game version as defined by ddragon

        Params:
            patch: MM.mm format patch
        """
        for version in self.versions:
            if ".".join(version.split(".")[:2]) == patch:
                return version

        # If we have a patch that we do not know, we reload versions stupidly.
        warnings.warn("Reloading game versions")
        self.reload_versions()
        return self.get_version(patch)

    def get_primary_tree(self, runes, patch) -> Tuple[int, str]:
        return self.get_tree(runes[0], patch)

    def get_secondary_tree(self, runes, patch) -> Tuple[int, str]:
        return self.get_tree(runes[4], patch)

    def get_tree(self, _rune: lol_dto.classes.game.LolGamePlayerRune, patch) -> Tuple[int, str]:
        data = self.get_runes_data(patch)

        for tree in data:
            for slot in tree["slots"]:
                for rune in slot["runes"]:
                    if rune["id"] == _rune["id"]:
                        return tree["id"], lol_id_tools.get_name(tree["id"], object_type="rune")


rune_tree_handler = RuneTreeHandler()


def add_qq_runes(player: lol_dto.classes.game.LolGamePlayer, runes_list, patch=None, add_names=True):
    player["runes"] = []
    slot = 0
    for rune_index, rune in enumerate(runes_list):

        # We iterate on the rune’s "rank", which can be more than 1 for stats perks
        for i in range(rune["runes_num_"]):
            rune_dto = lol_dto.classes.game.LolGamePlayerRune(id=rune["runes_id_"], slot=slot)

            if add_names:
                rune_dto["name"] = lit.get_name(rune_dto["id"], object_type="rune")

            player["runes"].append(rune_dto)
            slot += 1

    # We need patch information to properly load rune tree names
    if patch:
        player["primaryRuneTreeId"], player["primaryRuneTreeName"] = rune_tree_handler.get_primary_tree(
            player["runes"], patch
        )
        (player["secondaryRuneTreeId"], player["secondaryRuneTreeName"],) = rune_tree_handler.get_secondary_tree(
            player["runes"], patch
        )

    return player
