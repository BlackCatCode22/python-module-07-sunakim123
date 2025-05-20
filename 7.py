import datetime
import re


def gen_birth_date(age, season):
    today = datetime.date.today()
    birth_year = today.year - age

    # Estimate mid-season birthdays
    season_to_date = {
        "spring": datetime.date(birth_year, 3, 21),
        "summer": datetime.date(birth_year, 6, 21),
        "fall": datetime.date(birth_year, 9, 21),
        "winter": datetime.date(birth_year, 12, 21),
        "unknown": datetime.date(birth_year, 7, 1),  # estimate
    }
    return season_to_date.get(season.lower(), season_to_date["unknown"])

def gen_unique_id(species, counter):
    prefix = species[:2].capitalize()
    return f"{prefix}{counter:02d}"


def load_animal_names(filename):
    species_names = {}
    with open(filename, 'r') as file:
        current_species = None
        for line in file:
            line = line.strip()
            if line.endswith("Names:"):
                current_species = line.split()[0].lower()
                species_names[current_species] = []
            elif line:
                names = [name.strip() for name in line.split(',') if name.strip()]
                species_names[current_species].extend(names)
    return species_names


def main():
    names_dict = load_animal_names("animalNames.txt")
    species_counters = {species: 1 for species in names_dict}
    name_indices = {species: 0 for species in names_dict}
    habitats = {}

    with open("arrivingAnimals.txt", 'r') as file:
        lines = file.readlines()

    today_str = datetime.date.today().isoformat()

    for line in lines:
        pattern = r"(\d+) year old (\w+) (\w+), born in ([\w ]+), (.+) color, (\d+) pounds, from (.+)"
        match = re.match(pattern, line.strip())
        if match:
            age = int(match.group(1))
            sex = match.group(2)
            species = match.group(3).lower()
            season = match.group(4).strip().lower()
            color = match.group(5)
            weight = match.group(6)
            origin = match.group(7)

            birth_date = gen_birth_date(age, season)
            animal_id = gen_unique_id(species, species_counters[species])
            name = names_dict[species][name_indices[species] % len(names_dict[species])]

            species_counters[species] += 1
            name_indices[species] += 1

            info = f"{animal_id}; {name}; birth date: {birth_date.isoformat()}; {color} color; {sex}; {weight} pounds; from {origin}; arrived {today_str}"
            habitat = species.capitalize() + " Habitat"

            if habitat not in habitats:
                habitats[habitat] = []
            habitats[habitat].append(info)

    with open("zooPopulation.txt", "w") as outfile:
        for habitat, animals in habitats.items():
            outfile.write(habitat + ":\n\n")
            for animal in animals:
                outfile.write(animal + "\n")
            outfile.write("\n")

if __name__ == "__main__":
    main()
