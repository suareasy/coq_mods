Map Maker
================================================================================

Python gui for generating custom maps for [Caves of Qud](http://www.cavesofqud.com/).


What does it do?
--------------------------------------------------------------------------------

map_maker allows users to easily create maps and export them to the desired _*.rpm_ 
format to be used in any mod.

Installation and Requirements
--------------------------------------------------------------------------------
Needs 
 * [hagadias](https://github.com/TrashMonks/hagadias)
 * python3

map\_maker uses **hagadias** as a data source to display information about a 
selected item.

Tile support
--------------------------------------------------------------------------------

map_maker is capable of using in game tiles when add items to a map. Currently, 
the way this works by making sure map_maker can find the games _ObjectBlueprints.xml_ 
file. This can be done including the path to its parent directory (see the example 
below). Also, the [CavesofQudTileModdingToolkit.zip](https://www.dropbox.com/s/g8coebnzoqfema9/CavesofQudTileModdingToolkit.zip?dl=0) needs to be extracted into _map\_maker/_.

```shell
$ git clone git@github.com:billbrasky/coq_mods.git
$ cd coq_mods/map_maker
```

Down load and extract [CavesofQudTileModdingToolkit.zip](https://www.dropbox.com/s/g8coebnzoqfema9/CavesofQudTileModdingToolkit.zip?dl=0)

```shell
$ python3 run.py /path/to/game/
```
In the directory _path/to/game/_ should be the directory _CoQ\_Data/_. So for 
me using the version from HumbleBundle on Linux the game path is, _~/Downloads/Linux/_.

TODO
--------------------------------------------------------------------------------

* ~~Incorporate tile processing from [hagadias](https://github.com/TrashMonks/hagadias).~~ DONE
* Better listing for layered items.
* Add a 'redo' button.
* When holding left click, allow only one item per cell until you leave the cell.
* Finalize zooming and panning of main canvas.
* Add neat info feature when clicking on an object.
