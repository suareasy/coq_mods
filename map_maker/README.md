Map Maker
================================================================================

Python gui for generating custom maps for [Caves of Qud](http://www.cavesofqud.com/).


What does it do?
--------------------------------------------------------------------------------

map_maker allows users to easily create maps and export them to the desired _*.rpm_ 
format to be used in any mod.

Installation
--------------------------------------------------------------------------------

First, [hagadias](https://github.com/TrashMonks/hagadias) needs to be installed. 
map\_maker uses **hagadias** as a data source to display information about a 
selected item.

After that, no installation is required.


Tile support
--------------------------------------------------------------------------------

map_maker is capable of using in game tiles when add items to a map. Currently, 
the way this works by making sure map_maker can find the games _ObjectBlueprints.xml_ 
file. This can be done including the path to its parent directory (see the example 
below). Also, the [CavesofQudTileModdingToolkit.zip](https://www.dropbox.com/s/g8coebnzoqfema9/CavesofQudTileModdingToolkit.zip?dl=0) needs to be extracted into _map\_maker/_.

```
$ python3 run.py /path/to/game/
```
In the directory _path/to/game/_ should be the directory _CoQ\_Data/_

TODO
--------------------------------------------------------------------------------

* ~~Incorporate tile processing from [hagadias](https://github.com/TrashMonks/hagadias).~~ DONE
* Better listing for layered items.
* Add a 'redo' button.
* When holding left click, allow only one item per cell until you leave the cell.
* Finalize zooming and panning of main canvas.
* Add neat info feature when clicking on an object.
