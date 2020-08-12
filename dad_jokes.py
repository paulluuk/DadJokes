def get_data():
    data = {}
    with open("child_definitions.txt", "r") as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip()
        parts = line.split(":")
        name = parts[0].lower()
        pos = parts[1]
        desc = parts[2].strip(".")
        data[name] = (pos, desc)
    return data


def a_vs_an(x):
    if len(x) >= 2:
        A = "A " in x[:4]
        An = "An " in x[:4]
        a = "a " in x[:4]
        an = "an " in x[:4]
        if A or An or a or an:
            return ""
    if x[0] in "aeoyui":
        return "An"
    else:
        return "A"


def overlap(word1, word2):
    for i in range(len(word1), 0, -1):
        if word1[:i] == word2[-i:]:
            return i
    return 0


def combine(word1, word2):
    o = overlap(word1, word2)
    return "".join([word2[:-o], word1[:o], word1[o:]])


def generate_jokes():
    d = get_data()
    words = d.keys()
    for word1 in words:
        for word2 in words:
            if word1 != word2:
                pos1, desc1 = d[word1]  # todo: find a use for part-of-sentence
                pos2, desc2 = d[word2]  # todo: find a use for part-of-sentence

                question, answer = find_overlap(desc2, word1, word2)
                if question:
                    yield question, answer

                question, answer = find_third_meaning(desc1, desc2, word1, word2, words)
                if question:
                    yield question, answer


def find_third_meaning(desc1, desc2, word1, word2, words):
    mix1 = word1 + word2
    mix2 = word1 + "-" + word2
    mix3 = word1 + " " + word2
    for mix in [mix1, mix2, mix3]:
        if mix in words:
            if ";" in desc1:
                desc1 = desc1.split(";")[0]
            if ";" in desc2:
                desc2 = desc2.split(";")[0]
            that_idx_1 = desc1.index("that") + 4 if "that" in desc1 else -1
            that_idx_2 = desc2.index("that") + 4 if "that" in desc2 else -1
            which_idx_1 = desc1.index("which") + 5 if "which" in desc1 else -1
            which_idx_2 = desc2.index("which") + 5 if "which" in desc2 else -1
            idx1 = max(that_idx_1, which_idx_1)
            idx2 = max(that_idx_2, which_idx_2)
            if idx2 != -1:
                desc = desc1 + " which" + desc2[idx2:]
            elif idx1 != -1:
                desc = desc2 + " which" + desc1[idx1:]
            else:
                desc = desc1 + " and " + desc2
            question = f"What do you call {desc}?"
            answer = f"{a_vs_an(mix)} {mix} ({word1}+{word2})"
            return question, answer
    return None, None


def find_overlap(desc2, word1, word2):
    o = overlap(word1, word2)
    if o >= 3 or o == len(word1) or o == len(word2):
        combined = combine(word1, word2)
        if combined != word1 and combined != word2:
            question = f"What do you call a kind of {word1} that is {desc2}?"
            answer = f"{a_vs_an(combined)} {combined} ({word2}+{word1})"
            return question, answer
    return None, None


if __name__ == "__main__":
    with open("generated_jokes.txt", "w") as jokes:
        for question, answer in generate_jokes():
            jokes.write(question + "\n")
            jokes.write(answer + "\n")
