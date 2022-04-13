import copy
import os
import json as jsonlib
from abc import ABC, abstractmethod
import pandas as pd
from ..utils import workspace


class Export(ABC):
    def __init__(self, output: str, profile: str = "default"):
        """

        Args:
            output (str): Output File Path
        """
        self.profile = profile
        self.file_ext_check(output)
        self.output = output
        self.data = None

    def list_exist_dirs(self):
        perk_dir_list = []
        for root, dirs, files in os.walk(os.path.join(workspace(), "data", "wish_list", self.profile)):
            if "icons" in dirs and "data.json" in files:
                perk_dir_list.append(root)
        return perk_dir_list

    def get_perk_icon(self, perk_id: str) -> str:
        perk_icon_dir = os.path.join(workspace(), "data", "perks", "icons")
        perk_icon_file = os.path.join(perk_icon_dir, f"{perk_id}.jpg")
        if os.path.isfile(perk_icon_file) is False:
           perk_icon_file = None
        return perk_icon_file

    def get_perk_icon_link(self, perk_id: str) -> str:
        perk_dir = os.path.join(workspace(), "data", "perks")
        perk_json = os.path.join(perk_dir, f"{perk_id}.json")
        with open(perk_json, "r") as fp:
            perk_json = jsonlib.load(fp)
        return perk_json['icons']['icon']

    @abstractmethod
    def file_ext_check(self, output: str):
        pass

    @abstractmethod
    def process(self):
        pass

    @abstractmethod
    def save(self):
        pass


class HTMLExport(Export):
    def file_ext_check(self, output: str):
        _ext = os.path.splitext(output)[-1]
        if _ext not in [".html"]:
            raise TypeError(f"Output File Ext Invalid, {_ext}\n"
                            f"Expect Ext is one of [html]")

    def process(self):
        wish_list = []
        for element in self.list_exist_dirs():
            data_file = os.path.join(element, "data.json")
            with open(data_file, "r") as fp:
                json_data = jsonlib.load(fp)
            item = [
                json_data['name'],
                json_data['icons']['water_mark'],
                json_data['icons']['icon'],
                json_data['category'],
                json_data['weapon_type'],
                json_data['damage_type'],
            ]
            for perk_data in json_data['perks']:
                _item = copy.deepcopy(item)
                for perk in perk_data['perks']:
                    _item.append(self.get_perk_icon_link(perk['hash']))
                wish_list.append(_item)
        self.data = pd.DataFrame(wish_list,
                                 columns=[
                                     "name",
                                     "season",
                                     "icon",
                                     "category",
                                     "type",
                                     "damage type",
                                     "wish perk #1",
                                     "wish perk #2",
                                     "wish perk #3",
                                     "wish perk #4"
                                 ])

    def path_to_image_html(self, path):
        if path == "None":
            return None
        else:
            return '<img src="' + path + '" width="60" >'

    def _gen_html(self):
        html_string = """
        <html>
            <head><title>HTML Pandas Dataframe with CSS</title></head>
            <link rel="stylesheet" type="text/css" href="style.css"/>
            <body>
                {table}
            </body>
        </html>.
        """
        html_data = self.data.to_html(escape=False,
                                      formatters={
                                          "icon": self.path_to_image_html,
                                          "season": self.path_to_image_html,
                                          "wish perk #1": self.path_to_image_html,
                                          "wish perk #2": self.path_to_image_html,
                                          "wish perk #3": self.path_to_image_html,
                                          "wish perk #4": self.path_to_image_html,
                                          "wish perk #5": self.path_to_image_html,
                                      },
                                      classes="mystyle"
                                      )
        return html_string.format(table=html_data)

    def save(self):
        with open(self.output, "w", encoding="utf-8") as fp:
            fp.write(self._gen_html())


