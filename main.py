import multiprocessing
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from waitress import serve
import hashlib
import json
import matrix_display.splashscreen1x128 as splashscreen1x128
import news.foxnews as foxnews, news.espnnews as espnnews
import matrix_display.displayLeague1x128 as displayLeague1x128
import matrix_display.displayEvents1x128 as displayEvents1x128
import matrix_display.displayNews1x128 as displayNews1x128
import sports.mlb as mlb, sports.nfl as nfl, sports.nba as nba, sports.ncaaf as ncaaf
import sports.ncaam as ncaam, sports.ncaaw as ncaaw, sports.wnba as wnba, sports.nhl as nhl
from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions
from config.config_loader import ConfigError, ConfigLoader
import socket

app = Flask(__name__)
app.secret_key = "secret_key"
app.config["SESSION_PERMANENT"] = False
CONFIG_FILE = "./config/main_config.json"
main_thread = None

def get_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return str(s.getsockname()[0])
    except socket.error:
        return "Unable to determine IP address"
    
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        config = load_config()
        username = request.form.get("username")
        password = request.form.get("password")
        stored_username = config["authentication"]["username"]
        stored_password = hash_password(config["authentication"]["password"])

        if username == stored_username and hash_password(password) == stored_password:
            session["logged_in"] = True

            next_page = session.pop("next", url_for("index"))
            return redirect(next_page)
        else:
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

def load_config():
    try:
        return ConfigLoader(CONFIG_FILE).config
    except ConfigError as e:
        print(f"Configuration Error: {e}")
        return {}
    
def save_config(config):
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file, indent=4)

@app.route("/")
def index():
    if not session.get("logged_in"):
        session["next"] = request.url
        return redirect(url_for("login"))
    config = load_config()

    # Join the 'displayed_leagues' list as a string for display in the form
    displayed_leagues = ", ".join(config['leagues']['displayed_leagues'])

    return render_template("index.html", config=config, displayed_leagues=displayed_leagues)
        
def setup_matrix():
    options = RGBMatrixOptions()
    options.rows = 64
    options.cols = 128
    options.chain_length = 1
    options.parallel = 1
    options.brightness = 75
    options.hardware_mapping = 'regular'
    return RGBMatrix(options=options)

def run_app(league, news_source, matrix, config):
    match league: 
        case 'mlb':
            category = 'baseball'
            espn_sport = 'mlb'
            fox_sport = 'mlb'
            events_data = mlb.getData()
        case 'nba':
            category = 'basketball'
            espn_sport = 'nba'
            fox_sport = 'nba'
            events_data = nba.getData()
        case 'nfl':
            category = 'football'
            espn_sport = 'nfl'
            fox_sport = 'nfl'
            events_data = nfl.getData()
        case 'ncaaf':
            category = 'football'
            espn_sport = 'college-football'
            fox_sport = 'college-football'
            events_data = ncaaf.getData(config["leagues"]["ncaaf_conference"])
        case 'ncaam':
            category = 'basketball'
            espn_sport = 'mens-college-basketball'
            fox_sport = 'college-basketball'
            events_data = ncaam.getData(config["leagues"]["ncaam_conference"])
        case 'ncaaw':
            category = 'basketball'
            espn_sport = 'womens-college-basketball'
            fox_sport = 'womens-college-basketball'
            events_data = ncaaw.getData(config["leagues"]["ncaaw_conference"])
        case 'wnba':
            category = 'basketball'
            espn_sport = 'wnba'
            fox_sport = 'wnba'
            events_data = wnba.getData()
        case 'nhl':
            category = 'hockey'
            espn_sport = 'nhl'
            fox_sport = 'nhl'
            events_data = nhl.getData()

    if news_source == 'espn':
        headlines_data = espnnews.main(category, espn_sport)
    elif news_source == 'fox':
        headlines_data = foxnews.main(fox_sport) 

    for article in headlines_data:
        if config["news"]["source"] == 'espn':
            print(article[0])
            print("/".join(article[1]))
        else:
            print(article)
        print('-'*80)

    displayLeague1x128.main(league, matrix, config)

    if config['other']['first_display'] == 'events':
        displayEvents1x128.main(events_data, matrix, config)
        if config['news']['display_news']:
            displayNews1x128.main(headlines_data, matrix, config)
    elif config['other']['first_display'] == 'news':
        displayNews1x128.main(headlines_data, matrix, config)
        if config['events']['display_events']:
            displayEvents1x128.main(events_data, matrix, config)

def run_main_app():
    try:
        matrix = setup_matrix()

        config = load_config()
        leagues = config['leagues']['displayed_leagues']
        news = config['news']['source']

        splashscreen1x128.main(get_ip(), matrix, config)

        while True:
            for league in leagues:
                run_app(league, news, matrix, config)
    except KeyboardInterrupt:
        print("Quitting program...")

def stop_app():
    global main_thread
    if main_thread and main_thread.is_alive():
        main_thread.terminate()
        print("App stopped.")

def restart_app():
    print("Restarting app...")
    stop_app()
    # Restart the app by creating a new thread and starting it again
    start_app()

def start_app():
    global main_thread
    main_thread = multiprocessing.Process(target=run_main_app)
    main_thread.start()

@app.route("/update", methods=["POST"])
def update_config():
    new_values = request.json
    config = load_config()

    for key, value in new_values.items():
        keys = key.split('.')
        target = config
        for k in keys[:-1]:
            target = target[k]
        target[keys[-1]] = value
    
    try:
        save_config(config)
        ConfigLoader(CONFIG_FILE).validate_config()
        return jsonify({"message": "Configuration updated successfully", "new_config": config})
    except ConfigError as e:
        return jsonify({"error": str(e)}), 400

@app.route("/restart", methods=["POST"])
def restart():
    restart_app()
    return jsonify({"message": "App is restarting..."})

if __name__ == "__main__":
    start_app()  # Start the main app
    
    serve(app, host='0.0.0.0', port=5001)