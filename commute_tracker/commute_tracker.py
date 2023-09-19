import googlemaps
import csv

if __name__ == '__main__':
    # print("imported successfully\n")
    with open('./commute_tracker/google_api_key_maci.txt') as api_key_file:
        api_key = api_key_file.read()

    gmaps = googlemaps.Client(key=api_key)

    start_loc = [
        '2947 Ottumwa Dr, Sacramento, CA 95835',
        '1311 Bluegrass Pl, Woodland, CA 95776',
        '116 N 16th St, Sacramento, CA 95814'
    ]

    end_loc = [
        '2947 Ottumwa Dr, Sacramento, CA 95835',
        '1311 Bluegrass Pl, Woodland, CA 95776',
        '116 N 16th St, Sacramento, CA 95814'
    ]

    dist_mat = gmaps.distance_matrix(end_loc, start_loc)

    columns = ['destination','time','duration(text)','duration(value)']

    print(dist_mat)