#!/usr/bin/env python3
from tools.base_tool import *
import requests
import json
from tools.base_tools_manager import BaseToolsManager


class WeatherToolsManager(BaseToolsManager):
    def __init__(self) -> None:
        BaseToolsManager.__init__(self)
        city_parameter = ToolParameter(name="city", description="The city to get the latitude and longitude for.", type="string", required=True)
        country_parameter = ToolParameter(name="country", description="The country to get the latitude and longitude for.", type="string", required=True)
        city_to_lat_long_parameters = ToolParameters(parameters=[city_parameter, country_parameter])
        city_to_lat_long_tool = Tool(name="CityToLatLongTool", description="Get the latitude and longitude for a given city.", parameters=city_to_lat_long_parameters)

        latitude_parameter = ToolParameter(name="latitude", description="The latitude of the location.", type="number", required=True)
        longitude_parameter = ToolParameter(name="longitude", description="The longitude of the location.", type="number", required=True)
        weather_from_lat_long_parameters = ToolParameters(parameters=[latitude_parameter, longitude_parameter])
        weather_from_lat_long_tool = Tool(name="WeatherFromLatLongTool", description="Get the weather for a certain location.", parameters=weather_from_lat_long_parameters)

        self.tools = ToolsArray(tools=[city_to_lat_long_tool, weather_from_lat_long_tool])
        # print(self.tools.to_json())

    def handle_tool_as_json(self, tool_name, tool_arguments):
        # TODO. Convert to dictionary search
        tool_response = {}
        if tool_name == "CityToLatLongTool":
            tool_result = self._city_to_lat_long(city=tool_arguments["city"], country=tool_arguments["country"])
            tool_response = {"name": tool_name, "result": tool_result}
        elif tool_name == "WeatherFromLatLongTool":
            tool_result = self._weather_from_lat_long(latitude=tool_arguments["latitude"], longitude=tool_arguments["longitude"])
            tool_response = {"name": tool_name, "result": tool_result}

        return json.dumps(tool_response)

    def _weather_from_lat_long(self, latitude: str, longitude: str):
        position_temperature = {}
        try:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m&temperature_unit=celsius&wind_speed_unit=mph&timezone=auto&forecast_days=1"
            # print(url)

            response_weather = requests.get(url=url, timeout=1)
            data = response_weather.json()

            if data:
                # print(json.dumps(data))
                temperature = data["current"]["temperature_2m"]
                position_temperature = {"temperature": temperature, "temperature_unit": "celsius"}
        except Exception as e:
            print("Error: " + str(e))
        return position_temperature

    def _city_to_lat_long(self, city: str, country: str):
        # TODO. allow accepting country as well
        city_position = {}
        try:
            url = f"https://nominatim.openstreetmap.org/search?city={city}&country={country}&format=json&addressdetails=1&limit=1"
            # print(url)

            response_city = requests.get(url=url, timeout=1)
            data = response_city.json()
            # print(data)
            if data:
                # Extract the latitude and longitude from the first result
                lat = float(data[0]["lat"])
                lon = float(data[0]["lon"])
                # Add the city, latitude, and longitude to the results list
                city_position = {"latitude": lat, "longitude": lon}
        except Exception as e:
            print("Error: " + str(e))
        return city_position

def main():
    weatherToolsManager = WeatherToolsManager()
    print(weatherToolsManager.get_all_tools())

    # city = "paris"
    # city_pos = city_to_lat_long(city=city)
    # # print(json.dumps(city_pos))
    # city_temp = weather_from_lat_long(latitude=city_pos["latitude"], longitude=city_pos["longitude"])
    # # print(json.dumps(city_temp))
    # temp = city_temp["temperature"]
    # print(f"Current temperature in {city} is {temp} degrees celsius.")

if __name__ == "__main__":
    main()
