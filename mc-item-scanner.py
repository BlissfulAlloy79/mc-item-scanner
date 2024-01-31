import nbtlib
import anvil
from anvil.errors import ChunkNotFound
import os
import argparse
import csv


aparser = argparse.ArgumentParser(description=r"path of \world")
aparser.add_argument('-o', '--outdirectory', default=r'.\\')
aparser.add_argument('-w', '--worlddirectory', default=r'.\\')

args = aparser.parse_args()
PATH_OUTDIR = args.outdirectory
PATH_WORLD = args.worlddirectory

item_record: dict = {}


def count_item(item_id, item_count: int):
    item_id: str = str(item_id)
    if item_id not in item_record:
        item_record[item_id] = 0
    item_record[item_id] += item_count


def region_search(region_file):
    def search_shulker_box_item(shulker_box):
        if "Items" not in shulker_box["tag"]["BlockEntityTag"]:
            return
        for item in shulker_box["tag"]["BlockEntityTag"]["Items"]:
            count_item(item["id"], int(str(item["Count"])))
            # print(item["id"], " ", item["Count"])

    target_region = anvil.Region.from_file(region_file)

    try:
        for i in range(0, 32):
            for j in range(0, 32):
                try:
                    chunk = anvil.Chunk.from_region(target_region, i, j)
                    if chunk.tile_entities:
                        te = chunk.tile_entities
                        for k in te:
                            if "Items" not in k:
                                continue
                            for a in k["Items"]:
                                count_item(a["id"], int(str(a["Count"])))
                                # print(a["id"], " ", a["Count"])
                                if str(a["id"]).endswith("shulker_box") and "tag" in a:
                                    search_shulker_box_item(a)
                except ChunkNotFound:
                    pass
    except IndexError as e:
        print(f"{e}, when searching region {region_file}")


def player_inventory_search(data_file):
    def search_shulker_box_item(shulker_box):
        try:
            if "Items" not in shulker_box["tag"]["BlockEntityTag"]:
                return
            for item in shulker_box["tag"]["BlockEntityTag"]["Items"]:
                count_item(item["id"], int(item["Count"]))
            # print(item["id"], " ", item["Count"])
        except KeyError as e:
            print(f"KeyError: {e}")
            print(data_file)
            print(shulker_box)

    target_file = nbtlib.load(data_file)

    for i in target_file["Inventory"]:
        count_item(i["id"], int(i["Count"]))
        # print(i["id"], " ", int(i["Count"]))
        if str(i["id"]).endswith("shulker_box") and "tag" in i:
            search_shulker_box_item(i)

    for i in target_file["EnderItems"]:
        count_item(i["id"], int(i["Count"]))
        # print(i["id"], " ", int(i["Count"]))
        if str(i["id"]).endswith("shulker_box") and "tag" in i:
            search_shulker_box_item(i)


def main():
    if not os.path.isdir(PATH_OUTDIR):
        raise NotADirectoryError("the outdirectory specified is not a directory")

    if "level.dat" not in os.listdir(PATH_WORLD):
        raise FileNotFoundError("file: level.dat cannot be found in the world directory!")

    try:
        print(r"searching \playerdata")
        for f in os.listdir(fr"{PATH_WORLD}\playerdata"):
            if f.endswith(".dat"):
                player_inventory_search(fr"{PATH_WORLD}\playerdata\{f}")
    except FileNotFoundError:
        print(r"directory: \playerdata cannot be found in the world directory")

    try:
        print(r"searching \region")
        for f in os.listdir(fr"{PATH_WORLD}\region"):
            if f.endswith(".mca"):
                region_search(fr"{PATH_WORLD}\region\{f}")
    except FileNotFoundError:
        print(r"directory: \region cannot be found in the world directory")

    try:
        print(r"searching \DIM1\region")
        for f in os.listdir(fr"{PATH_WORLD}\DIM1\region"):
            if f.endswith(".mca"):
                region_search(fr"{PATH_WORLD}\DIM1\region\{f}")
    except FileNotFoundError:
        print(r"directory: \DIM1\region cannot be found in the world directory")

    try:
        print(r"searching \DIM-1\region")
        for f in os.listdir(fr"{PATH_WORLD}\DIM-1\region"):
            if f.endswith(".mca"):
                region_search(fr"{PATH_WORLD}\DIM-1\region\{f}")
    except FileNotFoundError:
        print(r"directory: \DIM-1\region cannot be found in the world directory")

    # print(item_record)

    with open(fr'{PATH_OUTDIR}\results.csv', 'w', encoding='utf8', newline='') as out:
        writer = csv.writer(out)
        writer.writerow(["item", "count"])
        for i in item_record.items():
            writer.writerow(list(i))


if __name__ == '__main__':
    main()
