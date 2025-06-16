import json

from django.shortcuts import render, get_object_or_404
# Create your views here.
from players.models import *
import colorsys

def generate_color_palette(n):
    colors = []
    for i in range(n):
        hue = i / n
        lightness = 0.5
        saturation = 0.7
        rgb = colorsys.hls_to_rgb(hue, lightness, saturation)
        rgb = tuple(int(255 * c) for c in rgb)
        colors.append('#{:02x}{:02x}{:02x}'.format(*rgb))
    return colors

def interval_packing(intervals):
    rows = []
    for interval in sorted(intervals, key=lambda x: x['start']):
        placed = False
        for row in rows:
            if row[-1]['end'] <= interval['start']:
                row.append(interval)
                interval['row'] = rows.index(row)
                placed = True
                break
        if not placed:
            rows.append([interval])
            interval['row'] = len(rows)
    return intervals

def timeline(pl):

    items = []
    s = 500
    for p in pl:
        if s%20 == 0 and s>0 and p.namefirst:
            items.append({
                "id": p.id,
                "content": p.get_full_name(),
                "start": f"{p.debut}",
                "end": f"{p.finalgame}",
            })
        s-= 1

    return json.dumps(items)
def show_players(request):
    pl = People.objects.all().order_by("namefirst")
    stat = None
    if request.method == 'POST':
        print(request.POST)
        pid = request.POST.getlist('pid')
        print(pid)
        pid = list(map(lambda x: int(x), list(pid)))
        stat = list()
        print(pid)
        for i in pid:
            p = get_object_or_404(People, pk=i)
            print(p)
            #stat.append((p.get_full_name(), list(map(lambda k: k.get_info(), p.batting_set.all()))))
            stat.append((p.get_full_name(), p.get_data_for_radio()))
        print(stat)
    return render(request, template_name="players/players.html", context={"players_list": pl, "player_stat": stat, "items": timeline(pl)})


def radar_charts_view(request):
    if request.method == 'POST':
        print(request.POST)
        pid = request.POST.getlist('pid')
        print(pid)
        pid = list(map(lambda x: int(x), list(pid)))
        stat = list()
        print(pid)
        num_players = len(pid)
        for i in pid:
            p = get_object_or_404(People, pk=i)
            print(p)
            #stat.append((p.get_full_name(), list(map(lambda k: k.get_info(), p.batting_set.all()))))
            stat.append((p.get_full_name(), p.get_data_for_radio()))
        print(stat)
    labels = ["Hmotnost", "Výška", "Úspěšných odpalů %", "Houmranů %", "SB"]  # your axes

    # Example data — in real app you'll load this dynamically
    player_stats = {
        "Player A": [30, 90, 50, 40, 10],
        "Player B": [20, 70, 30, 60, 5],
        "Player C": [40, 100, 60, 20, 15],
        "Player D": [10, 50, 20, 80, 8],
    }

    colors = generate_color_palette(num_players)

    datasets = []
    for idx, (player, stats) in enumerate(player_stats.items()):
        color = colors[idx]
        datasets.append({
            "label": player,
            "data": stats,
            "borderColor": color,
            "backgroundColor": color + "33",  # add transparency
            "fill": True
        })

    context = {
        "labels": json.dumps(labels),
        "datasets": json.dumps(datasets)
    }

    return render(request, 'players/radars.html', context)