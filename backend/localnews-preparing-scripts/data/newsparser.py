import requests
import csv

api_key = '3ce65548db8d4955b6e6f942d42281ee'

# Base URL for NewsAPI
base_url = 'https://newsapi.org/v2/everything'

# Full list of cities for local news
cities = [
    "Anchorage", "Birmingham", "Hoover", "Huntsville", "Mobile", "Montgomery", "Tuscaloosa",
    "Fayetteville", "Fort Smith", "Jonesboro", "Little Rock", "Springdale", "Avondale", "Chandler",
    "Gilbert", "Glendale", "Mesa", "Peoria", "Phoenix", "Scottsdale", "Surprise", "Tempe", "Tucson",
    "Yuma", "Alameda", "Alhambra", "Anaheim", "Antioch", "Apple Valley", "Bakersfield", "Baldwin Park",
    "Bellflower", "Berkeley", "Buena Park", "Burbank", "Carlsbad", "Carson", "Chico", "Chino",
    "Chino Hills", "Chula Vista", "Citrus Heights", "Clovis", "Compton", "Concord", "Corona",
    "Costa Mesa", "Daly City", "Downey", "El Cajon", "El Monte", "Elk Grove", "Escondido", "Fairfield",
    "Folsom", "Fontana", "Fremont", "Fresno", "Fullerton", "Garden Grove", "Glendale", "Hawthorne",
    "Hayward", "Hemet", "Hesperia", "Huntington Beach", "Indio", "Inglewood", "Irvine", "Lake Forest",
    "Lakewood", "Lancaster", "Livermore", "Long Beach", "Los Angeles", "Lynwood", "Manteca", "Menifee",
    "Merced", "Milpitas", "Mission Viejo", "Modesto", "Moreno Valley", "Mountain View", "Murrieta",
    "Napa", "Newport Beach", "Norwalk", "Oakland", "Oceanside", "Ontario", "Orange", "Oxnard",
    "Palmdale", "Pasadena", "Perris", "Pleasanton", "Pomona", "Rancho Cucamonga", "Redding",
    "Redlands", "Redondo Beach", "Redwood City", "Rialto", "Richmond", "Riverside", "Roseville",
    "Sacramento", "Salinas", "San Bernardino", "San Buenaventura (Ventura)", "San Diego",
    "San Francisco", "San Jose", "San Leandro", "San Marcos", "San Mateo", "San Ramon", "Santa Ana",
    "Santa Barbara", "Santa Clara", "Santa Clarita", "Santa Maria", "Santa Monica", "Santa Rosa",
    "Simi Valley", "South Gate", "Stockton", "Sunnyvale", "Temecula", "Thousand Oaks", "Torrance",
    "Tracy", "Turlock", "Tustin", "Union City", "Upland", "Vacaville", "Vallejo", "Victorville",
    "Visalia", "Vista", "West Covina", "Westminster", "Whittier", "Arvada", "Aurora", "Boulder",
    "Centennial", "Colorado Springs", "Denver", "Fort Collins", "Greeley", "Lakewood", "Longmont",
    "Loveland", "Pueblo", "Thornton", "Westminster", "Bridgeport", "Danbury", "Hartford", "New Britain",
    "New Haven", "Norwalk", "Stamford", "Waterbury", "Washington", "Wilmington", "Boca Raton",
    "Boynton Beach", "Cape Coral", "Clearwater", "Coral Springs", "Davie", "Deerfield Beach",
    "Deltona", "Fort Lauderdale", "Gainesville", "Hialeah", "Hollywood", "Jacksonville", "Lakeland",
    "Largo", "Lauderhill", "Melbourne", "Miami", "Miami Beach", "Miami Gardens", "Miramar", "Orlando",
    "Palm Bay", "Palm Coast", "Pembroke Pines", "Plantation", "Pompano Beach", "Port St. Lucie",
    "St. Petersburg", "Sunrise", "Tallahassee", "Tampa", "West Palm Beach", "Albany", "Athens",
    "Atlanta", "Augusta", "Columbus", "Johns Creek", "Macon", "Roswell", "Sandy Springs", "Savannah",
    "Warner Robins", "Honolulu", "Cedar Rapids", "Davenport", "Des Moines", "Iowa City", "Sioux City",
    "Waterloo", "Boise City", "Meridian", "Nampa", "Arlington Heights", "Aurora", "Bloomington",
    "Bolingbrook", "Champaign", "Chicago", "Cicero", "Decatur", "Elgin", "Evanston", "Joliet",
    "Naperville", "Palatine", "Peoria", "Rockford", "Schaumburg", "Springfield", "Waukegan",
    "Bloomington", "Carmel", "Evansville", "Fishers", "Fort Wayne", "Gary", "Hammond", "Indianapolis",
    "Lafayette", "Muncie", "South Bend", "Kansas City", "Lawrence", "Olathe", "Overland Park", "Topeka",
    "Wichita", "Lexington", "Louisville", "Baton Rouge", "Kenner", "Lafayette", "Lake Charles",
    "New Orleans", "Shreveport", "Boston", "Brockton", "Cambridge", "Fall River", "Lawrence", "Lowell",
    "Lynn", "New Bedford", "Newton", "Quincy", "Somerville", "Springfield", "Worcester", "Baltimore",
    "Portland", "Ann Arbor", "Dearborn", "Detroit", "Farmington Hills", "Flint", "Grand Rapids",
    "Kalamazoo", "Lansing", "Livonia", "Rochester Hills", "Southfield", "Sterling Heights", "Troy",
    "Warren", "Westland", "Wyoming", "Bloomington", "Brooklyn Park", "Duluth", "Minneapolis",
    "Plymouth", "Rochester", "St. Paul", "Columbia", "Independence", "Kansas City", "Lee's Summit",
    "O'Fallon", "Springfield", "St. Joseph", "St. Louis", "Gulfport", "Jackson", "Billings", "Missoula",
    "Asheville", "Cary", "Charlotte", "Concord", "Durham", "Fayetteville", "Gastonia", "Greensboro",
    "Greenville", "High Point", "Jacksonville", "Raleigh", "Wilmington", "Winston-Salem", "Fargo",
    "Lincoln", "Omaha", "Manchester", "Nashua", "Camden", "Clifton", "Elizabeth", "Jersey City",
    "Newark", "Passaic", "Paterson", "Trenton", "Union City", "Albuquerque", "Las Cruces", "Rio Rancho",
    "Santa Fe", "Henderson", "Las Vegas", "North Las Vegas", "Reno", "Sparks", "Albany", "Buffalo",
    "Mount Vernon", "New Rochelle", "New York", "Rochester", "Schenectady", "Syracuse", "Yonkers",
    "Akron", "Canton", "Cincinnati", "Cleveland", "Columbus", "Dayton", "Parma", "Toledo",
    "Youngstown", "Broken Arrow", "Edmond", "Lawton", "Norman", "Oklahoma City", "Tulsa", "Beaverton",
    "Bend", "Eugene", "Gresham", "Hillsboro", "Medford", "Portland", "Salem", "Allentown", "Bethlehem",
    "Erie", "Philadelphia", "Pittsburgh", "Reading", "Scranton", "Cranston", "Pawtucket", "Providence",
    "Warwick", "Charleston", "Columbia", "Mount Pleasant", "North Charleston", "Rock Hill",
    "Rapid City", "Sioux Falls", "Chattanooga", "Clarksville", "Knoxville", "Memphis", "Murfreesboro",
    "Nashville", "Abilene", "Allen", "Amarillo", "Arlington", "Austin", "Baytown", "Beaumont",
    "Brownsville", "Bryan", "Carrollton", "College Station", "Corpus Christi", "Dallas", "Denton",
    "Edinburg", "El Paso", "Fort Worth", "Frisco", "Garland", "Grand Prairie", "Houston", "Irving",
    "Killeen", "Laredo", "League City", "Lewisville", "Longview", "Lubbock", "McAllen", "McKinney",
    "Mesquite", "Midland", "Mission", "Missouri City", "Odessa", "Pasadena", "Pearland", "Pharr",
    "Plano", "Richardson", "Round Rock", "San Angelo", "San Antonio", "Sugar Land", "Tyler", "Waco",
    "Wichita Falls", "Layton", "Ogden", "Orem", "Provo", "Salt Lake City", "Sandy", "St. George",
    "West Jordan", "West Valley City", "Alexandria", "Chesapeake", "Hampton", "Lynchburg",
    "Newport News", "Norfolk", "Portsmouth", "Richmond", "Roanoke", "Suffolk", "Virginia Beach",
    "Burlington", "Auburn", "Bellevue", "Bellingham", "Everett", "Federal Way", "Kennewick", "Kent",
    "Renton", "Seattle", "Spokane", "Spokane Valley", "Tacoma", "Vancouver", "Yakima", "Appleton",
    "Green Bay", "Kenosha", "Madison", "Milwaukee", "Racine", "Waukesha", "Charleston", "Cheyenne"
]


local_articles = []
global_articles = []

# Function to fetch news based on given parameters
def get_news(query, page_size):
    params = {
        'apiKey': api_key,
        'q': query,
        'language': 'en',
        'pageSize': page_size
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    if data['status'] == 'ok':
        return data['articles']
    else:
        print(f"Error fetching news for '{query}': {data['message']}")
        return []

# Fetching local news
for city in cities:
    articles = get_news(city, 20)  # Fetching 20 articles for each city
    local_articles.extend(articles)

# Fetching global news
global_keywords = 'global OR international OR world'
global_articles = get_news(global_keywords, 50)  # Fetching 50 global articles

# Combining and shuffling articles
all_articles = local_articles + global_articles

# Saving articles to a CSV file
with open('news_articles.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['source', 'author', 'title', 'description', 'url', 'publishedAt', 'content']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for article in all_articles:
        writer.writerow({
            'source': article['source']['name'],
            'author': article.get('author'),
            'title': article.get('title'),
            'description': article.get('description'),
            'url': article.get('url'),
            'publishedAt': article.get('publishedAt'),
            'content': article.get('content')
        })

print("Articles successfully saved to 'news_articles.csv'")
