HEROS = ["Dehaka","Tychus"]

def is_hero(unit_type: str):
    for hero in HEROS:
        if unit_type.startswith(hero):
            return True, hero

    return False, None