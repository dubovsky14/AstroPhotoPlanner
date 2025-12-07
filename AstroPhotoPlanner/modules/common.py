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

def get_montly_summaries_of_observation_times(dates_and_observation_times : list[tuple[datetime.date, datetime.timedelta]], minimal_observation_time : datetime.timedelta) -> list[dict]:
    """
    Get list of tuples [month,total_observation_time] in a given year.
    """
    monthly_summaries = {
        month: {
            'month_name': MONTH_NAMES[month],
            'dates_and_times': [],
            'suitable_days_count': 0,
            'total_days_count': 0,
            'on_hover_text': '\n',
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
        summary['color'] = "red" if summary['suitable_days_count'] == 0 else "green" if summary['suitable_days_count'] == summary['total_days_count'] else "orange"

    result = [monthly_summaries[month] for month in range(1, 13)]
    return result