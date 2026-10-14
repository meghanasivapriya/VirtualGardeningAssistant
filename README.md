# 🌱 Virtual Gardening Assistant

A Django-based web application that helps users care for their plants through weather-based recommendations, plant identification, and plant health diagnosis.

## Features

- **User Authentication:** Register, log in, and manage your account.
- **Plant Management:** Add, view, update, and delete personal plant records.
- **Weather Updates:** Get weather information using browser geolocation.
- **Smart Plant Care:** Receive general plant care recommendations based on weather conditions.
- **Plant Identification:** Identify plants from uploaded photos using the PlantNet API.
- **Plant Health Diagnosis:** Analyze tomato and potato plant health using the PlantHealthEngine API.
- **Profile Management:** Update profile details and upload a profile picture.

## Technologies Used

- **Backend:** Python, Django
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite
- **APIs:** OpenWeather API, PlantNet API, PlantHealthEngine API
- **Tools:** PyCharm, Git, GitHub

## Installation and Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/meghanasivapriya/VirtualGardeningAssistant.git
   ```

2. Navigate to the project directory:

   ```bash
   cd VirtualGardeningAssistant
   ```

3. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   ```

   Windows PowerShell:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

4. Install the required dependencies:

   ```bash
   pip install django pillow requests
   ```

5. Configure your API keys using environment variables or a `.env` file. Never commit API keys or other secrets to GitHub.

6. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

7. Start the development server:

   ```bash
   python manage.py runserver
   ```

8. Open `http://127.0.0.1:8000/` in your browser.

## Project Goal

The goal of this project is to make plant care more accessible by combining web development, weather information, plant identification, and plant health analysis in one application.

## Future Enhancements

- More plant disease detection capabilities
- Personalized plant care schedules
- Plant watering reminders
- Expanded plant database and recommendations

## Author

**Meghana B.**

GitHub: [@meghanasivapriya](https://github.com/meghanasivapriya)
