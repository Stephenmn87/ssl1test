import random

from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'Giftest'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    pass

# FUNCTIONS

## if we wanted to initialize some random values, could do here, though probably easier to wait until they're needed
#def creating_session(subsession: Subsession):

    #from numpy import random
    #import itertools
    #strategyMethod = itertools.cycle([True, False])
    #for p in subsession.get_players():
    #    p.participant.STRATEGY_ELICIT = next(strategyMethod)

# PAGES
class Gifshow(Page):
    timeout_seconds = 28

    @staticmethod
    def vars_for_template(player: Player):
       return dict(var='1')

page_sequence = [Gifshow]
