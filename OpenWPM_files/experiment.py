from __future__ import absolute_import
from six.moves import range
from automation import CommandSequence, TaskManager
from copy import copy
from sys import argv


# The list of sites that we wish to crawl
NUM_BROWSERS = 10

sites_with_treatment = [
    'https://www.youtube.com',
    'https://pnandak1.github.io/a',
    'http://www.youtube.com/'
]
sites_without_treatment = [
    'https://www.youtube.com',
    'http://www.youtube.com/'
]

# Loads the manager preference and NUM_BROWSERS copies of the default browser dictionaries
manager_params, browser_params = TaskManager.load_default_params(NUM_BROWSERS)

# Update browser configuration (use this for per-browser settings)
for i in range(NUM_BROWSERS):
    # Record HTTP Requests and Responses
    browser_params[i]['http_instrument'] = True
    # Enable flash for all three browsers
    browser_params[i]['disable_flash'] = False
    browser_params[i]['headless'] = True

# Update TaskManager configuration (use this for crawl-wide settings)
manager_params['data_directory'] = '~/Desktop/'
manager_params['log_directory'] = '~/Desktop/'

# Instantiates the measurement platform
# Commands time out by default after 60 seconds
manager = TaskManager.TaskManager(manager_params, browser_params)

# Visits the sites with all browsers simultaneously
control = bool(argv[1])

if control:
    sites_to_visit = sites_without_treatment
else:
    sites_to_visit = sites_with_treatment

for site in sites_to_visit:
    command_sequence = CommandSequence.CommandSequence(site)

    # Start by visiting the page
    command_sequence.get(sleep=0, timeout=60)

    # dump_profile_cookies/dump_flash_cookies closes the current tab.
    if control:
        command_sequence.dump_page_source(suffix="control", timeout=120)
    else:
        command_sequence.dump_page_source(suffix="experimental", timeout=120)

    # index='**' synchronizes visits between the three browsers
    manager.execute_command_sequence(command_sequence, index='**')

manager.close()
