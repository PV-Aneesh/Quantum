import dwave
import dwave.cloud
from dimod.reference.samplers import ExactSolver
import dwave_networkx as dnx
import networkx as nx
from dwave.system import DWaveSampler, EmbeddingComposite

sampler2 = EmbeddingComposite(DWaveSampler(
    endpoint='https://cloud.dwavesys.com/sapi',
    token='DEV-d9500e99062cdd39d17bc2f4a0993eb1cae4e053', 
    solver='DW_2000Q_5'))
sampler = ExactSolver()
s5 = nx.star_graph(4)
print(dnx.min_vertex_cover(s5, sampler))
print(dnx.min_vertex_cover(s5, sampler2))
print(s5)
