from pathlib import Path

clock_icon = "⏲"

duration_labels = {
    clock_icon + "15m": 15,
    clock_icon + "30m": 30,
    clock_icon + "1h": 60,
    clock_icon + "2h": 120,
    clock_icon + "3h": 180,
    clock_icon + "4h": 240,
    clock_icon + "5h": 300,
    clock_icon + "6h": 360,
    clock_icon + "7h": 420,
    clock_icon + "8h": 480
}

db_path = Path.home().joinpath("users.json")
