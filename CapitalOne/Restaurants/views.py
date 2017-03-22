from django.shortcuts import render
import requests

### WEBPAGES
def index(request):
    #params = {"Authorization": "Bearer GDiZCRPhWsvt4Tm9iutxJo7dJPFbh7OKV1PwbI5j_8CdmETqvQWHIZ8nTRBYvSpnfXzNAShki4EwUwdmB28NW1psM4Bc2NCo_eBh8ccGaa-nevbE5vS91AK3LETMWHYx"}
    #r = requests.get('https://api.yelp.com/v3/autocomplete?text=del&latitude=37.786882&longitude=-122.399972',
    #                 params=params)
    headers = {"Authorization": "Bearer GDiZCRPhWsvt4Tm9iutxJo7dJPFbh7OKV1PwbI5j_8CdmETqvQWHIZ8nTRBYvSpnfXzNAShki4EwUwdmB28NW1psM4Bc2NCo_eBh8ccGaa-nevbE5vS91AK3LETMWHYx"}
    r = requests.get('https://api.yelp.com/v3/autocomplete?text=del&latitude=37.786882&longitude=-122.399972', headers = headers)
    result = r.json()

    return render(request, 'Restaurants/basic.html', {'contents': [result]})


def search(request):
    if request.method == 'POST':
        #Grab the html values
        cost = request.POST.get('costTextfield', None)
        dist = request.POST.get('distTextfield', None)
        popu = request.POST.get('popuTextfield', None)

        #Interpreting in the preferences
        data = [cost, dist, popu]
        for x in range(0, len(data)):
            data[x] = make_num(data[x])
            if (str(data[x]) == "nan"): # Bind non-numerical outputs to 0
                data[x] = 0
            elif (abs(data[x]) > 10):  # Bind overlarge inputs to their max value
                data[x] = data[x] / abs(data[x]) * 10

        #Locate the user
        lat = request.POST.get('latiTextfield', None)
        long = request.POST.get('longTextfield', None)
        #if ()
        print(lat, long)

        """
        #Fetch a solution space
        params = {
            "latitude": "",
            "longitude": "",
            "radius": "",

        }
        headers = {
            "Authorization": "Bearer GDiZCRPhWsvt4Tm9iutxJo7dJPFbh7OKV1PwbI5j_8CdmETqvQWHIZ8nTRBYvSpnfXzNAShki4EwUwdmB28NW1psM4Bc2NCo_eBh8ccGaa-nevbE5vS91AK3LETMWHYx"
        }
        r = requests.get('https://api.yelp.com/v3/search',
                         headers=headers, params=params)
        result = r.json()

        #Optimize within the solution space given user preferences
        """


        return render(request, 'Restaurants/search.html', {'contents': [lat, long]})
    else:
        return render(request, 'Restaurants/basic.html')

### UTILITY FUNCTIONS

#Return the float of an input, or nan if the input cannot be cast as a float (as NaN casts as a float to nan...)
def make_num(s):
    try:
        float(s)
        return float(s)
    except:
        return "nan"
