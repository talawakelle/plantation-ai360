# Tea disease image dataset

V1 strategy:

1. Prioritize licensed Sri Lankan tea disease imagery.
2. Add suitable external tea datasets only after harmonizing labels.
3. Keep ORIGINAL image identities and provenance.
4. Split originals into train/val/test before augmentation.
5. Never let augmented variants of the same original cross splits.
6. Keep a final external or Sri Lankan held-out test set untouched until evaluation.
7. Add `Unknown / manual review` behavior at application level using calibrated confidence/OOD checks rather than pretending the classifier learned every possible condition.

Expected classification folder shape:

```
train/Class_Name/*.jpg
val/Class_Name/*.jpg
test/Class_Name/*.jpg
```
