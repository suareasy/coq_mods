Map Maker
================================================================================

Python gui for generating custom maps for [Cave of Qud](http://www.cavesofqud.com/).


What does it do?
--------------------------------------------------------------------------------

map_maker allows users to easily create maps and export them to the desired _*.rpm_ 
format to be used in any mod.

Installation
--------------------------------------------------------------------------------

NA

Tile support
--------------------------------------------------------------------------------

map_maker is capable of using in game tiles when add items to a map. Currently, 
the way this works by making sure map_maker can find the games _ObjectBlueprints.xml_ 
file and the [CavesofQudTileModdingToolkit.zip](https://www.dropbox.com/s/g8coebnzoqfema9/CavesofQudTileModdingToolkit.zip?dl=0).

```
$ python3 map_maker.py /home/dsuarez/Downloads/Linux/CoQ_Data/StreamingAssets/Base/ObjectBlueprints.xml ~/Downloads/Textures
```

TODO
--------------------------------------------------------------------------------

* Incorporate tile processing from [hagadias](https://github.com/TrashMonks/hagadias).
* Better listing for layered items.
* Add a 'redo' button.
* When holding left click, allow only one item per cell until you leave the cell.
* Finalize zooming and panning of main canvas.
* Add neat info feature when clicking on an object.
