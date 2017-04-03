from django.shortcuts import render
from django.contrib import messages
import requests
import math

### Webpages

# Render the main page
def index(request):
    return render(request, 'Restaurants/basic.html')

# Wait on the user's request
def search(request):
    if request.method == 'POST':
        #Grab the html values

        cost = request.POST.get('costTextfield', None)
        dist = request.POST.get('distTextfield', None)
        popu = request.POST.get('popuTextfield', None)
        imme = request.POST.get('immeTextfield', None)
        resultNum = request.POST.get('resuTextfield', None)
        typeS = request.POST.get('typeSelect', None)

        print(typeS)

        #Interpreting in the preferences
        data = [cost, dist, popu, imme]
        for x in range(0, len(data)):
            data[x] = make_num(data[x])
            if (str(data[x]) == "nan"): # Bind non-numerical outputs to 0
                data[x] = 0
                if (x == 0):
                    messages.add_message(request, messages.INFO, 'Price')
                elif (x == 1):
                    messages.add_message(request, messages.INFO, 'Distance')
                elif (x == 2):
                    messages.add_message(request, messages.INFO, 'Popularity')
                elif (x == 3):
                    messages.add_message(request, messages.INFO, 'Acclaim')
            elif (abs(data[x]) > 10):  # Bind overlarge inputs to their max value
                data[x] = data[x] / abs(data[x]) * 10

        #Establish a dictionary to house the GET parameters for the API request
        params = {}

        #Locate the user
        lat = request.POST.get('latiTextfield', None)
        long = request.POST.get('longTextfield', None)

        error = 0
        if ((lat == "Error") or (long == "Error")):
            #LET THE USER KNOW THAT THEY NEED TO TURN ON LOCATION SERVICES TO GET RELEVANT RESULTS
            #The request needs something to go on... Give them an optional location input field? Or just give them random results?
            error = 1
        else:
            params["latitude"] = float(lat)
            params["longitude"] = float(long)

        #Cut down search space if the user wants someplace nearby
        rad = 40000 - data[1] * 2000
        if (rad > 40000):
            rad = 40000
        params["radius"] = int(rad)

        #If user specified what they wanted, deal accordingly
        if typeS is not None:
            if (int(typeS) == 1):
                params["categories"] = "restaurants"
            elif (int(typeS) == 2):
                params["categories"] = "active"
            elif (int(typeS) == 3):
                params["categories"] = "arts"
            elif (int(typeS) == 4):
                params["categories"] = "nightlife"

        #Cut down search space if the user really wants to go to the place
        if (data[3] > 8):
             params["open_now"] = 1

        #Don't make bad recommendations, except the user might want some, so don't actually
        #params["sort_by"] = "rating"

        #Expand the search space as much as possible
        params["limit"] = "50"

        #Fetch a solution space
        headers = {
            "Authorization": "Bearer GDiZCRPhWsvt4Tm9iutxJo7dJPFbh7OKV1PwbI5j_8CdmETqvQWHIZ8nTRBYvSpnfXzNAShki4EwUwdmB28NW1psM4Bc2NCo_eBh8ccGaa-nevbE5vS91AK3LETMWHYx"
        }

        if (error == 0):
            r = requests.get('https://api.yelp.com/v3/businesses/search',
                         headers=headers, params=params)
            result = r.json()

            #Determine how many results max the user actually wants
            resultNum = make_num(resultNum)
            if (str(resultNum) == "nan"):
                resultNum = 3
                messages.add_message(request, messages.INFO, 'Number of Results')
            elif (resultNum > 50):
                resultNum = 50
            elif (resultNum < 0):
                resultNum = 0
            else:
                resultNum = abs(int(resultNum)) #Absolute value is redundant, but kept just in case

            # Optimize within the visible solution space given user preferences
            if (result['total'] < 50):
                searchSize = result['total']
            else:
                searchSize = 50

            if searchSize != 0:
                sortList = []
                reviewMax = 0
                rateMax = 0
                distMax = 0
                priceMax = 0

                #Determining the max value for each parameter to create a relative scale
                for i in range(0, searchSize):
                    try:
                        if (result['businesses'][i]['review_count'] > reviewMax):
                            reviewMax = result['businesses'][i]['review_count']
                    except:
                        garbage = 1

                    try:
                        if (result['businesses'][i]['rating'] > rateMax):
                            rateMax = result['businesses'][i]['rating']
                    except:
                        garbage = 1

                    try:
                        if (measure(float(lat), float(long), result['businesses'][i]['coordinates']['latitude'],
                    result['businesses'][i]['coordinates']['longitude']) > distMax):
                            distMax = measure(float(lat), float(long), result['businesses'][i]['coordinates']['latitude'],
                    result['businesses'][i]['coordinates']['longitude'])
                    except:
                        garbage = 1

                    try:
                        if (len(result['businesses'][i]['price']) > priceMax):
                            priceMax = len(result['businesses'][i]['price'])
                    except:
                        garbage = 1

                for i in range(0, searchSize):
                    #Maintaining business indexes for easy sorting later
                    score = 0
                    try: #Minimize price (want the lowest score, so by default add a lot to scores of people who want low prices)
                        score -= data[0] * len(result['businesses'][i]['price']) / priceMax
                    except: #If no price listed, do nothing
                        garbage = 1


                    try: #Minimize distance
                        score -= data[1] * measure(float(lat), float(long), result['businesses'][i]['coordinates']['latitude'],
                            result['businesses'][i]['coordinates']['longitude']) / distMax
                        dist = round(measure(float(lat), float(long), result['businesses'][i]['coordinates']['latitude'],
                            result['businesses'][i]['coordinates']['longitude']) * 0.621371, 2) #Give a rough distance estimate
                    except:
                        garbage = 1

                    try: #Maximize rating
                        score -= data[2] * result['businesses'][i]['rating'] / rateMax
                    except:
                        garbage = 1

                    try: #Maximize the number of reviews
                        score -= data[3] * result['businesses'][i]['review_count'] / reviewMax
                    except:
                        garbage = 1

                    sortList.append([i, score, dist])

                sortList.sort(key=lambda y: y[1])  # Determine the optimal choices given user inputs
                if (searchSize < resultNum): #If the search space is smaller than requested, return all of them
                    resultNum = searchSize

                #Grab as many results as the user requested
                fetchList = sortList[0:resultNum]

                chosenList = []
                #Grabbing the optimal choices
                for z in range(0,len(fetchList)):
                    chosenList.append(result['businesses'][fetchList[z][0]])
                    chosenList[z]['NUMBER'] = str(z + 1) + "/" + str(len(fetchList))
                    chosenList[z]['DIST'] = fetchList[z][2]

            else:
                error = 2


        if (error == 0): #If there aren't any errors, give them the results
            return render(request, 'Restaurants/search.html', {'contents': chosenList, 'coords': [str(lat), str(long)]})
        elif (error == 1): #Theoretically this should never be called as without allowing location data, the form shouldn't send.
            return render(request, 'Restaurants/search_fail.html', {'contents': "Uh oh, it looks like we can't locate you. Urban Connoisseur needs to access your location information to give you relevant results."})
        else:
            return render(request, 'Restaurants/search_fail.html', {
                'contents': "Uh oh, it looks like Urban Connoisseur couldn't find any results for you. Sorry about that."})
    else:
        return render(request, 'Restaurants/basic.html')

### Utility functions

#Return the float of an input, or nan if the input cannot be cast as a float (as NaN casts as a float to nan...)
def make_num(s):
    try:
        float(s)
        return float(s)
    except:
        return "nan"

#Approximate the number of meters between two lat/long coords (implemented in case a result with coordinates but no distance is returned)
def measure(lat1, lon1, lat2, lon2): #Haversine implementation
    R = 6378.137 # Radius of earth in KM
    dLat = lat2 * math.pi / 180 - lat1 * math.pi / 180
    dLon = lon2 * math.pi / 180 - lon1 * math.pi / 180
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(lat1 * math.pi / 180) * math.cos(lat2 * math.pi / 180) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return d # kilometers
