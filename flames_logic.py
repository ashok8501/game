def calculate_flames(name1, name2):
    name1 = name1.lower().replace(" ", "")
    name2 = name2.lower().replace(" ", "")

    for ch in name1[:]:
        if ch in name2:
            name1 = name1.replace(ch, "", 1)
            name2 = name2.replace(ch, "", 1)

    count = len(name1 + name2)

    flames = ["Friends", "Love", "Affection", "Marriage", "Enemies", "Siblings"]

    while len(flames) > 1:
        index = (count % len(flames)) - 1
        if index >= 0:
            flames = flames[index+1:] + flames[:index]
        else:
            flames.pop()

    return flames[0]