import { fetchWeatherApi } from "openmeteo";

const params = {
	latitude: -33.0475,
	longitude: -71.4425,
	daily: "rain_sum",
	hourly: "rain",
	models: ["ecmwf_ifs025", "ecmwf_ifs", "ecmwf_aifs025_single", "best_match"],
	current: "rain",
	timezone: "auto",
	past_days: 92,
	forecast_days: 16,
};
const url = "https://api.open-meteo.com/v1/forecast";
const responses = await fetchWeatherApi(url, params);

// Process 1 location and 4 models
for (const response of responses) {
	// Attributes for timezone and location
	const latitude = response.latitude();
	const longitude = response.longitude();
	const elevation = response.elevation();
	const timezone = response.timezone();
	const timezoneAbbreviation = response.timezoneAbbreviation();
	const utcOffsetSeconds = response.utcOffsetSeconds();
	
	console.log(
		`\nCoordinates: ${latitude}°N ${longitude}°E`,
		`\nElevation: ${elevation}m asl`,
		`\nTimezone: ${timezone} ${timezoneAbbreviation}`,
		`\nTimezone difference to GMT+0: ${utcOffsetSeconds}s`,
		`\nModel Nº: ${response.model()}`,
	);
	
	const current = response.current();
	const hourly = response.hourly();
	const daily = response.daily();
	
	// Note: The order of weather variables in the URL query and the indices below need to match!
	const weatherData = {
		current: {
			time: new Date((Number(current.time()) + utcOffsetSeconds) * 1000),
			rain: current.variables(0).value(),
		},
		hourly: {
			time: Array.from(
				{ length: (Number(hourly.timeEnd()) - Number(hourly.time())) / hourly.interval() }, 
				(_ , i) => new Date((Number(hourly.time()) + i * hourly.interval() + utcOffsetSeconds) * 1000)
			),
			rain: hourly.variables(0).valuesArray(),
		},
		daily: {
			time: Array.from(
				{ length: (Number(daily.timeEnd()) - Number(daily.time())) / daily.interval() }, 
				(_ , i) => new Date((Number(daily.time()) + i * daily.interval() + utcOffsetSeconds) * 1000)
			),
			rain_sum: daily.variables(0).valuesArray(),
		},
	};
	
	// The 'weatherData' object now contains a simple structure, with arrays of datetimes and weather information
	console.log(
		`\nCurrent time: ${weatherData.current.time}\n`,
		weatherData.current.rain,
	);
	console.log("\nHourly data:\n", weatherData.hourly)
	console.log("\nDaily data:\n", weatherData.daily)
}
