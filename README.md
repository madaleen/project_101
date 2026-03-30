# Food Saving & Donation Platform

A platform to reduce food waste by connecting Restaurants/Merchants with NGOs and Individuals for donations and discounts.

## 🚀 Vision
To create a seamless bridge between surplus food and those in need, ensuring transparency and efficiency through technology.

## 👥 Roles & Responsibilities
- **Merchant (Restaurant/Shop)**: Posts items for donation or at a discount.
- **NGO / Care Center**: Claims donations for those in need.
- **Individual Volunteer**: Claims donations and helps with distribution.

## 🛠️ Tech Stack
- **Frontend**: React (Vite) - Mobile responsive.
- **Backend**: Python 3.12 (FastAPI) - Async engine.
- **Database**: PostgreSQL + PostGIS (Geospatial search).

## 📂 Project Structure
- `/frontend`: React application.
- `/backend`: FastAPI application (modular `app` package).
  - `/backend/app`: Model, Schema, Security, and Routers logic.
- `/database`: Initial schema drafts.

## 🌿 Git Strategy
- `main`: Production-ready code.
- `develop`: Integration branch.
- `feature/foodsave-backend`: Current backend implementation.
