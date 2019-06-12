WIP

Purpose: Create an easier process for creating custom maps for the game 
Caves of Qud.

A drawing in GIMP can be exported as an html file and processed to satisfy the 
games' requirements.

Use **mappings.csv** to specificy the _mapping_ of color code to in game 
texture name.

At the bottom of **mapper.py** specify html export file from GIMP, the mapping 
csv file to use, and the output location.

The expected input is an html file export from GIMP.

The output is an rpm file.
