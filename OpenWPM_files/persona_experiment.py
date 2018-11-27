from __future__ import absolute_import
from experiment.Experiment import Experiment, Stage


NUM_VIDEOS = 2


def visit_and_scroll(command_sequence):
    command_sequence.get(sleep=0, timeout=60)
    command_sequence.page_down(count=5)

def save_page_source(command_sequence):
    command_sequence.dump_page_source(suffix='__BY_GROUP', timeout=120)

def click_on_video(command_sequence, iframe_id=0):
    command_sequence.switch_to_frame(idx=iframe_id)
    command_sequence.click(xpath='/html/body/div/div/div[4]/button')
    command_sequence.reset_focus()

def click_on_videos(command_sequence):
    for i in range(NUM_VIDEOS):
        click_on_video(command_sequence, i)

def main():
    persona = Experiment(num_browsers=20)
    persona.add_stage(
        "start", "all", "https://www.youtube.com", 
        [visit_and_scroll]
    )
    persona.add_stage(
        "treatment", "control", "https://pnandak1.github.io/a/", 
        [visit_and_scroll, click_on_video]
    )
    persona.add_stage(
        "measurement", "all", "https://www.youtube.com", 
        [visit_and_scroll, save_page_source]
    )
    persona.run()


if __name__ == "__main__":
    main()
