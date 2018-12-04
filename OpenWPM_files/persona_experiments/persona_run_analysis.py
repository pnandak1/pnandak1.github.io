from __future__ import absolute_import
from persona_common import *
from sys import argv


def run_analysis():
    analysis = Analysis(
        data_path=str(argv[1]).strip() + "_data.txt",
        test_statistic=test_statistic,
        truncate = 5
    )
    analysis.load_data()
    analysis.perform()
    result = analysis.get_results()
    return result

def main():
    result = run_analysis()
    print "p-value: " + str(result)

if __name__ == "__main__":
    if __package__ is None:
        import sys
        from os import path
        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
        from experiment.Experiment import Experiment, Stage
        from analysis.Analysis import Analysis
    else:
        from ..experiment.Experiment import Experiment, Stage
        from ..analysis.Analysis import Analysis
    main()
