# Data connection inventory

The user has confirmed that the project can use all estates, divisions and field levels and that historical crop, field master, daily weather, fertilizer, labour, daily green leaf, factory, spraying, sustainability, LifeHRMS and MD Booklet data are available.

## First connection order

1. Estate/division/field master
2. Daily crop / green leaf
3. Daily estate weather
4. Labour / worker-day data
5. Fertilizer and spray history
6. Disease/pest historical records
7. Factory daily/process records
8. RA/sustainability indicators
9. LifeHRMS read-only connector
10. MD Booklet read-only connector

## Required keys

Every imported operational record must resolve to a stable estate/division/field identity where applicable. Do not use free-text estate names as the long-term relational key.
