#It is a simple application that can show you what the weather is like in the city you entered in the input field
import tkinter as tk
import requests
from tkinter import BOTH, IntVar
from PIL import ImageTk, Image
from io import BytesIO

# Define window

root  =tk.Tk()
root.title("Weather Forecast")
root.iconbitmap("weather.ico")
root.geometry("400x400")
root.resizable(0,0)

# Define colors and fonts
sky_color = '#76c3ef'
grass_color = "#aad207"
output_color = "#a5bcd2"
input_color = '#ecf2ae'
large_font = ("SimSun", 14)
small_font = ("SimSun", 10)

# Define functions
def search():
    global response

    url = "https://api.openweathermap.org/data/2.5/weather?"
    api_key = "ccf76919f4cadd334cc26a07f6e4b865"

    if search_method.get() == 1:
        querystring = {"q":city_entry.get(), "appid":api_key, "units":"metric"}
    elif search_method.get() ==2:
        querystring = {"zip":city_entry.get(), "appid":api_key, "units":"metric"}

    response = requests.request("GET", url, params=querystring)
    response = response.json()


    '''{'coord': {'lon': 16.8927, 'lat': 52.3471}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds',
     'icon': '03d'}], 'base': 'stations', 'main': {'temp': 291.09, 'feels_like': 290.72, 'temp_min': 290.98, 'temp_max': 292.81,
      'pressure': 1004, 'humidity': 68}, 'visibility': 10000, 'wind': {'speed': 3.6, 'deg': 270}, 'clouds': {'all': 40},
       'dt': 1663156477, 'sys': {'type': 2, 'id': 19661, 'country': 'PL', 'sunrise': 1663129489, 'sunset': 1663175497},
        'timezone': 7200, 'id': 3092856, 'name': 'Luboń', 'cod': 200}'''
    get_weather()
    get_icon()

def get_weather():
    city_name = response["name"]
    city_lat = str(response["coord"]["lat"])
    city_lon = str(response["coord"]["lon"])

    main_weather = response['weather'][0]["main"]
    description = response['weather'][0]["description"]

    temp = str(response["main"]["temp"])
    feels_like = str(response["main"]["feels_like"])
    temp_min = str(response["main"]["temp_min"])
    temp_max = str(response["main"]["temp_max"])
    humidity = str(response["main"]["humidity"])

    city_info_label.config(text = city_name + "(" + city_lat + "," + city_lon + ")", font = large_font, bg = output_color)
    weather_label.config(text = "Weather: " + main_weather + ", " + description, font = small_font, bg = output_color)
    temp_label.config(text = "Temperature: " + temp + " C", font = small_font, bg = output_color)
    feels_label.config(text = "Feels Like: " + feels_like + " C", font = small_font, bg = output_color)
    temp_min_label.config(text = "Min Temperature: " + temp_min + " C", font = small_font, bg = output_color)
    temp_max_label.config(text = "Max Temperature: " + temp_max + " C", font = small_font, bg = output_color)
    humidity_label.config(text = "Humidity: " + humidity, font= small_font, bg = output_color )



def get_icon():
    global img
    icon_id = response["weather"][0]['icon']

    url = "http://openweathermap.org/img/wn/{icon}@2x.png".format(icon=icon_id)

    icon_response = requests.get(url, stream=True)

    img_data = icon_response.content

    img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))

    photo_label.config(image = img)

    # Define layout
# Create frames
sky_frame = tk.Frame(root, bg=sky_color, height=250)
grass_frame = tk.Frame(root, bg=grass_color)
sky_frame.pack(fill=BOTH, expand=True)
grass_frame.pack(fill=BOTH, expand=True)

output_frame = tk.LabelFrame(sky_frame, bg =  output_color, width=325, height=225)
input_frame = tk.LabelFrame(grass_frame, bg = input_color, width=325)
output_frame.pack(pady=30)
output_frame.pack_propagate(0)
input_frame.pack(pady=15)


# Output frame layout
city_info_label = tk.Label(output_frame, bg =  output_color, text = "")
weather_label = tk.Label(output_frame, bg =  output_color, text = "")
temp_label = tk.Label(output_frame, bg =  output_color, text = "")
feels_label = tk.Label(output_frame, bg =  output_color, text = "")
temp_min_label = tk.Label(output_frame, bg =  output_color, text = "")
temp_max_label = tk.Label(output_frame, bg =  output_color, text = "")
humidity_label = tk.Label(output_frame, bg =  output_color, text = "")
photo_label = tk.Label(output_frame, bg =  output_color, text = "")

city_info_label.pack(pady=8)
weather_label.pack()
temp_label.pack()
feels_label.pack()
temp_min_label.pack()
temp_max_label.pack()
humidity_label.pack()
photo_label.pack(pady=8)

# Input frame layout
city_entry = tk.Entry(input_frame, width = 20, font = large_font)
submit_button = tk.Button(input_frame, text = "Submit", font = large_font, bg = input_color, command=search)

search_method =IntVar()
search_method.set(1)
search_city = tk.Radiobutton(input_frame, text = "Search by city name", variable = search_method, value = 1, font = small_font,  bg = input_color)
search_zip = tk.Radiobutton(input_frame, text = "Search by ZIP", variable = search_method, value =2, font = small_font,bg = input_color)
city_entry.grid(row=0, column= 0, padx= 10, pady= (10,0))
submit_button.grid(row=0, column= 1, padx= 10, pady= (10,0))
search_city.grid(row=1, column= 0, pady=2)
search_zip.grid(row=1, column= 1, pady=2, padx =10)

# Root window mainloop
root.mainloop()