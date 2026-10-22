import os
import shutil

from Database.Account import Account;
from Database.Inventory import Inventory;
from Database.Item import Item;
from Database.Character import Character;
from Database.Quest import Quest;
from Helper.Resources import ResourcesHelper;

# Clear Python Cache After Run
for DirPath, DirNames, FileNames in os.walk("."):
    if "__pycache__" in DirNames:
        shutil.rmtree(os.path.join(DirPath, "__pycache__"), ignore_errors=True)
        DirNames.remove("__pycache__")
    for f in FileNames:
        if f.endswith((".pyc", ".pyo")):
            os.remove(os.path.join(DirPath, f))
         