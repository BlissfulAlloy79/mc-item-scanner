# mc-item-scanner

scans all the items in your minecraft save

it will generate a `results.csv` to store the scanning results

the scanning process only involves items in the tile entities in the world and player inventories, including ender chest

those item entity which is not stored in a container or player inventory will not be counted

# Prerequisites

```
pip install nbtlib
```

### Install specified version off anvil-parser for higher version support

```
pip install git+https://github.com/0xTiger/anvil-parser.git
```



# How to use

### Example usage

```
python mc-item-scanner.py -w <world directory> -o <output file direcotry>
```

use `-w` or `--worlddirectory` to specify the world save you want to scan

use `-o` or `--outdirectory` to specify which directory the `results.csv` file will be generated