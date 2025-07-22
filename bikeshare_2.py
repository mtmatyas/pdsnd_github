import time
import pandas as pd
import calendar as ca

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }



def get_filters():
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
        city = input("Please enter the name of the city you wish to analyze: ").lower()
        
        if city in (CITY_DATA.keys()):
            break
        else:
            print('I\'m sorry, that was an invalid entry. Please enter: chicago, new york city, or washington')

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("If you wish to filter by month please enter the month, otherwise enter all: ").lower()
        valid_month = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

        if month in (valid_month):
            break
        else:
            print('I\'m sorry, that was an invalid entry. Please enter either one of the following: ')
            print(', '.join(valid_month))
                  

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("If you wish to filter by day, please enter the day. Otherwise enter all: ").title()
        valid_day = ['All', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        if day in (valid_day):
            break
        else:
            print('I\'m sorry, that was an invalid entry. Please enter either one of the following: ')
            print(', '.join(valid_day)) 

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
    # load csv into a dataframe
    file_path = r"C:\Users\EFCDTM4\Udacity Python Project\all-project-files"
    file = (CITY_DATA[city])
    df = pd.read_csv(f'{file_path}\{file}')

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of the week to create new columns
    df['Month'] = df['Start Time'].dt.month
    df['Day of week'] = df['Start Time'].dt.day_name()

    # filter by month
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) +1
        df = df[df['Month'] == month]

    # filter by day
    if day != 'All':
        df = df[df['Day of week'] == day]

    return df

def raw_data(df):
    # function that allows the user to see the raw data (inclusive of filters) that they requested
    # Creating exit loop variable because when user would input no to seeing additional data the outer loop would re-prompt for input
    exit_loop = False

    while not exit_loop:
        view_data = input('Would you like to see 5 examples of individual trip data? Please enter yes or no: ').lower()
        if view_data == 'yes':
            i = 0
            while True:
                print(df.iloc[i:i+5])
                i += 5
                additional_data = input('Would you like to see an additional 5 examples of individual trip data? Please enter yes or no: ').lower()
                if additional_data == 'no':
                    exit_loop = True
                    break
        elif view_data in ('no'):
            break
        else:
            print('I\'m sorry that was an invalid response, please try again!')



def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # display the most common month
    if month == 'all':
        common_month = df['Month'].mode()[0]
        common_month = ca.month_name[common_month]

        print(f'The most common month of travel is: ', common_month)
    else:
        pass

    # display the most common day of week
    if day == 'All':
        df['Day of week'] = df['Start Time'].dt.day_name()
        common_day_of_week = df['Day of week'].mode()[0]
        print('The most common day of the week to travel is: ', common_day_of_week)
    else:
        pass 
    

    ## display the most common start hour
    df['hour'] = df['Start Time'].dt.strftime('%I %p')
    popular_hour = df['hour'].mode()[0]

    print('The most popular start hour is: ', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    count_start = df['Start Station'].value_counts()
    start_station = count_start.idxmax()
    max_start = count_start.max()
    print('The most commonly used start station is:', start_station, 'with a total of', max_start, 'trips started at this location')

    # display most commonly used end station
    count_end = df['End Station'].value_counts()
    end_station = count_end.idxmax()
    max_end = count_end.max()
    print('The most commonly used end station is:', end_station, 'with a total of', max_end, 'trips ending at this location')

    # display most frequent combination of start station and end station trip
    # creating a new column that combines the start & end station to idenfity the most frequent route
    df['Route'] = df['Start Station'] + ' to ' + df['End Station']
    count_route = df['Route'].value_counts()
    route = count_route.idxmax()
    max_route = count_route.max()
    print('The most frequent taken route is:', route, 'with a total of', max_route, 'trips taken')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()


    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    # Trip Duration column values is in seconds, calculating to convert seconds to hours & remaining minutes
    total_hours = total_travel_time // 3600
    total_minutes = (total_travel_time % 3600) // 60
    if total_minutes == 60:
        total_hours +=1
        total_minutes = 0
    print(f"The total time traveled is: {total_hours} hours and {total_minutes} minutes")

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    # Trip Duration column values is in seconds, calculating to convert seconds to minutes & remaining seconds
    mean_minutes = round(mean_travel_time // 60)
    mean_seconds = round(mean_travel_time % 60)
    if mean_seconds == 60:
        mean_minutes += 1
        mean_seconds = 0 

    print(f"The mean travel timed is: {mean_minutes} minutes and {mean_seconds} seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_type= df['User Type'].value_counts()
    for User_Type, count in count_type.items():
        print(f"{User_Type}: {count}")


    # Display counts of gender
    # Creating an if else statement because Washington data does not contain gender column
    if 'Gender' in df.columns:
        count_gender = df['Gender'].value_counts()
        for Gender, count in count_gender.items():
            print(f"{Gender}: {count}")
    else:
        print(city.title(), "does not provide gender statistics")


    # Display earliest, most recent, and most common year of birth
    # Creating an if else statement because Washington does not provide birth year column
    if 'Birth Year' in df.columns:
        earliest_year = df['Birth Year'].min()
        earliest_year = int(earliest_year)
        print(f'The earliest year of birth for a bikeshare user during this time was: {earliest_year}')

        recent_year = df['Birth Year'].max()
        recent_year = int(recent_year)
        print(f'The most recent year of birth for a bikeshare user during this time was: {recent_year}')

        common_year = df['Birth Year'].mode()[0]
        common_year = int(common_year)
        print(f'The most common year of birth for a bikeshare user during this time was: {common_year}')
    else:
        print(city.title(), "does not provide year of birth statistics")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


    


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        raw_data(df)
        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print('Thank you for using the program!')
            break


if __name__ == "__main__":
	main()
