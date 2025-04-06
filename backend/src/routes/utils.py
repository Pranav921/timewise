
season_map = {
    "0": "Fall",
    "1": "Spring",
    "2": "Summer"
}

def get_semester_str(client_semester_str):
    season = client_semester_str[0]
    year = client_semester_str[1:5]

    return season_map[season] + " " + year
