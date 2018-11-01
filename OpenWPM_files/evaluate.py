import os


def read_files(sources_dir):
    experimental_lines = []
    control_lines = []
    for filename in os.listdir(sources_dir):
        with open(sources_dir + "/" + filename, 'r') as data_file:
            if "control" in filename:
                control_lines.append(data_file.readlines())
            else:
                experimental_lines.append(data_file.readlines())
    return experimental_lines, control_lines


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


def topic_difference(t1, t2):
    diff = 0.0
    counted = []
    for t in t1:
        if t not in t2:
            diff += 1
            counted.append(t)
    for t in t2:
        if t not in t1 and t not in counted:
            diff += 1
    return diff


def gen_feature_matrix(l1, l2):
    all_topics = []
    for tl in l1:
        for t in tl:
            if t not in all_topics:
                all_topics.append(t)
    for tl in l2:
        for t in tl:
            if t not in all_topics:
                all_topics.append(t)
    exp_matrix = []
    for tl in l1:
        vec = [0] * len(all_topics)
        for t in tl:
            i = all_topics.index(t)
            vec[i] = 1
        exp_matrix.append(vec)
    con_matrix = []
    for tl in l2:
        vec = [0] * len(all_topics)
        for t in tl:
            i = all_topics.index(t)
            vec[i] = 1
        con_matrix.append(vec)
    return exp_matrix, con_matrix, all_topics


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


def main(sources_dir):
    experimental_lines, control_lines = read_files(sources_dir)
    exp_topics_vec = []
    con_topics_vec = []
    for l in experimental_lines:
        exp_topics = extract_topics(l)
        exp_topics_vec.append(exp_topics)
    for l in control_lines:
        con_topics = extract_topics(l)
        con_topics_vec.append(con_topics)
    print exp_topics_vec
    print con_topics_vec
    for t1, t2 in zip(exp_topics_vec, con_topics_vec):
        print topic_difference(t1, t2)
    exp_m, con_m, features = gen_feature_matrix(exp_topics_vec, con_topics_vec)
    con_m = con_m[:len(exp_m)]
    print "Experimental Group:"
    for v in exp_m:
        print(v)
    print "Control Group:"
    for v in con_m:
        print(v)
    print "Summaries"
    summary_exp = sum_cols(exp_m)
    summary_con = sum_cols(con_m)
    print summary_exp
    print summary_con
    print "Export CSV"
    print "Topic,Experimental,Control"
    for i in range(len(features)):
        print features[i] + "," + str(summary_exp[i]) + "," + str(summary_con[i])
    print "Normalized Difference:", normalized_difference(exp_m, con_m)


if __name__ == "__main__":
    # Give the directory where the dumped page sources are
    main("sources")
