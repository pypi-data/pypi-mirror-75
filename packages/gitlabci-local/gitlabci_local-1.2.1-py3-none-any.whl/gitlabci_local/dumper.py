#!/usr/bin/env python3

# Libraries
import oyaml as yaml

# Components
from .utils import nameCheck

# Dumper
def dumper(options, jobs):

    # Variables
    configuration = dict()
    result = False

    # Prepare configuration results
    if options.names:
        for job in options.names:
            if nameCheck(job, jobs, options.no_regex):
                configuration[job] = jobs[job]
                result = True
    else:
        configuration = jobs
        result = True

    # Dump configuration results
    print(yaml.dump(configuration, indent=2))
    print(' ', flush=True)

    # Result
    return result
