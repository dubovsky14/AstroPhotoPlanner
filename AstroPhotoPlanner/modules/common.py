import datetime

MONTH_NAMES = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December",
}

def get_montly_summaries_of_observation_times(dates_and_observation_times : list[tuple[datetime.date, datetime.timedelta]], minimal_observation_time : datetime.timedelta, working_with_peak_times : bool = False) -> list[dict]:
    """
    Get list of tuples [month,total_observation_time] in a given year.

    Each month contains:
    - month_name
    - dates_and_times: list of tuples (date, observation_time)
    - suitable_days_count
    - total_days_count
    - on_hover_text
    - color: "red" (no suitable days), "green" (all days suitable), "orange" (some days suitable) "blue" (location not suitable - won't get high enough, but sufficient peak time during night)
    """
    monthly_summaries = {
        month: {
            'month_name': MONTH_NAMES[month],
            'dates_and_times': [],
            'suitable_days_count': 0,
            'total_days_count': 0,
            'on_hover_text': '\n' if not working_with_peak_times else '\nBut it never gets high enough from the selected location. These are just peak times during the astronomical night:\n',
        }
        for month in range(1, 13)
    }

    for date, observation_time in dates_and_observation_times:
        month = date.month
        monthly_summaries[month]['dates_and_times'].append((date, observation_time))
        monthly_summaries[month]['total_days_count'] += 1
        if observation_time >= minimal_observation_time:
            monthly_summaries[month]['suitable_days_count'] += 1
        monthly_summaries[month]['on_hover_text'] += f"{date}: {observation_time.seconds // 3600}h {observation_time.seconds // 60 % 60}m {observation_time.seconds % 60}s\n"

    for month, summary in monthly_summaries.items():
        summary['dates_and_times'].sort(key=lambda x: x[0])  # Sort by date
        if working_with_peak_times:
            summary['color'] = "red" if summary['suitable_days_count'] == 0 else "blue" if summary['suitable_days_count'] == summary['total_days_count'] else "purple"
        else:
            summary['color'] = "red" if summary['suitable_days_count'] == 0 else "green" if summary['suitable_days_count'] == summary['total_days_count'] else "orange"

    result = [monthly_summaries[month] for month in range(1, 13)]
    return result

def convert_angle_to_float(angle_str: str) -> float:
    """
    Convert angle in format "DD°MM'SS" to float degrees.
    """
    angle_str = angle_str.replace("°", "h").replace("deg", "h").replace("d", "h")
    angle_str = angle_str.replace("m", "'").replace("s", '"')
    parts = angle_str.split("h")
    degrees = float(parts[0])
    negative = degrees < 0
    degrees = abs(degrees)
    if len(parts) > 1 and parts[1]:
        minutes_parts = parts[1].split("'")
        minutes = float(minutes_parts[0])
        degrees += minutes / 60
        if len(minutes_parts) > 1 and minutes_parts[1]:
            seconds_parts = minutes_parts[1].split('"')
            seconds = float(seconds_parts[0])
            degrees += seconds / 3600
    if negative:
        degrees = -degrees
    degrees = round(degrees, 4)
    return degrees