import os
import pathlib
import os.path as path
import json

from typing import *

class Configuration:

    def __init__(self) -> None:
        self.work_dir = "."
        self.x1: int = 0
        self.y1: int = 0
        self.x2: int = 0
        self.y2: int = 0
        self.sleep: float = 0.1
        self.retina: bool = False
        self.mouse_x: int = 0
        self.mouse_y: int = 0
        self.resize_ratio: float = 1
        self.convert_to_bw = True
        self.jsonize = ["work_dir", "x1", "y1", "x2", "y2", "mouse_x", "mouse_y", "resize_ratio", "convert_to_bw", "retina", "sleep"]
        if self.work_dir != ".":
            os.makedirs(self.work_dir)

        home_dir = str(pathlib.Path.home()) or os.environ.get("HOME") or os.environ.get("HOMEPATH") or ""
        self.cfg_file = path.join(home_dir, ".screenshots.json")

    def path(self, filename: str) -> str:
        if not self.work_dir:
            return filename
        return self.work_dir + os.path.sep + filename

    def load(self) -> None:
        try:
            jsn = json.load(open(self.cfg_file, "r"))
        except Exception as e:
            print(f"error loading {self.cfg_file}, using default values: {e}")
            jsn = {}
        for key in jsn:
            #print(f"cfg {key} -> {jsn[key]}")
            setattr(self, key, jsn[key])
            #print(self)

    def to_json(self) -> Any:
        jsn = {}
        for key in self.jsonize:
            jsn[key] = getattr(self, key)
        return jsn

    def save(self) -> None:
        json.dump(self.to_json(), open(self.cfg_file, "w"))
        #print(f"saved {self.cfg_file}")
    
    def __str__(self) -> str:
        return f"cnf[{self.to_json()}]"

def menu(title: str, options: List[Tuple[str, Callable[[Configuration], str], Callable[[Configuration], None]]],
         cnf: Configuration, exit_key: str = "", exit_option: str = "") -> None:
    keys: Dict[str, bool] = {}
    for key, descr, func in options:
        if key in keys:
            raise Exception(f"Double key {key}")
        keys[key] = True
    while True:
        print("----------------------------------------------------------------------------------------------------")
        print(f"{title}:\n")
        for key, descr, func in options:
            print(f"{key} - {descr(cnf)}")
        if exit_key:
            print(f"{exit_key} - {exit_option if exit_option else 'Exit'}")
        answer = input("\n? ")
        if answer == exit_key:
            return
        for key, descr, func in options:
            if key == answer:
                func(cnf)
                cnf.save()
