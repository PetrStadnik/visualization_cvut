import json
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from players.models import *
import colorsys


def line_chart_data(pl: [People]):
    charts = []
    for p in pl:
        pdata = p.get_data_for_linear()
        labels = pdata["years"]
        pdata.pop("years")
        datasets = []
        colors = generate_color_palette(len(pdata.keys()))
        for k in pdata.keys():
            color = colors.pop()
            bg_color = str(color)+"33"
            datasets.append({
                'label': k,
                'data': pdata[k],
                'borderColor': color,
                'backgroundColor': bg_color,
            })

        charts.append({
            'id': f'chart_{p.id}',
            'labels': labels,
            'datasets': datasets,
            'title': p.get_full_name(),
        })
    return charts


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


def timeline(pl):
    items = []
    s = 500
    for p in pl:
        if len(pl)<100 or (s%20 == 0 and s>0 and p.namefirst):
            items.append({
                "id": p.id,
                "content": p.get_full_name(),
                "start": f"{p.debut}",
                "end": f"{p.finalgame}",
            })
        s -= 1

    return json.dumps(items)


def show_players(request):
    pl = People.objects.all().filter(namefirst__isnull=False, namelast__isnull=False).order_by("namefirst")
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
            stat.append((p.get_full_name(), p.get_data_for_radio()))
        print(stat)
    return render(request, template_name="players/players.html", context={"players_list": pl, "player_stat": stat, "items": timeline(pl)})


def radar_charts_view(request):
    if request.method == 'POST':
        print(request.POST)
        pid = request.POST.getlist('pid')
        pid = list(map(lambda x: int(x), list(pid)))
        num_players = len(pid)
        if num_players == 0:
            return show_players(request)
        player_stats = dict()
        pl = []
        for i in pid:
            p = get_object_or_404(People, pk=i)
            pl.append(p)
            player_stats[p.get_full_name()] = p.get_data_for_radio()

        print(player_stats)
        labels = ["Hmotnost", "Výška", "Úspěšných odpalů", "Houmranů", "ERA", "SO"]
        maxes = list()
        for i in range(len(labels)):
            maxes.append(max([player_stats[k][i] for k in player_stats.keys()]))

        for i in range(len(labels)):
            for k in player_stats.keys():
                player_stats[k][i] = 100 * player_stats[k][i] / maxes[i]

        colors = generate_color_palette(num_players)
        datasets = []
        for idx, (player, stats) in enumerate(player_stats.items()):
            color = colors[idx]
            datasets.append({
                "label": player,
                "data": stats,
                "borderColor": color,
                "backgroundColor": color + "33",
                "fill": True
            })

        context = {
            "labels": json.dumps(labels),
            "datasets": json.dumps(datasets),
            "items": timeline(pl),
            "charts": line_chart_data(pl)
        }
        return render(request, 'players/radars.html', context)
    else:
        return render(request, 'players/players.html')


def index_view(request):
    return render(request, 'players/index.html')