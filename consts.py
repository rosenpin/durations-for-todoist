class TaskFields:
    ID = "id"
    Title = "content"
    Item = "item"
    Labels = "labels"
    ProjectID = "project_id"


class ProjectFields:
    Project = "project"
    Name = "name"


class LabelFields:
    Label = "label"
    Name = "name"


clock_icon = "⏲"

duration_labels = {
    clock_icon + "15m": 15,
    clock_icon + "30m": 30,
    clock_icon + "1h": 60,
    clock_icon + "2h": 120,
    clock_icon + "3h": 180,
    clock_icon + "4h": 240
}

# duration_labels = {
#    "🕑 15m": 15,
#    "🕓 30m": 30,
#    "🕕 1h": 60,
#    "🕗 2h": 120,
#    "🕙 3h": 180,
#    "🕛 4h": 240
# }
