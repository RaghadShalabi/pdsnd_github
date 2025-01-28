# By Eng. Raghad Shalabi 

import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # Get city input
    while True:
        city = input("Which city would you like to analyze? Chicago, New York City, or Washington: ").lower()
        if city in CITY_DATA:
            break
        else:
            print("Invalid input. Please choose from Chicago, New York City, or Washington.")

    # Get month input
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    while True:
        month = input("Which month? (all, january, february, ... , june): ").lower()
        if month in months:
            break
        else:
            print("Invalid input. Please choose from 'all', 'january', 'february', ..., 'june'.")

    # Get day input
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        day = input("Which day? (all, monday, tuesday, ... sunday): ").lower()
        if day in days:
            break
        else:
            print("Invalid input. Please choose from 'all', 'monday', 'tuesday', ..., 'sunday'.")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Load data for the specified city
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Filter by month if applicable
    if month != 'all':
        month_index = ['january', 'february', 'march', 'april', 'may', 'june'].index(month) + 1
        df = df[df['Start Time'].dt.month == month_index]

    # Filter by day if applicable
    if day != 'all':
        df = df[df['Start Time'].dt.day_name().str.lower() == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Most common month
    most_common_month = df['Start Time'].dt.month.mode()[0]
    print(f"Most common month: {most_common_month}")

    # Most common day of week
    most_common_day = df['Start Time'].dt.day_name().mode()[0]
    print(f"Most common day: {most_common_day}")

    # Most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print(f"Most common start hour: {most_common_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Most common start station
    most_common_start_station = df['Start Station'].mode()[0]
    print(f"Most commonly used start station: {most_common_start_station}")

    # Most common end station
    most_common_end_station = df['End Station'].mode()[0]
    print(f"Most commonly used end station: {most_common_end_station}")

    # Most frequent combination of start and end station
    most_common_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print(f"Most frequent combination of start and end station: {most_common_trip}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f"Total travel time: {total_travel_time} seconds")

    # Average travel time
    average_travel_time = df['Trip Duration'].mean()
    print(f"Average travel time: {average_travel_time} seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Counts of user types
    user_types = df['User Type'].value_counts()
    print(f"Counts of user types: \n{user_types}")

    # Counts of gender (if available)
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print(f"Counts of gender: \n{gender_counts}")
    else:
        print("Gender data not available.")

    # Earliest, most recent, and most common year of birth (if available)
    if 'Birth Year' in df.columns:
        earliest_birth = int(df['Birth Year'].min())
        most_recent_birth = int(df['Birth Year'].max())
        most_common_birth = int(df['Birth Year'].mode()[0])
        print(f"Earliest year of birth: {earliest_birth}")
        print(f"Most recent year of birth: {most_recent_birth}")
        print(f"Most common year of birth: {most_common_birth}")
    else:
        print("Birth Year data not available.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


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