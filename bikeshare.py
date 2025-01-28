import time
import pandas as pd

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

MONTHS = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
DAYS = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """Asks user to specify a city, month, and day to analyze."""
    print('Hello! Let\'s explore some US bikeshare data!')

    city = get_input('Which city would you like to analyze? Chicago, New York City, or Washington: ', CITY_DATA.keys())
    month = get_input('Which month? (all, january, february, ... , june): ', MONTHS)
    day = get_input('Which day? (all, monday, tuesday, ... sunday): ', DAYS)

    print('-' * 40)
    return city, month, day

def get_input(prompt, valid_options):
    """Helper function to handle user input with validation."""
    while True:
        user_input = input(prompt).lower()
        if user_input in valid_options:
            return user_input
        print(f"Invalid input. Please choose from {', '.join(valid_options)}.")

def load_data(city, month, day):
    """Loads and filters the city data by month and day."""
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    if month != 'all':
        month_index = MONTHS.index(month)
        df = df[df['Start Time'].dt.month == month_index]

    if day != 'all':
        df = df[df['Start Time'].dt.day_name().str.lower() == day]

    return df

def display_stats(stats, title):
    """Helper function to display stats."""
    print(f'\n{title}\n{"-" * len(title)}')
    for key, value in stats.items():
        print(f"{key}: {value}")

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    most_common_month = df['Start Time'].dt.month.mode()[0]
    most_common_day = df['Start Time'].dt.day_name().mode()[0]
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]

    stats = {
        'Most common month': most_common_month,
        'Most common day': most_common_day,
        'Most common start hour': most_common_hour
    }

    display_stats(stats, 'Most Frequent Times of Travel')

    print(f"\nThis took {time.time() - start_time} seconds.")
    print('-' * 40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    most_common_start_station = df['Start Station'].mode()[0]
    most_common_end_station = df['End Station'].mode()[0]
    most_common_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()

    stats = {
        'Most commonly used start station': most_common_start_station,
        'Most commonly used end station': most_common_end_station,
        'Most frequent combination of start and end station': most_common_trip
    }

    display_stats(stats, 'Most Popular Stations and Trip')

    print(f"\nThis took {time.time() - start_time} seconds.")
    print('-' * 40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = df['Trip Duration'].sum()
    average_travel_time = df['Trip Duration'].mean()

    stats = {
        'Total travel time': total_travel_time,
        'Average travel time': average_travel_time
    }

    display_stats(stats, 'Trip Duration')

    print(f"\nThis took {time.time() - start_time} seconds.")
    print('-' * 40)

def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Counts of user types
    user_types = df['User Type'].value_counts()

    stats = {'Counts of user types': user_types}

    # Gender data if available
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        stats['Counts of gender'] = gender_counts
    else:
        stats['Gender data'] = 'Not available'

    # Birth year stats if available
    if 'Birth Year' in df.columns:
        earliest_birth = int(df['Birth Year'].min())
        most_recent_birth = int(df['Birth Year'].max())
        most_common_birth = int(df['Birth Year'].mode()[0])

        stats.update({
            'Earliest year of birth': earliest_birth,
            'Most recent year of birth': most_recent_birth,
            'Most common year of birth': most_common_birth
        })
    else:
        stats['Birth Year data'] = 'Not available'

    display_stats(stats, 'User Stats')

    print(f"\nThis took {time.time() - start_time} seconds.")
    print('-' * 40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()