from __future__ import absolute_import
from six.moves import range
from automation import CommandSequence, TaskManager
from copy import copy
from sys import argv
from random import shuffle


NUM_BROWSERS = 4
NUM_VIDEOS = 2


def randomized_assignments(num_browsers):
    # map browser index to control/experimental
    browser_indicies = []
    for i in range(num_browsers):
        browser_indicies.append(i)
    shuffle(browser_indicies)
    half = int(num_browsers / 2)
    assignments = {}
    for i in range(num_browsers):
        if i < half:
            # Control
            assignments[browser_indicies[i]] = True
        else:
            # Experimental
            assignments[browser_indicies[i]] = False
    return assignments

def click_on_video(command_sequence, iframe_id):
    command_sequence.switch_to_frame(idx=iframe_id)
    command_sequence.click(xpath='/html/body/div/div/div[4]/button')
    command_sequence.reset_focus()


if __name__ == "__main__":
    # Loads the manager preference and NUM_BROWSERS copies of the default browser dictionaries
    manager_params, browser_params = TaskManager.load_default_params(NUM_BROWSERS)
    assignments = randomized_assignments(NUM_BROWSERS)

    # Update browser configuration (use this for per-browser settings)
    for i in range(NUM_BROWSERS):
        # Record HTTP Requests and Responses
        browser_params[i]['http_instrument'] = True
        # Enable flash for all three browsers
        browser_params[i]['disable_flash'] = False
        browser_params[i]['headless'] = True
        browser_params[i]['control'] = assignments[i]

    # Update TaskManager configuration (use this for crawl-wide settings)
    manager_params['data_directory'] = '~/Desktop/'
    manager_params['log_directory'] = '~/Desktop/'

    # Instantiates the measurement platform
    # Commands time out by default after 60 seconds
    manager = TaskManager.TaskManager(manager_params, browser_params)

    # The list of sites that we wish to crawl
    sites_with_group = [
        # ('https://www.youtube.com', 'both', 'start'),
        ('https://pnandak1.github.io/a/', 'control', 'treatment'),
        # ('http://www.youtube.com/', 'both', 'measurement')
    ]

    for site, group, stage in sites_with_group:
        command_sequence = CommandSequence.CommandSequence(site)
    
        command_sequence.get(sleep=0, timeout=60)

        if stage == 'start' or stage == 'measurement':
            command_sequence.page_down(count=5)
        
        if stage == 'treatment':
            for i in range(NUM_VIDEOS):
                click_on_video(command_sequence, i)

        if stage == 'measurement':
            command_sequence.dump_page_source(suffix='__BY_GROUP', timeout=120)

        if stage == 'treatment' and group == 'control':
            manager.execute_command_sequence(command_sequence, index='control')
        else:
            manager.execute_command_sequence(command_sequence, index='**')

    manager.close()
