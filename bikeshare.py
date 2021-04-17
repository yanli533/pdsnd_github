import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

month_dict={'all': 'all',
            'january': 1,
            'february': 2,
            'march': 3,
            'april': 4,
            'may': 5,
            'june': 6,
            'july': 7,
            'august': 8,
            'september': 9,
            'october': 10,
            'november': 11,
            'december': 12}

day_list=['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    validcity=True
    while validcity:
        city = input("Please select the city from chicago, new york city and washington: ")
        if city.lower() in CITY_DATA:
            validcity=False
            city = CITY_DATA[city.lower()]
        else:
            print('That is not included in this exercise \nPlease select from chicago, new york city and washington.')

    # TO DO: get user input for month (all, january, february, ... , june)
    print('Next please enter the month you interested.')

    validmonth=True
    while validmonth:
        month=input("Please enter the month you want to filter by: \n Enter all if no filter required by month.")
        if month.lower() in month_dict:
            validmonth=False
            month = month_dict[month.lower()]
        else:
            print('That is not a valid month. Please select between january and june or all for no month filter')

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    print("Now let\'s select the day!")

    validday=True
    while validday:
        day=input('Please enter the day you want to filter by: \n Enter all if no filter required by day.')
        if day.lower() in day_list:
            validday=False
        else:
            print('That is not a valid day. Please enter between monday and sunday or all for no day filter')

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
    df = pd.read_csv(city)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Day'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    
    if month != 'all':
        df = df[df['Month'] == month]
    if day.lower() != 'all':
        df = df[df['Day'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df['Month'].mode()[0]
    print('The most common month is {}'.format(common_month))

    # TO DO: display the most common day of week
    common_day = df['Day'].mode()[0]
    print('The most common day is {}'.format(common_day))

    # TO DO: display the most common start hour
    comm_start_hour = df['hour'].mode()[0]
    print('The most common start hour is {}'.format(comm_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    comm_start_station = df['Start Station'].mode()[0]
    print('The most common start station is {}'.format(comm_start_station))

    # TO DO: display most commonly used end station
    comm_end_station = df['End Station'].mode()[0]
    print('The most common end station is {}'.format(comm_end_station))

    # TO DO: display most frequent combination of start station and end station trip
    comm_combination_station = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('The most common combination of start station and end station is {}.'.format(comm_combination_station))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time is {} seconds.'.format(total_travel_time))

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Average travel time is {} seconds.'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type_dict={}
    for user in df['User Type']:
        if (user in user_type_dict) and (user is not np.nan):
            user_type_dict[user] += 1
        elif (user not in user_type_dict) and (user is not np.nan):
            user_type_dict[user] = 1
    
    for user, count in user_type_dict.items():
        print('For user type {} there {} counts.\n'.format(user, count))
       

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        print('The counts of gender of our customers are: \n')
        print(df.groupby(['Gender'])['Day'].count())
    else:
        print('There is no gender information for this city')

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth_year = df['Birth Year'].min()
        recent_birth_year = df['Birth Year'].max()
        most_comm_birth_year = df['Birth Year'].mode()
    
        print('The earliest birth year of our customers is {}.\n'.format(earliest_birth_year))
        print('The most recent birth year of our customers is {}.\n'.format(recent_birth_year))
        print('The most common birth year of our customers is {}.'.format(most_comm_birth_year))
    else:
        print('There is no birth year information for this city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """display raw data 5 rows at a time according to user request."""
    var=True
    num=0
    i = input("Do you want to see some raw data? Enter yes or no: ")
    while i=='yes':
        print(df.iloc[num:num+5])
        num += 5
        i = input("Do you want to see more data? Enter yes or no: ")
        if i =='yes':
            print(df.iloc[num:num+5])
            num +=5
            i = input("Do you want to see more data? Enter yes or no: ")
        else:
            break
    else:
        var=False

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)
        
        

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()



print('Hello! Let\'s explore some US bikeshare data!')


