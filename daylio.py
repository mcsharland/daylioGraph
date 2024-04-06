import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import sys

daylio_csv = sys.argv[1]
data = pd.read_csv(daylio_csv)

mood_mapping = {'awful': 1, 'bad': 2, 'meh': 3, 'good': 4, 'rad': 5}
mood_colors = {'awful': 'red', 'bad': 'orange', 'meh': 'deepskyblue', 'good': 'lime', 'rad': 'turquoise'}

data['mood_value'] = data['mood'].map(mood_mapping)
data['full_date'] = pd.to_datetime(data['full_date'])
data_sorted = data.sort_values(by='full_date')

MIN_PIXEL_DIST = 20

dpi = 100

default_window_size = 20

num_points = len(data_sorted)

pixel_distance = default_window_size * dpi / (num_points - 1)

if pixel_distance < MIN_PIXEL_DIST:
    scale_factor = MIN_PIXEL_DIST / pixel_distance
    pixel_distance = MIN_PIXEL_DIST
    window_size = default_window_size * scale_factor
else:
    window_size = default_window_size

base_height = 6

plt.figure(figsize=(window_size, base_height), dpi=dpi)

for i in range(len(data_sorted) - 1):
    start_mood = data_sorted['mood'].iloc[i]
    end_mood = data_sorted['mood'].iloc[i + 1]
    color = mood_colors[start_mood]
    plt.plot(data_sorted['full_date'].iloc[i:i+2], data_sorted['mood_value'].iloc[i:i+2], marker='o', linestyle='-', color=color, linewidth=2)

    if i == len(data_sorted) - 2:
        plt.plot(data_sorted['full_date'].iloc[-1], data_sorted['mood_value'].iloc[-1], marker='o', color=mood_colors[end_mood])

plt.title(f'Average mood of {round(data["mood_value"].mean(),2)} over {len(data)} days', fontsize=16)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Mood', fontsize=12)

labels=['Awful', 'Bad', 'Meh', 'Good', 'Rad']
label_colors = [mood_colors[mood.lower()] for mood in labels]
plt.yticks(ticks=[1, 2, 3, 4, 5], labels=labels)
for i, label in enumerate(plt.gca().get_yticklabels()):
    label.set_color(label_colors[i])

plt.grid(axis='y', linestyle='--')

plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.gcf().autofmt_xdate()
plt.tight_layout()

plt.savefig('graph.jpg', dpi=dpi, format='jpg')
# plt.show() # Uncomment to open the graph after running the program