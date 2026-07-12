# 🔭 Stargazing Advisor

A specialized analytics tool designed for astronomy enthusiasts and amateur stargazers to determine the optimal conditions for celestial observation at any specific location.

## 🌌 Overview

Not all clear nights are equal for stargazing. Factors like moon phase, atmospheric humidity, local particulate matter, and cloud cover significantly impact your visibility of deep-sky objects (DSOs) and planets. **Stargazing Advisor** processes real-time meteorological data and astronomical orbital positions to provide a "Visibility Score" and detailed recommendations.

## ✨ Key Features

- **Dynamic Weather Analysis:** Integrates atmospheric readings like cloud cover percentage, visibility distance, and precipitation probability.
- **Lunar Phase Awareness:** Automatically calculates the moon's illumination and altitude to warn about significant light pollution from the moon itself.
- **Atmospheric Clarity Index:** Analyzes humidity and air quality to predict how much "haze" might obscure distant galaxies.
- **Location-Based Recommendations:** Provide specific local conditions for any given coordinate or city name.
- **Optimal Window Alerts:** Identifies time windows where the combination of low lunar activity and clear skies creates peak viewing opportunities.
- **No API keys:** The featured APIs do not require authentication to be used.

## 🚀 Getting Started

### Prerequisites
- Python 3.9+

### Installation
1. Clone the repository:
   ```bash
   git clone <https://github.com/yourusername/startgazing-advisor.git
>   cd startgazing-advisor
   ```
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
## 📖 Usage

Run the application from the terminal:
```bash
python main.py
```
And follow the instructions!

## 🛠 Tech Stack
- **Python**: Core logic and data processing.
- **Requests**: Handling API interactions.
- **Rich**: For beautiful terminal output and progress indicators.

## 📊 Scoring System
The advisor calculates a score from **0 to 100** based on:

|   Factor    | Weight | Description                                                   |
|:-----------:|:------:|---------------------------------------------------------------|
| Cloud Cover |  40%   | Higher cover = lower score.                                   |
| Moon Phase  |  30%   | Full moon significantly reduces visibility of faint objects.  |
|  Humidity   |  20%   | High humidity causes light scattering.                        |
| Visibility  |  10%   | Overall atmospheric clarity impact.                           |

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.

## 📡 APIs and usages
- **[7Timer!](https://www.7timer.info/doc.php?lang=en)** for weather and cloud coverage data
- **[Horizons API](https://ssd-api.jpl.nasa.gov/doc/horizons.html#ephem_type)** for data on the moon and sun

---
*Made with 🌌 by the Stargazing Advisor Team.*