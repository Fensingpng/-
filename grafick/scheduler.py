def generate_schedule(people_data, posts, days):
    load = {p: 0 for p in people_data}
    schedule = {p: {} for p in people_data}

    for day in days:
        used_today = set()

        for post_index, post in enumerate(posts[1:], start=1):
            available = []

            for p, info in people_data.items():
                if day in info["blocked"]:
                    continue
                if p in used_today:
                    continue

                score = load[p]
                if info["pref"] == post:
                    score -= 0.5

                available.append((score, p))

            available.sort()
            chosen = [p for _, p in available[:2]]

            for person in chosen:
                schedule[person][day] = post_index
                load[person] += 1
                used_today.add(person)

    return schedule
