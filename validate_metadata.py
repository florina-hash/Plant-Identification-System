from plant_info import get_all_plant_names, get_plant_info


# Exact class names used by the ML dataset.
DATASET_CLASSES = [
    "Curry",
    "Drumstick",
    "Tomato",
    "Ginger",
    "Chilly",
    "Nelavembu",
    "Jackfruit",
    "Turmeric",
    "Honge",
    "Mint",
    "Jasmine",
    "Castor",
    "Kambajala",
    "Kasambruga",
    "Badipala",
    "Neem",
    "Guava",
    "Coriender",
    "ashoka",
    "Caricature",
    "Citron lime (herelikai)",
    "Catharanthus",
    "Astma_weed",
    "Balloon_Vine",
    "Hibiscus",
    "Bhrami",
    "Aloevera",
    "Chakte",
    "Eucalyptus",
    "Beans",
    "Insulin",
    "Marigold",
    "Bamboo",
    "Amla",
    "Arali",
    "Globe Amarnath",
    "Lemon",
    "Common rue(naagdalli)",
    "Ekka",
    "Betel",
    "Henna",
    "Gasagase",
    "Doddpathre",
    "Malabar_Spinach",
    "Rose",
    "Amruthaballi",
    "Mango",
    "Seethaashoka"
]


REQUIRED_FIELDS = [
    "scientific_name",
    "common_names",
    "family",
    "description",
    "uses"
]


metadata_classes = get_all_plant_names()

missing_classes = sorted(
    set(DATASET_CLASSES) - set(metadata_classes)
)

extra_classes = sorted(
    set(metadata_classes) - set(DATASET_CLASSES)
)


invalid_entries = []

for plant_name in DATASET_CLASSES:
    plant_info = get_plant_info(plant_name)

    if plant_info is None:
        continue

    missing_fields = [
        field
        for field in REQUIRED_FIELDS
        if field not in plant_info
    ]

    if missing_fields:
        invalid_entries.append({
            "plant": plant_name,
            "missing_fields": missing_fields
        })


print("===================================")
print("PLANT METADATA VALIDATION")
print("===================================")

print(f"Dataset classes : {len(DATASET_CLASSES)}")
print(f"Metadata classes: {len(metadata_classes)}")

print("\nMissing classes:")
print(missing_classes)

print("\nExtra classes:")
print(extra_classes)

print("\nEntries with missing fields:")
print(invalid_entries)


if not missing_classes and not extra_classes and not invalid_entries:
    print("\nSUCCESS: Metadata validation passed!")
else:
    print("\nERROR: Metadata validation failed.")