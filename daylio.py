import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from matplotlib.ticker import (MultipleLocator, NullFormatter)
import sys

daylio_csv = sys.argv[1]
data = pd.read_csv(daylio_csv)
mood_mapping = {'awful': 0.5, 'bad': 1.5, 'meh': 2.5, 'good': 3.5, 'rad': 4.5}
mood_colors = {'awful': 'red', 'bad': 'orange', 'meh': 'deepskyblue', 'good': 'lime', 'rad': 'turquoise'}
mood_boundaries = [1, 2, 3, 4]

data['mood_value'] = data['mood'].map(mood_mapping)
data['full_date'] = pd.to_datetime(data['full_date'])
data_sorted = data.sort_values(by='full_date')

MIN_PIXEL_DIST = 20
DPI = 100
DEFAULT_WINDOW_SIZE = 20
NUM_POINTS = len(data_sorted)
pixel_distance = DEFAULT_WINDOW_SIZE * DPI / (NUM_POINTS - 1)

if pixel_distance < MIN_PIXEL_DIST:
    scale_factor = MIN_PIXEL_DIST / pixel_distance
    pixel_distance = MIN_PIXEL_DIST
    window_size = DEFAULT_WINDOW_SIZE * scale_factor
else:
    window_size = DEFAULT_WINDOW_SIZE

base_height = 6
fig, ax = plt.subplots(figsize=(window_size, base_height), dpi=DPI)

#color code graph
for i in range(len(data_sorted) - 1):
    start_mood = data_sorted['mood_value'].iloc[i]
    end_mood = data_sorted['mood_value'].iloc[i + 1]
    x1, y1 = mdates.date2num(data_sorted['full_date'].iloc[i]), start_mood
    x2, y2 = mdates.date2num(data_sorted['full_date'].iloc[i + 1]), end_mood

    if y1 != y2:
        m = (y2 - y1) / (x2 - x1)
        intersection_points = [(x1, y1)]

        for boundary in mood_boundaries:
            if (y1 < boundary < y2) or (y2 < boundary < y1):
                x_intersection = x1 + (boundary - y1) / m
                intersection_points.append((x_intersection, boundary))

        intersection_points.append((x2, y2))
        intersection_points.sort(key=lambda x: x[0])

        for j in range(len(intersection_points) - 1):
            x_start, y_start = intersection_points[j]
            x_end, y_end = intersection_points[j + 1]
            mood_range = (int(min(y_start, y_end)), int(max(y_start, y_end)))
            color = mood_colors[list(mood_mapping.keys())[mood_range[0]]]
            ax.plot([mdates.num2date(x_start), mdates.num2date(x_end)], [y_start, y_end], linestyle='-', color=color, linewidth=2)
    else:
        color = mood_colors[data_sorted['mood'].iloc[i]]
        ax.plot([data_sorted['full_date'].iloc[i], data_sorted['full_date'].iloc[i + 1]], [y1, y2], linestyle='-', color=color, linewidth=2)

#color points
for mood, color in mood_colors.items():
    mask = data_sorted['mood'] == mood
    ax.plot(data_sorted.loc[mask, 'full_date'], data_sorted.loc[mask, 'mood_value'], marker='o', linestyle='None', color=color)

ax.set_title(f'Average mood of {round(data["mood_value"].mean(),2) + 0.5} over {len(data)} days', fontsize=16)
ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('Mood', fontsize=12, labelpad=25)

ax.grid(axis='y', linestyle='--')

ax.yaxis.set_major_locator(MultipleLocator(1))
ax.yaxis.set_minor_locator(MultipleLocator(0.5))
major_ticks = np.arange(0, 6, 1)
ax.set_yticks(major_ticks)
ax.yaxis.set_major_formatter(NullFormatter())
minor_ticks = np.arange(0.5, 5.5, 1)
ax.set_yticks(minor_ticks, minor=True)
ax.tick_params(axis='y', which='both', length=0)

for mood, value in mood_mapping.items():
    ax.text(0, value, mood.capitalize() + ' ', transform=ax.get_yaxis_transform(), ha='right', va='center', color=mood_colors[mood])

ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

min_date = data_sorted['full_date'].min()
max_date = data_sorted['full_date'].max()
graph_padding = 25 
date_range = max_date - min_date
pixel_width = fig.get_figwidth() * DPI
date_padding = date_range * (graph_padding / pixel_width)
ax.set_xlim(min_date - date_padding, max_date + date_padding)

fig.autofmt_xdate()

plt.subplots_adjust(bottom=0.15, top=0.9)
plt.tight_layout()

plt.savefig('graph.jpg', dpi=DPI, format='jpg')
# plt.show() # Uncomment to display the graph