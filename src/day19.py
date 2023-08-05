#!/usr/bin/env python3

"""
Job Scheduling.

Use DFS to get best possible end count.

Timing:

iterative
python3 = ~13.5 s
pypy = ~3.6 s

recursive
python3 = ~22.2 s
pypy = ~7.2 s
"""

from functools import lru_cache
from aoc import get_digits, map_list, read_input

# ------------------------------------------------------------------------------


def dfs_recursive(blueprint, time):
    (
        ID,
        ROre_Cost,
        RClay_Cost,
        RObs_Cost_Ore,
        RObs_Cost_Clay,
        RGeode_Cost_Ore,
        RGeode_Cost_Obs,
    ) = blueprint

    Max_RCost_ore = max([ROre_Cost, RClay_Cost, RObs_Cost_Ore, RGeode_Cost_Ore])

    best = [0]  # use list so that it become accessible in function XD
    Start = (time, 0, 0, 0, 0, 1, 0, 0, 0)

    def recurse_prep(time_left, ore, clay, obs, geode, r_ore, r_clay, r_obs, r_geode):
        # track best count of geode
        best[0] = max(best[0], geode)

        # calculate ideal end count geode from current state
        # algebracic sequence n/2 [ 2a + n - 1 ] + x
        best_possible = time_left * (2 * r_geode + time_left - 1) // 2 + geode

        if best_possible <= best[0]:
            return geode, f"{geode}"

        # throw away excess robot because
        # it is unnecessary to generate more
        # compare with the maximum amount of resource can be used
        r_ore = min(Max_RCost_ore, r_ore)
        r_clay = min(RObs_Cost_Clay, r_clay)
        r_obs = min(RGeode_Cost_Obs, r_obs)

        # throw away excess resource because
        # we can only use that much
        # compare wih total ore that can be used - amount of ore generated
        # t-1 because resource generated from robot can be used only until next loop
        ore = min(ore, Max_RCost_ore * time_left - r_ore * (time_left - 1))
        clay = min(clay, RObs_Cost_Clay * time_left - r_clay * (time_left - 1))
        obs = min(obs, RGeode_Cost_Obs * time_left - r_obs * (time_left - 1))

        return recurse(time_left, ore, clay, obs, geode, r_ore, r_clay, r_obs, r_geode)

    @lru_cache(maxsize=None)
    def recurse(time_left, ore, clay, obs, geode, r_ore, r_clay, r_obs, r_geode):
        # increase count of each resource
        # for next loop!!!
        ore += r_ore
        clay += r_clay
        obs += r_obs
        geode += r_geode

        # reduce time
        time_left -= 1

        # append possible route
        # by comparing count of resource (before increment) and the respecting cost
        result = {}

        # do nothing
        res, path = recurse_prep(time_left, ore, clay, obs, geode, r_ore, r_clay, r_obs, r_geode)
        result["x->" + path] = res

        # buy geode robot
        if ore - r_ore >= RGeode_Cost_Ore and obs - r_obs >= RGeode_Cost_Obs:
            res, path = recurse_prep(
                time_left, ore - RGeode_Cost_Ore, clay, obs - RGeode_Cost_Obs, geode, r_ore, r_clay, r_obs, r_geode + 1
            )
            result["r_geode->" + path] = res

        # buy obs robot
        if ore - r_ore >= RObs_Cost_Ore and clay - r_clay >= RObs_Cost_Clay:
            res, path = recurse_prep(
                time_left, ore - RObs_Cost_Ore, clay - RObs_Cost_Clay, obs, geode, r_ore, r_clay, r_obs + 1, r_geode
            )
            result["r_obs->" + path] = res

        # buy ore robot
        if ore - r_ore >= ROre_Cost:
            res, path = recurse_prep(time_left, ore - ROre_Cost, clay, obs, geode, r_ore + 1, r_clay, r_obs, r_geode)
            result["r_ore->" + path] = res

        # buy clay robot
        if ore - r_ore >= RClay_Cost:
            res, path = recurse_prep(time_left, ore - RClay_Cost, clay, obs, geode, r_ore, r_clay + 1, r_obs, r_geode)
            result["r_clay->" + path] = res

        k = max(result, key=result.get)
        return result[k], k

    best_overall, path = recurse(*Start)
    print()
    print(ID, path)
    print()
    return best_overall


