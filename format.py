# Copyright (C) 2023 Warren Usui, MIT License
"""
Format the table and write the html file
"""
import json

def get_all_data():
    """
    Read saved data from get_reality, and the team and result data.
    Return this all in one dictionary
    """
    with open("big_save.json", 'r', encoding='utf-8') as ofd:
        big_table = json.load(ofd)
    with open("rbig_save.json", 'r', encoding='utf-8') as ofd:
        rbig_table = json.load(ofd)
    with open("reality.txt", 'r', encoding='utf-8') as ofd:
        rtext = ofd.read()
        reality = list(map(int, rtext.split("|")))
    with open("team_info.txt", 'r', encoding='utf-8') as ofd:
        tdict = {}
        teams = ofd.read()
        for team_txt in teams.split('\n'):
            parts = team_txt.split(":")
            if len(parts) < 3:
                continue
            tdict[int(parts[0])] = {'name': parts[2], 'abbrev': parts[1]}
    return {"big_table": big_table, "tot_w": rbig_table, "reality": reality,
            "team_data": tdict}

def make_topline(data):
    """
    Construct the column headers of the html table
    """
    nm_team = []
    tleft = 64 - len(data['reality'])
    tms = data['reality'][-tleft:]
    tmnos = [tms[i:i + 2] for i in range(0, len(tms), 2)]
    ostr = ''
    for pair in tmnos:
        tcol = []
        boxs = ''
        for tnumb in pair:
            school = data['team_data'][tnumb]['abbrev']
            tcol.append(school)
            boxs += f"<div>{school}</div>"
        boxs = '<th>' + boxs + '</th>'
        ostr += boxs
        nm_team.append(tcol)
    ohead = "<tr><th>NAME</th><th><div>Winning</div><div>Outcomes</div></th>"
    ohead += "<th><div>Probable</div><div>Payoff</div</th>"
    ohead += ostr + "</tr>"
    return nm_team, ohead

def get_ccode(diffy, total):
    """
    Get the style color for a square on the table

    @param integer diffy difference between two team choices
    @param integer total total number of winning combinations
    @return RBG color code
    """
    coloff = 512 * diffy / total
    icol = int(coloff + .5)
    if icol < 256:
        red = icol
        green = 255
    else:
        red = 255
        green = max(511 - icol, 0)
    return f'#{red:02x}{green:02x}00'

def main_rtn():
    """
    Assemble all the parts into one html file.
    Fix the headers and column headings.  Then loop through each
    player (after sorting) and perform the math on the numeric values
    followed by displaying the color coded required outcomes.
    """
    def handle_line_start():
        pctwv = ((entry[1][0][0] + entry[1][0][1]) /
                 (2 ** (63 - len(indata['reality']))))
        twv = indata['tot_w'][entry[0]]
        if twv == 0:
            return ''
        oline = '<tr>'
        for dval in [entry[0], twv, f"{pctwv:08.6f}"]:
            oline += f"<td>{dval}</td>"
        return oline
    indata = get_all_data()
    nm_team, topline = make_topline(indata)
    with open("headers.txt", 'r', encoding='utf-8') as ofd:
        htmltext = ofd.read()
    htmltext += topline
    sorted_cont = sorted(indata['big_table'].items(),
                         key=lambda x : x[1][0][0] + x[1][0][1],
                         reverse=True)
    for entry in sorted_cont:
        oline = handle_line_start()
        if len(oline) == 0:
            break
        for col_cnt in range(len(entry[1])):
            if entry[1][col_cnt][0] == entry[1][col_cnt][1]:
                oline += '<td>*</td>'
                continue
            if entry[1][col_cnt][0] < entry[1][col_cnt][1]:
                team_nm = nm_team[col_cnt][1]
            else:
                team_nm = nm_team[col_cnt][0]
            evalue = [0, 0]
            evalue[0] = entry[1][col_cnt][0]
            evalue[1] = entry[1][col_cnt][1]
            if entry[1][col_cnt][0] * entry[1][col_cnt][1] == 0:
                oline += '<td style="background-color:#000000;'
                oline += f'color:#ffffff">{team_nm}</td>'
            else:
                diffy = evalue[0] - evalue[1]
                if diffy  < 0:
                    diffy = 0 - diffy
                bcolor = get_ccode(diffy, evalue[0] + evalue[1])
                oline += f'<td style="background-color:{bcolor}">'
                oline += f'{team_nm}</td>'
        oline += '</tr>'
        htmltext += oline
    htmltext += "</table></center></body></html>"
    with open("out_table.html", 'w', encoding='utf-8') as ofd:
        ofd.write(htmltext)

if __name__ == "__main__":
    main_rtn()
