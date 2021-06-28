import time
import pandas as pd
import numpy as np
import calendar as cal #this need to be added as there will be a part where we have to display the name of the month in the script

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Setting up for the variables of months and days for the filters first
    As users might input other months which are not available in the bikeshare data

    """

    months = ['january', 'february', 'march', 'april', 'may', 'june']
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Please enter one of the following options: chicago, new york city, washington:\n ").lower()
        if city not in CITY_DATA:
            print("Please ensure the correct input of City...")
        else:
            break
    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Please enter one month which is the first six months of the year. Type 'all' to include the first 6 months:\n ").lower()
        if month != 'all' and month not in months:
            print("Please ensure correct input of month...")

        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Please enter any day of the week. Please type 'all' if want to apply all days:\n ").lower()
        if day != 'all' and day not in days:
            print("Please ensure correct input of day...")
        else:
            break

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
    df = pd.read_csv(CITY_DATA[city])

    # Converting Start Time Column to Datetime:
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extracting month and day in Start Time and create a new column
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name() #tried weekday_name but seems like it didn't run correctly, and searched it should be day_name instead for this pandas version

    #filtering the month if applicable
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        #filter by month to create the new DataFrame
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]



    return df



def display_raw(df):
    """
    Loads raw data when user requests.
    """
    i = 0
    ans = input("Would you like to see raw data sample? Yes or No:\n ").lower()
    pd.set_option('display.max_columns', 200)

    while True:
        if ans == 'yes':
            print(df[i:i+5])
            ans = input("Would you like to see the next 5 rows of raw data? Yes or No:\n ").lower()
            if ans == 'yes':
                i += 5
            if ans == 'no':
                break
        if ans == 'no':
            break



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_popular_month = df['month'].mode()[0] #most counted month
    print("The most frequent month is: ", cal.month_name[most_popular_month]) #converting into calendar month name

    # display the most common day of week
    most_popular_day = df['day_of_week'].mode()[0] #most counted day of week
    print("The most frequent day is: ", most_popular_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour #we have not extracted hour from the dataframe yet
    most_popular_hour = df['hour'].mode()[0] #most counted hour
    print("The most frequent hour of the day is: ", most_popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print("The most frequent station to start is: ", common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print("The most frequent station to end is: ", common_end_station)

    # display most frequent combination of start station and end station trip
    common_start_end_station = (df['Start Station'] + ' to ' + df['End Station']).mode()[0] #this counts the values in 2 category simultaneously (adding the 'to' makes it nicer)
    print("The most frequent combination of start-to-end station is: ", common_start_end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum() #this calculates the sum of 'Trip Duration'
    print("The total time of travel is: ", total_travel_time, "seconds")

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean() #this calculates the average of traveling time in 'Trip Duration'
    print("The average time of travel is: ", round(mean_travel_time), "seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types

    user_type_count = df['User Type'].value_counts() #this counts the number of each unique value in 'User Type'
    print("The counts of user type:\n " ,user_type_count)


    # Display counts of gender
    if 'Gender' in df: #as noticed, Washington is missing the Gender category

        gender_count = df['Gender'].value_counts() #this counts the number of each unique value (Female and male) in 'User Type'
        print("Gender count as follows:\n ", gender_count)

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df: #as noticed, New York City is missing the Birth category in the data, if Birth exists, then will do the following calculation

        earliest_year = int(df['Birth Year'].min()) #min calculates the earliest year
        print("The earliest year of birth is: ", earliest_year)

        latest_year = int(df['Birth Year'].max()) #max calculates the oldest year
        print("The most recent year of birth is: ", latest_year)

        common_year = int(df['Birth Year'].mode()[0]) #mode counts the most repeated year
        print("The most commonst birth month is: ", common_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_raw(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n ')
        if restart.lower() != 'yes':
            print("\nAlrighty then! See you next time!\n")
            break



if __name__ == "__main__":
	main()
