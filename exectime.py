from main import buildTicker,buildTickerParallel,buildTickerParallel2
import timeit
import cProfile
import pstats

def calculateExecutionTime(function):
    with cProfile.Profile() as pr:
        function()
    
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()
    stats.dump_stats(filename=f'{function.__name__}.prof')

def testWithTimeit(funclist,no_of_tries,filename=None):
    for function in funclist:
        print(f'Now testing {function.__name__}')
        time_taken = timeit.timeit(stmt=f'{function.__name__}()',number=no_of_tries,setup=f'from __main__ import {function.__name__}')
        result  = f'Function:{function.__name__} | Time Taken: {time_taken} for {no_of_tries} runs'
        print(result)
        if filename != None:
            with open(filename,"a") as file:
                file.write(result)
                file.write('\n')



if __name__ == '__main__':
    # calculateExecutionTime(buildTickerParallel2)
    testWithTimeit([buildTicker,buildTickerParallel,buildTickerParallel2],10,'threadresult.txt')

    