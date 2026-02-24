import googlemaps
import csv
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

# USER SETTINGS
# set up locations of interest for driving duration
start_loc = [
    '2947 Ottumwa Dr, Sacramento, CA 95835',
    '301 Harter Ave, Woodland, CA 95776',
    '3808 Faraday Ave, Davis, CA 95618',
]
end_loc = [
    '2947 Ottumwa Dr, Sacramento, CA 95835',
    '301 Harter Ave, Woodland, CA 95776',
    '3808 Faraday Ave, Davis, CA 95618',
]
day_start_time = datetime.time(5)  # start commute data at 5am
day_end_time = datetime.time(20)  # end commute data at 8pm

def poll():
    now = datetime.datetime.now()
    current_date = now.strftime('%Y.%m.%d')
    current_day_of_week = now.strftime('%A')
    current_time = now.strftime('%H:%M')

    # perform distance matrix api call
    dist_mat = gmaps.distance_matrix(
        origins=start_loc, 
        destinations=end_loc, 
        mode='driving', 
        units='imperial', 
        departure_time=now)

    # write distance matrix (if origin and destination are not the same)
    with open('./commute_tracker/data.csv', 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')

        for row in range(len(start_loc)):
            for col in range(len(end_loc)):
                origin = dist_mat['origin_addresses'][row]
                destination = dist_mat['destination_addresses'][col]
                duration_in_traffic = dist_mat['rows'][row]['elements']\
                    [col]['duration_in_traffic']['text']
                if origin != destination:
                    csvwriter.writerow([
                        origin, 
                        destination, 
                        current_date, 
                        current_day_of_week, 
                        current_time, 
                        duration_in_traffic])

if __name__ == '__main__':
    # initialize googlemaps api with my personal api key string
    with open('./commute_tracker/google_api_key_maci.txt') as api_key_file:
        api_key = api_key_file.read()
    gmaps = googlemaps.Client(key=api_key)

    
    bsched = BlockingScheduler()

    # 'cron' trigger is the secret sauce here
    bsched.add_job( poll, 'cron', 
        day_of_week='mon-fri', 
        hour='5-20',         # Runs during hours 5 through 19
        minute='0,8,9,10,11,12,13,14,15,30,45'  # Every 15 minutes
    )

    try:
        print("commute tracker started. Press Ctrl+C to exit.")
        bsched.start()
    except (KeyboardInterrupt, SystemExit):
        pass
