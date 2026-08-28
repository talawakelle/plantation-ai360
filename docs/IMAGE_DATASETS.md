# Image dataset acquisition and provenance

## Primary V1 source — Sri Lankan Tea Leaf Dataset

- Repository: Mendeley Data
- Dataset ID: `sjmy6k24d6`
- Version pinned for V1: **4**
- DOI: `10.17632/sjmy6k24d6.4`
- Published: 21 July 2026
- Licence shown by repository: CC BY 4.0
- Region: images collected from Sri Lankan tea estates
- Raw images reported: 1,791
- Offline-augmented images reported: 5,968
- Classes described: algal leaf spot, black blight, blister blight, gray blight, spider mites, healthy
- Dataset page: `https://data.mendeley.com/datasets/sjmy6k24d6/4`

### Rule

Download the dataset, but use **raw originals** as the V1 source. Do not mix the repository's offline-augmented variants across training, validation and test sets.

Run:

```powershell
python scripts\prepare_tea_disease_dataset.py `
  --source "C:\path\to\extracted\RAW_FOLDER" `
  --output "data\vision\tea_disease"
```

This records every copied image and SHA-256 hash in `manifest.csv`.

## Supplementary datasets

Only add a supplementary source when it fills a defined class/data gap. For every source record:

- dataset title and version/DOI
- licence
- original class label
- canonical PlantationAI label
- source file identity/hash
- split assignment

Do not silently merge `gray blight`, `black blight`, `brown blight`, pest damage, or other visually similar labels. Label harmonisation requires explicit mapping and, where necessary, tea-pathology review.

## Local validation requirement

A model trained entirely on public datasets is a prototype. The Active Learning module is intended to build a future verified TTE image set from mobile uploads. Public-data test accuracy must never be presented as proven estate-level diagnostic accuracy.
