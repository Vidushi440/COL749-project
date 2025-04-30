import json
from copy import deepcopy

def read_preferences(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data['men'], data['women']

def gale_shapley(men_prefs, women_prefs):
    men_prefs = deepcopy(men_prefs)
    women_prefs = deepcopy(women_prefs)
    free_men = list(men_prefs.keys())
    engaged = {}  # woman: man
    proposals = {man: [] for man in men_prefs}
    women_rank = {w: {m: i for i, m in enumerate(women_prefs[w])} for w in women_prefs}

    while free_men:
        man = free_men.pop(0)
        for woman in men_prefs[man]:
            if woman not in proposals[man]:
                proposals[man].append(woman)
                if woman not in engaged:
                    engaged[woman] = man
                    break
                else:
                    current = engaged[woman]
                    if women_rank[woman][man] < women_rank[woman][current]:
                        engaged[woman] = man
                        free_men.append(current)
                        break

    matching = {man: None for man in men_prefs}
    for woman, man in engaged.items():
        matching[man] = woman
    return matching

def truncate_preferences(men_prefs, matching):

    truncated = {}
    for man, prefs in men_prefs.items():
        partner = matching[man]
        idx = prefs.index(partner)
        truncated[man] = prefs[:idx+1]
    return truncated

def top_trading_cycle(men_prefs, initial_matching):
    
    ownership = {man: initial_matching[man] for man in men_prefs}
    woman_owner = {w: m for m, w in ownership.items()}
    truncated_prefs = truncate_preferences(men_prefs, initial_matching)
    assigned = {}
    unassigned_men = set(men_prefs.keys())
    unassigned_women = set(woman_owner.keys())

    while unassigned_men:
        
        pointers = {}
        for man in unassigned_men:
            for woman in truncated_prefs[man]:
                if woman in unassigned_women:
                    pointers[man] = woman
                    break
        
        woman_points = {w: woman_owner[w] for w in unassigned_women}

        visited = set()
        cycles = []
        for man in unassigned_men:
            if man in visited:
                continue
            path = []
            current = man
            while current not in path:
                path.append(current)
                next_woman = pointers[current]
                current = woman_points[next_woman]

            cycle_start = path.index(current)
            cycle = path[cycle_start:]
            cycles.append(cycle)
            visited.update(cycle)

        men_to_remove = set()
        women_to_remove = set()
        for cycle in cycles:
            for man in cycle:
                woman = pointers[man]
                assigned[man] = woman
                men_to_remove.add(man)
                women_to_remove.add(woman)
        unassigned_men -= men_to_remove
        unassigned_women -= women_to_remove

    return assigned

def modify_preferences_for_coalition(men_prefs, coalition_matching):
    
    modified = {}
    for man, prefs in men_prefs.items():
        assigned_woman = coalition_matching[man]
        new_prefs = [assigned_woman] + [w for w in prefs if w != assigned_woman]
        modified[man] = new_prefs
    return modified

def calculate_happiness(men_prefs, matching):
    
    happiness = {}
    for man, prefs in men_prefs.items():
        partner = matching[man]
        if partner in prefs:
            score = len(prefs) - prefs.index(partner)
        else:
            score = 0
        happiness[man] = score
    return happiness

def total_happiness(happiness_dict):
    
    return sum(happiness_dict.values())

def write_output(filename, men_prefs, women_prefs, m0, coalition, final, happiness_m0, happiness_final):
    total_happiness_m0 = total_happiness(happiness_m0)
    total_happiness_final = total_happiness(happiness_final)

    with open(filename, 'w') as f:
        f.write("Stable Matching with Men’s Coalition (House-Swapping/Strict Core)\n")
        f.write("="*60 + "\n\n")
        f.write("Original Men Preferences:\n")
        for man, prefs in men_prefs.items():
            f.write(f"  {man}: {prefs}\n")
        f.write("\nOriginal Women Preferences:\n")
        for woman, prefs in women_prefs.items():
            f.write(f"  {woman}: {prefs}\n")
        f.write("\n")

        f.write("Step 1: Men-Optimal Matching (M0) via Gale-Shapley:\n")
        for man, woman in m0.items():
            f.write(f"  {man} → {woman}\n")
        f.write("\n")

        f.write("Step 2: Coalition Matching (Strict Core via TTC):\n")
        for man, woman in coalition.items():
            f.write(f"  {man} → {woman}\n")
        f.write("\n")

        f.write("Step 3: Final Matching (Enforced by Coalition):\n")
        for man, woman in final.items():
            f.write(f"  {man} → {woman}\n")
        f.write("\n")

        f.write("Happiness Scores (higher is better, max = #women, top choice = max):\n")
        f.write("  (M0)    (Final)\n")
        for man in men_prefs:
            f.write(f"{man}: {happiness_m0[man]:>3}     {happiness_final[man]:>3}\n")
        f.write("\n")
        f.write(f"Total happiness (higher is better):\n")
        f.write(f"  M0:    {total_happiness_m0}\n")
        f.write(f"  Final: {total_happiness_final}\n\n")

        f.write("Notes:\n")
        f.write("- Happiness is defined as len(prefs) - index of assigned partner (higher is better, top choice = max).\n")
        f.write("- The coalition (strict core) guarantees that no man is worse off than in M0, and some may be strictly better off.\n")
        f.write("- If the coalition and M0 matchings are identical, no strict core improvement was possible.\n")

def main():
    # Load preferences
    men_prefs, women_prefs = read_preferences('prefs.json')

    # Step 1: Gale-Shapley men-optimal matching
    m0_matching = gale_shapley(men_prefs, women_prefs)

    # Step 2: Coalition matching via Top Trading Cycle
    coalition_matching = top_trading_cycle(men_prefs, m0_matching)

    # Step 3: Modify men's preferences to enforce coalition
    modified_men_prefs = modify_preferences_for_coalition(men_prefs, coalition_matching)

    # Step 4: Final matching after coalition
    final_matching = gale_shapley(modified_men_prefs, women_prefs)

    # Calculate happiness (higher is better)
    happiness_m0 = calculate_happiness(men_prefs, m0_matching)
    happiness_final = calculate_happiness(men_prefs, final_matching)

    # Write detailed output
    write_output(
        'output.txt',
        men_prefs,
        women_prefs,
        m0_matching,
        coalition_matching,
        final_matching,
        happiness_m0,
        happiness_final
    )

if __name__ == '__main__':
    main()
