from plant_info import get_plant_info, get_all_plant_names


print("All plants:")
print(get_all_plant_names())

print("\nNeem information:")
print(get_plant_info("Neem"))

print("\nUnknown plant:")
print(get_plant_info("Banana"))