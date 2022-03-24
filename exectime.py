from main import buildTicker

def calculateExecutionTime(function):
    import cProfile
    import pstats

    with cProfile.Profile() as pr:
        function()
    
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()
    stats.dump_stats(filename='profile.prof')

if __name__ == '__main__':
    calculateExecutionTime(buildTicker)
    