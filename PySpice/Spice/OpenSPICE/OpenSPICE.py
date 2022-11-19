#!/usr/bin/env python3
from .netlist import parse
from .eqnstr import gen_eqns_top
import sys
from .solve import TransientSolverStrategy, OpPtSolverStrategy
from .genout import gen_out_txt

def run(input_fname, output_fname):
    with open(input_fname, "r") as f:
        file_txt = f.read()
    pdata = parse(file_txt)
    eqns = gen_eqns_top(pdata)
    # TODO Support multiple test types?
    # TODO Wrap this logic in a context object
    if pdata["ctrl"][0]["test_type"] == "tran":
        strat = TransientSolverStrategy(eqns, pdata["ctrl"][0])
    else:
        assert pdata["ctrl"][0]["test_type"] == "op_pt"
        strat = OpPtSolverStrategy(eqns)
    soln = strat.solve_eqns()
    gen_out_txt(output_fname, pdata["title"], pdata["ctrl"][0]["test_type"], soln, pdata["nodes"])

if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2])
