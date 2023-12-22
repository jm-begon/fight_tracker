from fight_tracker import Creature, Game, conditions

if __name__ == "__main__":
    game, _reg = Game.init()
    E, R = game.encounter, game.renderer

    R << conditions.Blinded()
    R << conditions.Grappled()
    R << conditions.Unconscious()
    R << conditions.Exhausted()
