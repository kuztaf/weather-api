# Weather API

A RESTful API to retrieve current weather information and forecasts.

## Features

- Get current weather by city or coordinates.
- Extended forecast.
- JSON responses.

## Installation

You can use Docker to install dependencies and automatically start Redis:

```bash
docker-compose up
```

This will install all necessary dependencies and start both the application and a Redis container.

Alternatively, you can install manually:

```bash
git clone https://github.com/kuztaf/weather-api.git
cd weather-api
```

## Descripción

Se usa Redis para realizar cache sobre las solicitudes al API y evitar hacer muchas llamadas al API externo.

## 🛠 Tecnologías & Herramientas

![Python](https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/-Django-092E20?style=flat-square&logo=django&logoColor=white)
![Docker](https://img.shields.io/badge/-Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![Redis](https://img.shields.io/badge/-Redis-DC382D?style=flat-square&logo=redis&logoColor=white)
![Pytest](https://img.shields.io/badge/-Pytest-0A9EDC?style=flat-square&logo=pytest&logoColor=white)
