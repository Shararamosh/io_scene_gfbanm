# Pokémon Switch Animation Blender Importer/Exporter

This is Blender 2.80+ addon for importing single or multiple animation files from the Pokémon games in Nintendo Switch (Pokémon Sword/Shield, Let's GO Pikachu/Eevee, Legends Arceus and Scarlet/Violet).
## Dependencies:
- [Flatbuffers library](https://pypi.org/project/flatbuffers/) (the addon will attempt installing it using pip if not detected)
## Implemented:
- Skeleton:
  - Translation transforms
  - Scaling transforms (requires correct "Inherit Scale" option to be set on bones prior to importing animation)
  - Rotation transforms
## Not implemented:
- Material flags
- Event data
## Partially implemented:
- Animation export:
  - Invalid rotation transforms (due to incorrect rotation quantization)
  - Invalid translation transforms for non-root bones (due to being affected by parent bones' invalid rotation transforms)
  - Valid scale transforms ("Inherit Scale" option is not taken into account as it's part of armature, not animation)

Flatbuffers schema scripts were generated from [pkZukan's gfbanm.fbs](https://github.com/pkZukan/PokeDocs/blob/main/SWSH/Flatbuffers/Animation/gfbanm.fbs).

If you need addon for importing and/or exporting both animations and meshes, download [this one](https://github.com/ChicoEevee/Pokemon-Switch-V2-Model-Importer-Blender). It fully includes this addon, but may occasionally be out-of-date.