def dfs_iterative(blueprint, time_left):
    (
        _,
        ROre_Cost,
        RClay_Cost,
        RObs_Cost_Ore,
        RObs_Cost_Clay,
        RGeode_Cost_Ore,
        RGeode_Cost_Obs,
    ) = blueprint

    Max_RCost_ore = max([ROre_Cost, RClay_Cost, RObs_Cost_Ore, RGeode_Cost_Ore])

    best = 0
    Start = (time_left, 0, 0, 0, 0, 1, 0, 0, 0)

    stack = [Start]
    seen = set()

    while stack:
        current = stack.pop()

        (
            time_left,
            ore,
            clay,
            obs,
            geode,
            r_ore,
            r_clay,
            r_obs,
            r_geode,
        ) = current

        # track best count of geode
        best = max(best, geode)

        # calculate ideal end count geode from current state
        # algebracic sequence n/2 [ 2a + n -1 ] + x
        best_possible = time_left * (2 * r_geode + time_left - 1) // 2 + geode

        if best_possible <= best:
            continue

        # throw away excess robot because
        # it is unnecessary to generate more
        # compare with the maximum amount of resource can be used
        r_ore = min(Max_RCost_ore, r_ore)
        r_clay = min(RObs_Cost_Clay, r_clay)
        r_obs = min(RGeode_Cost_Obs, r_obs)

        # throw away excess resource because
        # we can only use that much
        # compare wih total ore that can be used - amount of ore generated
        # t-1 because resource generated from robot can be used only until next loop
        ore = min(ore, Max_RCost_ore * time_left - r_ore * (time_left - 1))
        clay = min(clay, RObs_Cost_Clay * time_left - r_clay * (time_left - 1))
        obs = min(obs, RGeode_Cost_Obs * time_left - r_obs * (time_left - 1))

        current = (time_left, ore, clay, obs, geode, r_ore, r_clay, r_obs, r_geode)

        if current in seen:
            continue

        seen.add(current)

        # if len(seen) % 1000000 == 0:
        #     print(time_left, best, len(seen))

        # increase count of each resource
        # for next loop!!!
        ore += r_ore
        clay += r_clay
        obs += r_obs
        geode += r_geode

        # reduce time
        time_left -= 1

        # append possible route
        # by comparing count of resource (before increment) and the respecting cost

        # do nothing
        stack.append((time_left, ore, clay, obs, geode, r_ore, r_clay, r_obs, r_geode))

        # buy ore robot
        if ore - r_ore >= ROre_Cost:
            stack.append(
                (
                    time_left,
                    ore - ROre_Cost,
                    clay,
                    obs,
                    geode,
                    r_ore + 1,
                    r_clay,
                    r_obs,
                    r_geode,
                )
            )

        # buy clay robot
        if ore - r_ore >= RClay_Cost:
            stack.append(
                (
                    time_left,
                    ore - RClay_Cost,
                    clay,
                    obs,
                    geode,
                    r_ore,
                    r_clay + 1,
                    r_obs,
                    r_geode,
                )
            )

        # buy obs robot
        if ore - r_ore >= RObs_Cost_Ore and clay - r_clay >= RObs_Cost_Clay:
            stack.append(
                (
                    time_left,
                    ore - RObs_Cost_Ore,
                    clay - RObs_Cost_Clay,
                    obs,
                    geode,
                    r_ore,
                    r_clay,
                    r_obs + 1,
                    r_geode,
                )
            )

        # buy geode robot
        if ore - r_ore >= RGeode_Cost_Ore and obs - r_obs >= RGeode_Cost_Obs:
            stack.append(
                (
                    time_left,
                    ore - RGeode_Cost_Ore,
                    clay,
                    obs - RGeode_Cost_Obs,
                    geode,
                    r_ore,
                    r_clay,
                    r_obs,
                    r_geode + 1,
                )
            )
    print(len(seen))
    return best


def solve(day=19, test=False):
    txt = read_input(day, test).splitlines()

    blueprints = map_list(get_digits, txt)

    part1 = 0
    part2 = 1
    dfs = dfs_iterative  # iterative is faster, but recursive helps with showing path
    for i, b in enumerate(blueprints, 1):
        part1 += i * dfs(b, 24)

        if i <= 3:
            part2 *= dfs(b, 32)

    return part1, part2


# ------------------------------------------------------------------------------

# res = solve(test=True)
# assert res == (33, 3472)

res = solve()
assert res == (1144, 19980)
print(*res)

# ------------------------------------------------------------------------------
