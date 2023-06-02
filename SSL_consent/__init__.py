import random

from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'Consent'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    consent1 = models.BooleanField(blank=True)
    consent2 = models.BooleanField(blank=True)
    consent3 = models.BooleanField(blank=True)
    consent4 = models.BooleanField(blank=True)
    consent5 = models.BooleanField(blank=True)
    consent6 = models.BooleanField(blank=True)
    consent7 = models.BooleanField(blank=True)
    consent8 = models.BooleanField(blank=True)


# FUNCTIONS

## if we wanted to initialize some random values, could do here, though probably easier to wait until they're needed
#def creating_session(subsession: Subsession):

    #from numpy import random
    #import itertools
    #strategyMethod = itertools.cycle([True, False])
    #for p in subsession.get_players():
    #    p.participant.STRATEGY_ELICIT = next(strategyMethod)

# PAGES
class ConsentForm(Page):
    form_model = 'player'
    form_fields = ['consent1','consent2','consent3','consent4','consent5','consent6','consent7','consent8']

    @staticmethod
    def error_message(player, values):
        print('hi')
        if values['consent1'] != True or values['consent2'] != True or values['consent3'] != True or values['consent4'] != True or values['consent5'] != True or values['consent6'] != True or values['consent7'] != True or values['consent8'] != True:
            return 'You must check all boxes to indicate you consent to take part'

page_sequence = [ConsentForm]
