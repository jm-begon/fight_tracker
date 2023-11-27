from fight_tracker import Damage
from fight_tracker import conditions
from fight_tracker.arithmetic import DescriptiveInt

if __name__ == '__main__':
    from fight_tracker import Creature, Game, NPC
    from fight_tracker import PlayerCharacter as PC

    game, _reg = Game.init()
    E, R = game.encounter, game.renderer

    odric = PC("P1", "Odric", 16, 20, 20).set_saving_throws(
        CHA=2,
    ).set_ability_modifier(DEX=1)
    maudal = PC("P2", "Maudal", 12, 15)
    alea = PC("P3", "Alea", 14, 16, 19).set_saving_throws(
        CON=1
    )

    gob1 = Creature("Goblin 1", DescriptiveInt(13, "leather armor"), 10, 10)
    gob2 = Creature("Goblin 2", 13, 10, 10)

    # init
    _reg(odric)
    _reg(maudal, 12)
    _reg(alea, 16)
    _reg(gob1, 11)
    _reg(gob2, 15)

    E.start()
    R << E
    alea.concentrate_on("Dancing light")
    gob1 - 6
    conditions.Prone() >> gob1
    E.next_turn()
    R << E
    alea - 20
    alea.stop_concentrating()
    E.next_turn()
    R << E
    gob1 - 10
    E.next_turn()
    R << E
    dmg = gob2 - Damage.as_type(9, "piercing")
    E.next_turn()
    E.end()

    game.new_encounter()
    gob1 = Creature("Goblin 3", 13, 10, 10)
    gob2 = Creature("Goblin 4", 13, 10, 10)
    _reg(gob1, 15)
    _reg(gob2, 15)
    _reg(alea, 10)
    E = game.encounter
    E.start()
    R << E
    alea - 2
    E.end()






