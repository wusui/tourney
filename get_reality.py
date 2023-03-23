# Copyright (C) 2023 Warren Usui, MIT License
"""
Compute all possible future outcomes
"""
import json
from datetime import datetime
import itertools

def rhist(rlist):
    """
    Return a list of team numbers from a list of index values
    """
    retv = 64 * [0]
    for entry in rlist:
        retv[entry - 1] += 1
    return retv

def get_tourney_state():
    """
    Read and format user pick data
    """
    with open("reality.txt", "r", encoding="utf-8") as mreality:
        rdata = mreality.read()
        return list(map(int, rdata.split("|")))

def score_peeps(reality):
    """
    Extract best score and point values for all entrants
    """
    with open("picks.json", 'r', encoding='utf-8') as ofile:
        pick_data = json.load(ofile)
    new_bestv = 0
    ret_peep = {}
    for keyv in pick_data:
        score = 0
        our_picks = rhist(pick_data[keyv])
        for ent in range(len(reality)):
            sval = min(our_picks[ent], rhist(reality)[ent])
            if sval > 0:
                score += 2 ** sval - 1
        score *= 10
        if score > new_bestv:
            new_bestv = score
        ret_peep[keyv] = score
    return [new_bestv, ret_peep]

def reduce_no(field):
    """
    Save max value if passed (used by map function)
    """
    def reduce_no_inner(indx):
        if field[indx] == max(field):
            return indx
        return -1
    return reduce_no_inner

def mk_data(sub_list, pos_fut):
    """
    Extract more possible outcomes
    """
    retv = []
    for evls in list(enumerate(pos_fut)):
        retv.append(sub_list[evls[0]][evls[1]])
    return retv

def scan_all_outcomes():
    """
    Try all possible outcomes.  A bulk of the cpu time is consumed here
    """
    def get_future(win_list):
        if len(win_list) == 63:
            answers.append(win_list)
            return
        game_inds = list(itertools.product([0, 1],
                                     repeat=(64 - len(win_list)) // 2))
        wlist = rhist(win_list)
        x_pos = list(filter(lambda a: a>=0, list(map(reduce_no(wlist),
                                                 range(len(wlist))))))
        x_pos1 = list(map(lambda a: a+1, x_pos))
        sub_list = [x_pos1[n:n+2] for n in range(0, len(x_pos1), 2)]
        for pos_fut in game_inds:
            get_future(win_list + mk_data(sub_list, pos_fut))
    answers = []
    get_future(get_tourney_state())
    print(datetime.now())
    result = {}
    spt = len(get_tourney_state())
    edis = (64 - spt) // 2
    for outcome in answers:
        rkey = "-".join(list(map(str, outcome[spt:spt + edis])))
        lresult = []
        sample = score_peeps(outcome)
        for keyv in list(sample[1]):
            if sample[1][keyv] == sample[0]:
                lresult.append(keyv)
        if rkey in result:
            result[rkey].append(lresult)
        else:
            result[rkey] = [lresult]
    print(datetime.now())
    return result

def org_outcomes(result):
    """
    Organize the outcomes fron result paramenter into a format that is
    easier to display (data saved in big_table and rbig_table
    """
    wper_rx = {}
    wper_cx = {}
    def set_wper(result):
        for rkey in list(result):
            wper_rx[rkey] = {}
            wper_cx[rkey] = {}
            for winset in result[rkey]:
                for indv in winset:
                    value = 1 / len(winset)
                    if indv in wper_rx[rkey]:
                        wper_rx[rkey][indv] += value
                        wper_cx[rkey][indv] += 1
                    else:
                        wper_rx[rkey][indv] = value
                        wper_cx[rkey][indv] = 1
    set_wper(result)
    big_table = {}
    rbig_table = {}
    ssize = len(list(wper_rx)[0].split('-'))
    tleft = dict(list(map(lambda a: [a[1], a[0]],
                          enumerate(get_tourney_state()[(0 - ssize * 2):]))))
    with open("picks.json", 'r', encoding='utf-8') as ofile:
        people = list(json.load(ofile))
    for peep in people:
        big_table[peep] = list(map(lambda _: [0, 0], range(ssize)))
        rbig_table[peep] = 0
    for nkeys in list(wper_rx):
        for pkeys in(list(wper_rx[nkeys])):
            for xind in list(map(lambda a: tleft[a],
                                 list(map(int, nkeys.split('-'))))):
                big_table[pkeys][xind // 2][xind % 2] += wper_rx[nkeys][pkeys]
                if xind < 2:
                    rbig_table[pkeys] += wper_cx[nkeys][pkeys]
    with open("big_save.json", 'w', encoding='utf-8') as ofd:
        json.dump(big_table, ofd)
    with open("rbig_save.json", 'w', encoding='utf-8') as ofd:
        json.dump(rbig_table, ofd)

def get_reality():
    """
    Wrap call so there is one entry point here
    """
    org_outcomes(scan_all_outcomes())

if __name__ == "__main__":
    get_reality()
