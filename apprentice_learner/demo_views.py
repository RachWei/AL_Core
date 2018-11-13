from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

# from apprentice_learner.models import ActionSet
from apprentice_learner.models import Project
from apprentice_learner.models import Operator
from apprentice_learner.models import Agent
from apprentice_learner.views import AGENTS


DEFAULT_AGENT_TYPE = 'WhereWhenHowNoFoa'

@csrf_exempt
def init_tictactoe():
    """
    Creates the demo Project.

    This function creates a project to house of the demo related Opperators and
    agents in the case that it doesn't already exist.
    """
    ttt_available = Operator(name="TTT Available",
                             head="('available', '?s')",
                             conditions="[(('value', '?s'), '?sv'),"
                                        "(('row', '?s'), '?sr'),"
                                        "(('col', '?s'), '?sc'),"
                                        "(lambda x: x > 0, '?sr'),"
                                        "(lambda x: x > 0, '?sc')]",
                             effects="[(('available', '?s'), "
                                     "(lambda x: x == '', '?sv'))]")
    ttt_available.save()

    ttt_horizontal = Operator(name="TTT Horizonal",
                              head="('horizontal_adj', '?s1', '?s2')",
                              conditions="[(('row', '?s1'), '?s1r'),"
                                         "(('row', '?s2'), '?s1r'),"
                                         "(('col', '?s1'), '?s1c'),"
                                         "(('col', '?s2'), '?s2c'),"
                                         "(lambda x, y: abs(x-y) == 1, '?s1c',"
                                         " '?s2c')]",
                              effects="[(('horizontal_adj', '?s1', '?s2'),"
                                      "True)]")
    ttt_horizontal.save()

    ttt_vertical = Operator(name="TTT Vertical",
                            head="('vertical_adj', '?s1', '?s2')",
                            conditions="[(('row', '?s1'), '?s1r'),"
                                       "(('row', '?s2'), '?s2r'),"
                                       "(('col', '?s1'), '?s1c'),"
                                       "(('col', '?s2'), '?s1c'),"
                                       "(lambda x, y: abs(x-y) == 1,"
                                       " '?s1r', '?s2r')]",
                            effects="[(('vertical_adj', '?s1', '?s2'), True)]")
    ttt_vertical.save()

    ttt_diagonal = Operator(name="TTT Diagonal",
                            head="('diag_adj', '?s1', '?s2')",
                            conditions="[(('row', '?s1'), '?s1r'),"
                                       "(('row', '?s2'), '?s2r'),"
                                       "(('col', '?s1'), '?s1c'),"
                                       "(('col', '?s2'), '?s2c'),"
                                       "(lambda x, y: abs(x-y) == 1,"
                                       " '?s1r', '?s2r'),"
                                       "(lambda x, y: abs(x-y) == 1,"
                                       " '?s1c', '?s2c')]",
                            effects="[(('diag_adj', '?s1', '?s2'), True)]")
    ttt_diagonal.save()

    ttt_move = Operator(name="TTT Move",
                        head="('Move', '?r', '?c')",
                        conditions="[(('player', '?s'), '?p'),"
                                   "(('row', '?cell'), '?r'),"
                                   "(('col', '?cell'), '?c'),"
                                   "(('value', '?cell'), '')]",
                        effects="[(('sai', 'board', 'move', (('row', '?r'),"
                                "('col', '?c'),('player', '?p'))), True)]")
    ttt_move.save()

    demo_proj = Project(name="DEMO")
    demo_proj.save()
    demo_proj.feature_set.add(ttt_available)
    demo_proj.feature_set.add(ttt_horizontal)
    demo_proj.feature_set.add(ttt_vertical)
    demo_proj.feature_set.add(ttt_diagonal)
    demo_proj.function_set.add(ttt_move)

    demo_proj.save()

    first_agent_args = {}
    first_agent_args['feature_set'] = demo_proj.compile_features()
    first_agent_args['function_set'] = demo_proj.compile_functions()

    instance = AGENTS[DEFAULT_AGENT_TYPE](**first_agent_args)
    agent = Agent(instance=instance,
                  agent_type=DEFAULT_AGENT_TYPE,
                  name="DEMO_DEFAULT")
    agent.project = demo_proj
    agent.save()

    return demo_proj


def tic_tac_toe(http_request):
    try:
        demo_proj = Project.objects.get(name="DEMO")
    except ObjectDoesNotExist:
        demo_proj = init_tictactoe()

    agents = Agent.objects.filter(project_id=demo_proj.id)
    agent_types = [k for k in AGENTS]

    return render(http_request, 'apprentice_learner/tictactoe.html',
                  {'project_id': demo_proj.id,
                   'agents': agents,
                   'types': agent_types})
