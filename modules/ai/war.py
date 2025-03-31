import random
from modules.ai.tools import are_ais_bordering


def declare_war(map, ai1, ai2):
    if are_ais_bordering(map, ai1, ai2):
        declare = random.choice([True, False])
        ai1.at_war = declare
        ai2.at_war = declare
        if declare:
            ai1.war_targets.append(ai2)
            ai2.war_targets.append(ai1)
        
    
    
