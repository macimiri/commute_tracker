import googlemaps
import csv
import datetime
from time import sleep

# USER SETTINGS
# set up locations of interest for driving duration
start_loc = [
    '2947 Ottumwa Dr, Sacramento, CA 95835',
    '301 Harter Ave, Woodland, CA 95776',
    '116 N 16th St, Sacramento, CA 95814'
]
end_loc = [
    '2947 Ottumwa Dr, Sacramento, CA 95835',
    '301 Harter Ave, Woodland, CA 95776',
    '116 N 16th St, Sacramento, CA 95814'
]
day_start_time = datetime.time(5)  # start commute data at 5am
day_end_time = datetime.time(20)  # end commute data at 8pm

if __name__ == '__main__':
    # initialize googlemaps api with my personal api key string
    with open('./commute_tracker/google_api_key_maci.txt') as api_key_file:
        api_key = api_key_file.read()
    gmaps = googlemaps.Client(key=api_key)

    # check every minute and run script on the quarter hour
    while(True):
        now = datetime.datetime.now()
        current_date = now.strftime('%Y.%m.%d')
        current_day_of_week = now.strftime('%A')
        current_time = now.strftime('%H:%M')

        if (((int(now.strftime('%M')) % 15) == 0) 
            and now.time() >= day_start_time
            and now.time() <= day_end_time):
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
                        duration_in_traffic = dist_mat['rows'][row]['elements'][col]['duration_in_traffic']['text']
                        if origin != destination:
                            csvwriter.writerow([origin, destination, current_date, current_day_of_week, current_time, duration_in_traffic])

        sleep(60)
