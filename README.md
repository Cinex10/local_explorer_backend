# Local Explorer Backend

## Overview
Local Explorer is a backend service that provides location-based data and services for exploring places, businesses, and points of interest. The service integrates with multiple APIs including Google Maps, OpenWeather, and geocoding services to deliver comprehensive location information.

## Features
- Location-based search and discovery
- Integration with Google Maps API
- Weather information via OpenWeather API 
- Geocoding capabilities
- Custom data schemas for standardized responses
- Support for opening hours and business details
- Accessibility information
- Address and landmark details

## Technology Stack
- Python backend
- Google Maps API integration
- OpenWeather API integration
- Geocoding API
- GROQ API for data querying
- Environment-based configuration

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
Create a `.env` file with the following keys:
```
GOOGLE_MAPS_API_KEY=your_key
OPENWEATHER_API_KEY=your_key 
GEOCODING_API_KEY=your_key
GROQ_API_KEY=your_key
MODEL="llama-3.1-8b-instant"
```

## API Reference

The service provides various endpoints for accessing location data. Key features include:

- Location search
- Business details
- Opening hours
- Accessibility information
- Weather data
- Geocoding services

## Data Models

The application uses custom data models for standardizing responses, including:

- Opening Hours
- Location Details
- Weather Information
- Address Information
