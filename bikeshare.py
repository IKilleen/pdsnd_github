import time
import pandas as pd 

CITY_DATA = { 'chicago': 'chicago.csv',
              'nyc': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['jan', 
          'feb', 
          'mar',
          'apr',
          'may', 
          'jun']

DAYS = {'mon': 'Monday',
        'tue': 'Tuesday', 
        'wed': 'Wednesday',
        'thu': 'Thursday', 
        'fri': 'Saturday',
        'sun': 'Sunday'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    city = ""
    time_filter = ""
    month = "all"
    day = "all"
     
    # ask for city
    while city not in CITY_DATA: 
        city = input('\nFrom what city would you like statistics: Chicago, Washington or NYC?\n')
        city = city.lower()
    
    # see if filter is needed
    while time_filter  not in ['month', 'day', 'both', 'none']:
        time_filter = input('\nWould you like to filter the data by month, day, both, or none?\n')
        time_filter = time_filter.lower()

    # if we filter, ask more questions
    if time_filter == 'month' or time_filter == 'both':
        while month not in MONTHS: 
            month = input('\nWhich month (Jan, Feb, Mar, Apr, May, Jun)?\n')
            month = month.lower()
    if time_filter == 'day' or time_filter == 'both': 
        while day not in DAYS: 
            day = input('\nWhat day (Mon, Tue, Wed, Thu, Fri, Sat, Sun)?\n').lower()          
               
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
        (pd.DataFrame) df - containing city data filtered by month and day
    """

    # read in data for city
    df =  pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter 
    if month != 'all':
        month = MONTHS.index(month) + 1 
        df = df[df['month'] == month]
    if day != 'all':
        df = df[df['day_of_week'] == DAYS[day]]
    
    # add missing columns
    if city == 'washington': 
        df['Gender'] = 'Unknown'
        df['Birth Year'] = 0
    
    df['Birth Year'] = df['Birth Year'].fillna(0)
    df['Gender'] = df['Gender'].fillna('Unknown')

    return df
    

def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.
    
    Args:
        (pd.DataFrame) df - containing city data 
    """
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    popular_month = df['month'].mode()[0]
    print('Most Popular Month:', popular_month)

    popular_day = df['day_of_week'].mode()[0]
    print('Most Popular Day:', popular_day)

    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.

    Args:
        (pd.DataFrame) df - city data 
    """
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    popular_start_station = df['Start Station'].mode()[0]
    print('Most Popular Start Station:', popular_start_station)

    popular_end_station= df['End Station'].mode()[0]
    print('Most Popular End Station:', popular_end_station)

    df['Route'] = df['Start Station'] + " - " + df['End Station']
    popular_route = df['Route'].mode()[0]
    print('\nMost Popular Trip Combo:\n', popular_route)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.
    
    Args:
        (pd.DataFrame) df - city data 
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_time = df['Trip Duration'].sum()
    average_total_time = df['Trip Duration'].mean()
    
    print("Total Time: %dhrs %dmin %dsec" % format_time(total_time))
    print("Average Time: %dhrs %dmin %dsec" % format_time(average_total_time))
            
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def format_time(secs):
    """
    Calculates hours, minutes, seconds 

    Args: 
       (int) secs - number of seconds
          
    Returns: 
        (int) hours - number of hours
        (int) minutes - number of minutes
        (int) seconds - number of remaining seconds
    """
    hours = secs/3600
    minutes = (secs % 3600) / 60
    seconds = secs % 60
    return hours, minutes, seconds


def user_stats(df):
    """
    Displays statistics on bikeshare users.
    
    Args: 
        (pd.DataFrame) df - city data 
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = df['User Type'].value_counts()
    print(user_types)

    gender = df['Gender'].value_counts()
    print(gender)

    max_dob = df['Birth Year'].max()
    print(max_dob)

    min_dob = df['Birth Year'].min()
    print(min_dob)

    popular_dob = df['Birth Year'].mode()[0]
    print(popular_dob)
 
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """
    Asks user if they want to see user details.

    Args: 
       (pd.DataFrame) df - city data  
    """
    for i, r in df.iterrows(): 
        # ask question every 5th time
        if i % 5 == 0: 
            response = ''
            while response not in ['yes', 'no']:
                response = input('\nWould you like to see detailed user data?')
            if response == 'no':
                break 
        print()
        print("Birth Year: %d" % r["Birth Year"])
        print("Gender: %s" % r["Gender"])
        print("Start Station: %s" % r["Start Station"])
        print("Trip Duration in Seconds: %d" % r["Trip Duration"])
        print("User Type: %s" % r["User Type"])
        
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input("\nWould you like to restart? Enter 'yes' or 'no'.\n")
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
