# Algodex: Master Rubik's Cube Algorithms Through Practice

## Overview

**Algodex** is a web platform designed to help Rubik's cube enthusiasts search, learn, and practice algorithms efficiently. Whether you're a casual solver or competitive speedcuber, Algodex provides an intuitive interface to explore algorithms across all three major solving methods (F2L, OLL, and PLL), view community feedback, and track your practice progress over time.

The platform operates on a freemium model: anonymous users can search and practice algorithms without creating an account, but their solve times are not persisted. Registered users unlock the full experience—they can post custom algorithms, vote on existing ones, and maintain a comprehensive history of their practice sessions.

## Screenshots
![homepage](assets/homepage.png)
![login page](assets/login.png)
![register page](assets/register.png)
![algorithm page](assets/algorithm-page.png)
![practice without account](assets/practice-no-account.png)
![profile with no solve](assets/profile-no-solve.png)
![profile with solves](assets/profile-with-solve.png)

## Distinctiveness and Complexity: Why This Project Satisfies Requirements

### What Makes Algodex Distinctive

Algodex stands apart from typical CS50 Web projects in several meaningful ways:

**1. Domain-Specific Problem Solving:** Most course projects build generic CRUD applications (e.g., social networks, note apps, e-commerce sites). Algodex targets a niche but passionate community—Rubik's cube speedcubers—and solves a *real problem* they face: algorithm fragmentation. Cubers often reference algorithms from YouTube videos, Reddit threads, or scattered notation documents. Algodex centralizes this knowledge in one searchable, votable, practice-enabled platform. This isn't a generic social app; it's purpose-built for a specific user base with specific needs.

**2. Dual-Mode User Architecture:** The ability to function both with and without authentication is uncommon in CS50 projects. Most applications enforce login immediately. Algodex allows anonymous exploration and practice, removing friction for new users while still incentivizing account creation through persistent solve tracking. This required careful conditional logic throughout the codebase and thoughtful UX design—not a trivial undertaking.

**3. Real-Time Timer with Backend Persistence:** The practice timer is the *heart* of Algodex, and implementing it presented genuine technical complexity. Rather than rely on pre-built libraries or Django REST Framework (which would bloat the project scope), I engineered a custom JavaScript-to-Django pipeline using the Fetch API. This required:
   - Building a JavaScript stopwatch that accurately measures solve times
   - Sending timer data via POST request to a Django view without a REST API framework
   - Validating and persisting timing data on the backend
   - Preventing timing manipulation or cheating attempts
   
   This "custom integration" approach keeps the codebase lean while solving a problem that simpler projects would ignore entirely.

**4. Voting System with Duplicate Prevention:** The algorithm voting feature uses Django's `ManyToManyField` to prevent users from voting multiple times on the same algorithm. While this pattern exists in Django documentation, implementing it correctly—with proper queryset checks, atomic operations, and seamless frontend-backend coordination—demonstrates solid understanding of Django's ORM and relational database design.

**5. Profile Analytics:** Each user profile displays their solve history, complete with timestamps and algorithm details. This requires complex queryset optimization (filtering `Solve` records by user, prefetching related `Algorithm` data) and presents a simple but effective analytics dashboard—a feature that adds genuine value to the platform.

### Technical Complexity Breakdown

- **Custom Fetch API Integration:** Without using Django REST Framework or REST library, managing JSON data transfer between JavaScript and Django required understanding of CORS, HTTP methods, CSRF tokens, and request/response cycles.
- **Conditional Authentication Logic:** Using `request.user.is_authenticated` throughout templates and views to conditionally render features (post algorithm, vote, save solves) added complexity to template logic and view functions.
- **Database Design:** The `Solve` model's `ForeignKey` to both `User` and `Algorithm` enables complex queries for user analytics and algorithm popularity tracking.
- **Form Handling with django-widget-tweaks:** Custom form rendering required configuration beyond Django's defaults, adding polish and usability to the UI.

In summary, Algodex is **not** a generic CRUD app reskinned for a different domain. It's a thoughtfully designed platform that solves a real niche problem, implements non-trivial authentication patterns, and showcases custom backend-frontend integration without relying on heavy frameworks.

---

## File Structure and Descriptions

### Backend (Django)

- **`manage.py`** – Django's command-line utility for project management.
- **`__init__.py`** – Package initialization file.
- **`settings.py`** – Django configuration (installed apps, middleware, database, static files, etc.).
- **`admin.py`** – Django admin interface configuration for managing `Algorithm` and `Solve` models in the backend.
- **`apps.py`** – Application configuration.
- **`forms.py`** – Django form definitions for user input (registration, algorithm creation, voting).
- **`models.py`** – Database models:
  - **`Algorithm`** – Represents a Rubik's cube algorithm with name, category (F2L/OLL/PLL), move notation, description, creator, creation timestamp, yes/no vote counts, and a M2M field of voters to prevent duplicate votes.
  - **`Solve`** – Tracks individual practice sessions, recording the user, solve time (in seconds), algorithm practiced, and timestamp.
- **`tests.py`** – Unit and integration tests for views and models.
- **`urls.py`** – URL routing configuration mapping endpoints to view functions.
- **`views.py`** – Core application logic:
  - `index()` – Homepage displaying algorithms filtered by category.
  - `algorithm_detail()` – Displays a single algorithm with moves, description, votes, and practice button.
  - `practice()` – Renders the practice page with timer interface.
  - `submit_solve()` – Handles POST requests from the JavaScript timer, validates and saves `Solve` records.
  - `vote()` – Processes algorithm votes, checks if user has already voted using the `voters` M2M field.
  - `post_algorithm()` – Allows authenticated users to create new algorithms.
  - `profile()` – Displays user profile with solve history and statistics.
  - Authentication views (login, register, logout).
