
# FUN-H (Food UNH)

**FUN-H** (Food UNH) is a full-stack web application designed to streamline dining hall selection and promote healthy eating habits for University of New Hampshire students. Built by students for students, the platform enables users to browse daily menus, create USDA-compliant "Wildcat Plates," and manage their meal records.

---

## Platform

- Frontend: HTML, CSS, JavaScript (jQuery)
- Backend: Flask (Python)
- Templating: Jinja2
- Database: MongoDB
- Version Control: Git / GitLab

---

## Features

- Dynamic Daily Menus  
  View updated menu options for Philbrook and Holloway Commons dining halls.

- Wildcat Plate Creation  
  Build balanced meals by selecting items across four USDA-approved dietary categories: Fruits, Whole Grains, Vegetables, and Lean Protein.

- Account System  
  User registration and login via AJAX-powered forms. Sessions managed server-side.

- Meal Record Management  
  Save, view, edit, and delete past Wildcat Plates.

- Responsive UI  
  Mobile-friendly design with intuitive navigation and form handling.

- Admin Contact Page  
  Direct communication for feedback or inquiries.

---

## Major Components

| File                 | Description                                                 |
|----------------------|-------------------------------------------------------------|
| `index.html`         | Landing page with introduction and dining hall information. |
| `navbar.html`        | Reusable navigation bar template.                           |
| `createAccount.html` | User registration and login forms (AJAX integrated).        |
| `date.html`          | Plate creation with daily menu selection.                   |
| `editPlate.html`     | Edit existing Wildcat Plates.                               |
| `scripts.js`         | AJAX submission for login/signup and client-side behavior.  |
| `jquery.js`          | jQuery library for DOM manipulation and AJAX requests.      |

---

## Authentication

- AJAX-powered registration and login with no page reloads.
- Error handling and form validation for user feedback.

Example from `scripts.js`:

```javascript
$("form[name=signup_form").submit(function(e) {
    e.preventDefault();
    var formData = $(this).serialize();
    $.ajax({
        url: "/user/signup",
        type: "POST",
        data: formData,
        success: function(response) {
            console.log("Signup successful.");
        },
        error: function(error) {
            console.log("Signup failed.");
        }
    });
});
```

---

## Development Notes

- Created as part of **CS518: Introduction to Software Engineering** (Spring 2023, University of New Hampshire).
- Prioritized modularity and scalability.
- Styled using UNH’s color palette.
- Designed for both desktop and mobile experiences.

---

## How to Build & Run

1. Clone the repository:

    ```bash
    git clone https://github.com/GetBirned/FUN-H.git
    ```

2. Install dependencies:

    ```bash
    pip install Flask Flask-Login
    ```

3. Run the app:

    ```bash
    python app.py
    ```

*Note: The backend code (`app.py` and database models) may need to be configured or adapted if deploying from this version.*

---

## Contributors

- Dartagnan Birnie
- Austin Snow
- Anthony Santos
- Jason MacMillan

---

## License

This project was developed for academic purposes at the University of New Hampshire.
