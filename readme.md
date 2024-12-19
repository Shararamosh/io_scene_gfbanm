# Pokémon Switch Animation Blender Importer

This is Blender 2.80+ addon for importing single or multiple animation files from the Pokémon games in Nintendo Switch (Pokémon Sword/Shield, Let's GO Pikachu/Eevee, Legends Arceus and Scarlet/Violet).
## Dependencies:
- [Flatbuffers library](https://pypi.org/project/flatbuffers/) (the addon will attempt installing it using pip if not detected)
## Currently Working:
- Skeleton:
  - Translation transforms
  - Scaling transforms
  - Rotation transforms
## Not implemented:
- Material flags
- Event data

Flatbuffers schema scripts were generated from [pkZukan's gfbanm.fbs](https://github.com/pkZukan/PokeDocs/blob/main/SWSH/Flatbuffers/Animation/gfbanm.fbs).
