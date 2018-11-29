import time


NUM_VIDEOS = 2

def visit(command_sequence):
    command_sequence.get(sleep=0, timeout=60)

def scroll(command_sequence):
    command_sequence.page_down(count=5)

def save_page_source(command_sequence):
    command_sequence.dump_page_source(suffix='__BY_GROUP', timeout=120)

def click_on_play(command_sequence, iframe_id=0):
    command_sequence.click(xpath='//*[@id="Play"]')

def click_on_video(command_sequence, iframe_id=0):
    command_sequence.switch_to_frame(idx=iframe_id)
    command_sequence.click(xpath='/html/body/div/div/div[4]/button')
    command_sequence.reset_focus()

def click_jack(command_sequence, iframe_id=0):
    command_sequence.click(xpath='//*[@id="player_uid_644712413_1"]/div[4]/div[1]')

def click_on_videos(command_sequence):
    for i in range(NUM_VIDEOS):
        click_on_video(command_sequence, i)

def extract_topics(lines):
    topics = []
    for l in lines:
        if "- Topic" in l:
            topic_str = l.split("- Topic")[0][-20:]
            if ">" in topic_str:
                topic = topic_str.split(">")[-1]
                topics.append(topic.strip())
            elif "\"" in topic_str:
                topic = topic_str.split("\"")[-1]
                topics.append(topic.strip())
    return list(set(topics))

def sum_cols(m):
    res = [0] * len(m[0])
    for i in range(len(m[0])):
        for j in range(len(m)):
            res[i] += m[j][i]
    return res

def normalized_difference(m1, m2):
    diff = 0.0
    for i in range(len(m1)):
        for j in range(len(m1[0])):
            diff += abs(m1[i][j] - m2[i][j])
    return diff / (len(m1) * len(m1[0]))

def test_statistic_old(features, m1, m2):
    summary_exp = sum_cols(m1)
    summary_con = sum_cols(m2)
    print "Export CSV"
    print "Topic,Experimental,Control"
    for i in range(len(features)):
        print features[i] + "," + str(summary_exp[i]) + "," + str(summary_con[i])
    print "Normalized Difference:", normalized_difference(m1, m2)

def test_statistic(observed_values, unit_assignments):
    m1 = []
    m2 = []
    for block_num, block in enumerate(observed_values):
        for browser_id, data in enumerate(block):
            if unit_assignments[block_num][browser_id]:
                m1.append(data)
            else:
                m2.append(data)
    return normalized_difference(m1, m2)