- **`db.sqlite3`** – SQLite database (stores all users, algorithms, and solve records).

### Frontend (Templates & Static Files)

**Templates** (Django HTML templates with Jinja2 syntax):
- **`layout.html`** – Base template with navigation bar, responsive layout, and footer. Uses `request.user.is_authenticated` to conditionally show login/register or profile/logout links.
- **`home.html`** – Homepage displaying algorithm cards in a grid, filterable by category (F2L, OLL, PLL).
- **`algorithm_detail.html`** – Single algorithm view showing:
  - Algorithm name and creator
  - Move notation (e.g., "R U R' U' R2 U2 R")
  - Description and voting counts
  - Vote buttons (only visible to authenticated users)
  - Comments/feedback section
  - "Practice this algorithm" button
- **`practice.html`** – Interactive practice interface with:
  - Algorithm display
  - JavaScript-powered timer (00:00:00 format)
  - Start/Stop buttons
  - Submit button to save solve time (if authenticated)
  - Warning message for anonymous users that times won't be saved
- **`profile.html`** – User profile page displaying:
  - Username and join date
  - Total solves and average time
  - Detailed solve history table with algorithm name, time, and date
- **`register.html`** – User registration form.
- **`login.html`** – Login form.
- **`create_algorithm.html`** – Form for authenticated users to post new algorithms (category dropdown, move input, description textarea).

**Static Files:**
- **`navbar.js`** – Handles mobile navigation menu toggle.
- **`timer.js`** – **Core timer logic:**
  - Stopwatch implementation (millisecond precision)
  - Start/Stop button event listeners
  - Fetch API POST request sending timer data to `submit_solve()` view
  - CSRF token handling for secure form submission
  - Client-side validation and error handling
- **`main.css`** – Global styles (dark theme, gold accents, responsive grid layout).
- **`home.css`** – Homepage-specific styles (algorithm card layout, filter buttons).
- **`page.css`** – Page-specific styles (algorithm detail, practice interface).
- **`practice.css`** – Practice mode styles (timer display, button styling).
- **`profile.css`** – Profile page styles (solve history table, user info card).

### Project Configuration

- **`urls.py`** (main project) – Routes all requests to the `main` app's URL patterns.
- **`__init__.py`, `asgi.py`, `wsgi.py`** – Project initialization and server configuration files.
- **`requirements.txt`** – List of Python package dependencies.

---

## How to Run Your Application
### Prerequisites
- **Python 3.8+** installed on your system
- **pip** (Python package manager)
- **Git** (optional, for cloning the project)

### Setup Instructions

1. **Clone or download the project:**
   ```bash
   git clone <repository-url>
   cd Algodex
   ```

2. **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```

5. **Create a superuser account (optional, for Django admin):**
    ```bash
    python manage.py createsuperuser

    Run the development server:
    bash

    python manage.py runserver

    Open your browser and navigate to:

    http://127.0.0.1:8000/
    ```

## Usage
- Browse algorithms: Visit the homepage to search and filter algorithms by category (F2L, OLL, PLL).
- Practice without an account: Click "Practice this algorithm" to use the timer. Your times won't be saved.
- Create an account: Click "Register" to set up a free account and unlock algorithm posting and vote tracking.
- Post an algorithm: Once logged in, navigate to "Post Algorithm" and fill in the form with your algorithm's name, category, move notation, and description.
- Vote on algorithms: Click "It's working" or "It's not working" to vote on algorithm quality (requires login).
- View your profile: Click "Profile" in the navigation to see your practice history and statistics.

## Additional Information
### Dependencies
All required Python packages are listed in requirements.txt:

    Django 3.2+ – Web framework
    django-widget-tweaks – Enhanced form rendering with custom CSS classes and attributes
    SQLite3 – Default database (built into Python)

**Key Design Decisions**

No REST API Framework: To keep the project scope manageable and focused on core functionality, I avoided Django REST Framework. Instead, the timer-to-database pipeline uses vanilla Fetch API and Django views—this reduced overhead while demonstrating understanding of HTTP fundamentals.

M2M Voters Field: Rather than creating a separate Vote model, I used Django's ManyToManyField with custom queryset checks to prevent duplicate votes. This keeps the schema lean and leverages Django's ORM strengths.

SQLite Database: Appropriate for development and small-scale deployment. No external database server required.

Responsive Design: CSS media queries and flexbox ensure the app works on mobile, tablet, and desktop devices—important for a practice app that users may access on phones at competitions.

Anonymous User Support: Most Algodex features work without authentication, lowering the barrier to entry for new users exploring the platform.

**Future Enhancements**

Algorithm Statistics: Track which algorithms are practiced most frequently and average solve times per algorithm.
Leaderboards: Display fastest solvers for each algorithm category.
Algorithm Comments: Allow users to leave detailed feedback and tips on specific algorithms.
Spaced Repetition: Recommend algorithms for practice based on historical solve times and intervals.
Export Solve Data: Allow users to download their solve history as CSV or JSON.
Algorithm Variants: Tag algorithm variations (e.g., "standard" vs. "alternate" for the same case).

## Conclusion
Algodex demonstrates full-stack web development proficiency: a Django backend with relational database design, custom authentication logic, and a responsive frontend with vanilla JavaScript integration. The project solves a niche problem with genuine technical depth, avoiding the pitfall of "generic CRUD with a theme." It's ready for speedcubers worldwide to master their algorithms.
