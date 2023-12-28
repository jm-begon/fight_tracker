from fight_tracker import Creature, Damage, Game
from fight_tracker import PlayerCharacter as PC
from fight_tracker import conditions
from fight_tracker.arithmetic import DescriptiveInt


def test_normal_encounter() -> None:
    game = Game.init()
    odric = PC.quick_create("P1", "Odric", 16, 20, dexterity=12, charisma=15)

    maudal = PC.quick_create("P2", "Maudal", 12, 15)
    alea = PC.quick_create("P3", "Alea", 14, 19, hp=16, constitution=14)
    gob1 = Creature.quick_create(
        "Goblin 1", "Goblin", DescriptiveInt(13, "leather armor"), 10
    )
    gob2 = Creature.quick_create("Goblin 2", "Goblin", 13, 10)
    gob3 = Creature.quick_create("Goblin 3", "Goblin", 13, 10)
    E = (
        game.create_encounter()  # Return an encounter builder
        .add(odric)
        .add(maudal, 12)
        .add(alea, 16)
        .add(gob1, 11)
        .add(gob2, 15)
        .start()  # Return encounter
    )
    game.renderer(E)
    E  # Render
    alea.concentrate_on("Dancing light")
    gob1 - 6
    game.renderer(E)
    assert int(gob1.hp) == 4
    conditions.Prone() >> gob1
    E + 1
    alea - 20
    alea.stop_concentrating()
    assert int(alea.hp) == -4
    E + 1
    E.add(gob3, 12)
    E

    gob1 - 10
    E + 1
    dmg = gob2 - Damage.as_type(9, "piercing")
    E.end()

    zombie1 = Creature.quick_create("Zombie 1", "Zombie", 13, 10, 10)
    zombie2 = Creature.quick_create("Zombie 2", "Zombie", 13, 10, 10)

    E = game.create_encounter().add(zombie1).add(zombie2).add(odric, 15).start()
    odric - 2
    E.end()
