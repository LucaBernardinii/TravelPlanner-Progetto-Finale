# TravelPlanner

A web application for planning and organizing your travels. Track your trips, add destinations, check weather forecasts, and discover points of interest around the world. Built with Flask and SQLite, TravelPlanner provides a complete platform for managing your travel adventures.

Website: https://travelplanner-ws6x.onrender.com
Disclaimer: The web version might be slow or not work properly due to Render's free tier limitations. For the best experience, run the application locally.

## Features

### **Trip Management**
- Create, edit, and delete your personal trips with title, dates, and notes
- Complete CRUD operations on all your trips
- Organize and manage all your travel plans in one place
- View all your trips on a centralized dashboard

### **Destinations & Activities**
- Add multiple destinations to each trip with geographic coordinates
- Create and manage activities at each destination
- Organize activities by category: hotels, restaurants, museums, attractions, transport, and general
- Set specific arrival and departure dates for each destination
- Edit or remove destinations and activities anytime

### **Trip Sharing & Discovery**
- Share your trips with other users by toggling the sharing feature
- Browse shared trips from other travelers for inspiration
- Discover public travel plans in the community
- View the owner's name when browsing shared trips

### **Location Services**
- Search destinations worldwide using Nominatim geocoding service
- Get exact geographic coordinates for any location
- View destinations on an interactive map powered by Leaflet and OpenStreetMap
- Calculate routes and distances between destinations using OSRM routing engine

### **Weather Forecasts**
- Get 7-day weather forecasts for your destinations
- View daily temperature ranges (max/min), precipitation data, sunrise and sunset times
- Plan activities and packing based on accurate weather predictions

### **User Authentication**
- Secure registration with email and password
- Password hashing with Werkzeug security
- Login and session management
- Protected routes to keep your data private

## Installation

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd TravelPlanner-Progetto-Finale
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install requirements**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**
   ```bash
   python setup_db.py
   ```

5. **Run the application**
   ```bash
   python run.py
   ```

6. **Access the application**
   Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## Project Structure

```
TravelPlanner-Progetto-Finale/
├── app/
│   ├── __init__.py                  # Flask app initialization
│   ├── models.py                    # Database models
│   ├── schema.sql                   # Database schema
│   ├── blueprints/                  # Blueprint modules
│   │   ├── __init__.py
│   │   ├── auth.py                  # Authentication blueprint
│   │   ├── trips.py                 # Trips management blueprint
│   │   ├── explore.py               # Destination exploration blueprint
│   │   └── api.py                   # API endpoints blueprint
│   ├── repositories/                # Data access layer (Repository pattern)
│   │   ├── __init__.py
│   │   ├── user_repository.py
│   │   ├── trip_repository.py
│   │   ├── destination_repository.py
│   │   └── attivita_repository.py
│   ├── static/                      # Static files
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       ├── explore.js           # Explore page logic
│   │       └── map.js               # Map interaction scripts
│   └── templates/                   # HTML templates
│       ├── base.html                # Base template
│       ├── auth/                    # Authentication templates
│       │   ├── login.html
│       │   └── register.html
│       ├── explore/                 # Explore templates
│       │   └── search.html
│       ├── trips/                   # Trip templates
│       │   ├── index.html
│       │   ├── form.html
│       │   ├── detail.html
│       │   └── add_destination.html
│       └── errors/                  # Error pages
│           ├── 404.html
│           └── 500.html
├── instance/                        # Instance folder (SQLite database)
├── config.py                        # Application configuration
├── run.py                           # Application entry point
├── setup_db.py                      # Database setup script
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

## External APIs Used

This application uses the following free APIs to enhance functionality:

| API | Purpose | Registration Required |
|---|---|---|
| **[Nominatim](https://github.com/osm-search/Nominatim.git)** | Geocoding (city/destination name → geographic coordinates) | No |
| **[OpenStreetMap](https://github.com/openstreetmap) ([Leaflet](https://github.com/Leaflet/Leaflet.git))** | Interactive map display for destinations and activities | No |
| **[Open-Meteo](https://open-meteo.com/)** | 7-day weather forecasts with detailed daily metrics | No |
| **[OSRM](https://github.com/Project-OSRM/osrm-backend.git)** | Route calculation and distance measurement between locations | No |

All APIs are free and do not require paid registration.

## Technologies Used

- **Backend Framework**: Flask 3.1.3
- **Database**: SQLite3
- **Web Server**: Gunicorn
- **HTTP Client**: Requests
- **Security**: Werkzeug (password hashing)
- **Configuration Management**: python-dotenv
- **Frontend**: HTML5, CSS3, JavaScript

## Requirements

- Python 3.7 or higher
- Flask 3.1.3
- SQLite3
- Other dependencies listed in `requirements.txt`

## Usage

### Creating a Trip
1. Log in with your credentials
2. Navigate to the trips section
3. Click "Create New Trip"
4. Enter trip details: title, start date, end date, and personal notes
5. Save the trip

### Adding Destinations to Your Trip
1. Open a trip detail page
2. Click "Add Destination"
3. Search for a location using Nominatim geocoding (e.g., "Paris, France")
4. Select from search results to get exact coordinates
5. Set arrival and departure dates for the destination
6. The destination appears on the interactive map

### Managing Activities at Destinations
1. In a trip's detail page, find a destination
2. Click "Add Activity" for that destination
3. Enter activity details: name, type (hotel, restaurant, museum, attraction, transport, general)
4. Optionally add GPS coordinates if known
5. View all activities organized by type and location on the map

### Checking Weather Forecasts
1. Navigate to a trip's detail page
2. Select a destination to view its weather
3. See the 7-day forecast with temperature ranges, precipitation, sunrise/sunset times
4. Plan packing and activities based on weather data

### Sharing Your Trips
1. Open a trip you want to share
2. Click the "Share" button to toggle sharing status
3. Shared trips appear in the "Community Trips" section for other users
4. Browse other users' shared trips for travel inspiration
5. View detailed information about shared trips, including the owner's name

### Calculating Routes
1. When viewing multiple destinations in a trip
2. The application can calculate the route and distance between locations
3. Use OSRM routing engine for accurate distance and travel time estimates

## Development

### Database Management

To reset the database:
```bash
python setup_db.py
```

### Project Architecture

- **Blueprints**: Modular application components (auth, trips, explore)
- **Repository Pattern**: Data access layer abstraction
- **Server-side Processing**: All API calls happen on the backend
- **No Client-side JavaScript**: Keeps the application simple and secure

## License

This project is open source and available under the MIT License.

## Author

Private Account: [@LucaBernardiniii](https://github.com/LucaBernardiniii)

School Account:
Luca Bernardini - luca.bernardini@studenti.isissgobetti.it

TravelPlanner is developed as a final project for the fifth year of Computer Science studies.

## Other Projects

[MMDb](https://github.com/LucaBernardinii/MMDb_progetto_natale.git) - Web App inspired by Letterboxd

[Briscola Remastered](https://github.com/LucaBernardinii/Briscola_Remastered_progetto_di_natale.git) - Command Line game inspired by the traditional italian card game

## Contributing

Contributions are welcome. Feel free to fork this repository and submit pull requests for any improvements.
