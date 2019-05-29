# BSD-3-Clause License
#
# Copyright 2017 Orange
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from pydcop.algorithms import ComputationDef, AlgorithmDef
from pydcop.algorithms.maxsum import VariableComputation, FactorComputation, \
    build_computation
from pydcop.computations_graph.factor_graph import build_computation_graph
from pydcop.dcop.objects import Variable, Domain
from pydcop.dcop.relations import constraint_from_str


def test_comp_creation():
    d = Domain("d", "", ["R", "G"])
    v1 = Variable("v1", d)
    v2 = Variable("v2", d)
    c1 = constraint_from_str("c1", "10 if v1 == v2 else 0", [v1, v2])
    graph = build_computation_graph(None, constraints=[c1], variables=[v1, v2])

    comp_node = graph.computation("c1")
    algo_def = AlgorithmDef.build_with_default_param("maxsum")
    comp_def = ComputationDef(comp_node, algo_def)

    comp = FactorComputation(comp_def)
    assert comp is not None
    assert comp.name == "c1"
    assert comp.factor == c1

    comp_node = graph.computation("v1")
    algo_def = AlgorithmDef.build_with_default_param("maxsum")
    comp_def = ComputationDef(comp_node, algo_def)

    comp = VariableComputation(comp_def)
    assert comp is not None
    assert comp.name == "v1"
    assert comp.variable == v1
    assert comp.factor_names == ["c1"]


def test_comp_creation_with_factory_method():
    d = Domain("d", "", ["R", "G"])
    v1 = Variable("v1", d)
    v2 = Variable("v2", d)
    c1 = constraint_from_str("c1", "10 if v1 == v2 else 0", [v1, v2])
    graph = build_computation_graph(None, constraints=[c1], variables=[v1, v2])

    comp_node = graph.computation("c1")
    algo_def = AlgorithmDef.build_with_default_param("maxsum")
    comp_def = ComputationDef(comp_node, algo_def)

    comp = build_computation(comp_def)
    assert comp is not None
    assert comp.name == "c1"
    assert comp.factor == c1

    comp_node = graph.computation("v1")
    algo_def = AlgorithmDef.build_with_default_param("maxsum")
    comp_def = ComputationDef(comp_node, algo_def)

    comp = build_computation(comp_def)
    assert comp is not None
    assert comp.name == "v1"
    assert comp.variable == v1
    assert comp.factor_names == ["c1"]