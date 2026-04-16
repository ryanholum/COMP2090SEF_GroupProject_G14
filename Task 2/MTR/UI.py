import tkinter as tk
from tkinter import ttk
import main


root = tk.Tk()
root.title("MTR Route Finder")
root.geometry("700x500")



# Dropdown menus
start_var = tk.StringVar()
end_var = tk.StringVar()

station_names = [info["name"] for info in main.stations.values()]
name_to_id = {info["name"]: sid for sid, info in main.stations.items()}

ttk.Label(root, text="Start Station:").pack(pady=5)
ttk.Combobox(root, textvariable=start_var, values=station_names, width=40).pack()

ttk.Label(root, text="End Station:").pack(pady=5)
ttk.Combobox(root, textvariable=end_var, values=station_names, width=40).pack()



# Result Label (with boundary)
result_label = ttk.Label(
    root,
    text="",
    justify="left",
    anchor="nw",
    wraplength=500     # prevents overflow
)
result_label.pack(pady=15)



# Route Search Logic
def find_route():
    start_name = start_var.get()
    end_name = end_var.get()

    if not start_name or not end_name:
        result_label.config(text="Please select a starting point and destination")
        return

    start_id = name_to_id[start_name]
    end_id = name_to_id[end_name]

    path = main.bfs_shortest_path(start_id, end_id)

    if not path:
        result_label.config(text="No such route found")
        return

    english_path = [main.stations[s]["name"] for s in path]

    # Build output text
    output = "Station passthrough:\n" + " → ".join(english_path)

    total_time = main.calculate_total_time(path, main.edges)
    output += f"\n\nTotal Travel Time:\n{total_time} minutes"

    result_label.config(text=output)



# Search Button
ttk.Button(root, text="Search Route", command=find_route).pack(pady=10)


root.mainloop()
