# Matcha

## Project Overview

**Matcha** is a web application prototype designed to explore the concept of industrializing love through technology. The project aims to create a platform where users can connect, interact, and build relationships in a structured and engaging way. It leverages Flask, a lightweight Python web framework, to implement core functionalities such as user registration, profile management, chat systems, and notifications.

The project is currently **on hiatus**, meaning active development has been paused. However, the repository remains available for educational purposes and as a reference for web application development using Flask.

This project was initially developed in collaboration with my peer [github.com/beatriangu](https://github.com/beatriangu). You can find a completed solo fork of this project at [Matchito](https://github.com/beatriangu/Matchito).

## Structure

The repository is organized as follows:

### 1. **Core Components**
   - **`srcs/flask/blueprints/`**: Contains modular blueprints for features like user management, chat, notifications, and profile handling.
   - **`srcs/flask/manager/`**: Includes logic for managing core functionalities such as chats, interests, likes, and notifications.
   - **`srcs/flask/models/`**: Defines database models for storing user data and application state.
   - **`srcs/flask/templates/`**: HTML templates for rendering pages like login, registration, and email verification.
   - **`srcs/flask/static/`**: Static assets such as CSS files for styling the application.

### 2. **Supporting Files**
   - **`docker-compose.yml`**: Configuration for containerized deployment using Docker.
   - **`Makefile`**: Automates common tasks such as running the application and managing dependencies.
   - **`requirements/`**: Lists Python dependencies required for the project.

### 3. **Testing**
   - **`srcs/flask/tests/`**: Contains unit tests for validating application functionality, including user management and API endpoints.

## Competencies Developed

By working on this project, participants can develop the following skills:

- **Web Development**: Learn how to build web applications using Flask and integrate frontend technologies like HTML and CSS.
- **Python Programming**: Gain experience in writing Python scripts for backend logic and API development.
- **Database Management**: Understand how to design and interact with databases using Flask models.
- **Modular Design**: Explore the use of blueprints to structure large applications into manageable components.
- **Testing and Debugging**: Write unit tests to ensure application reliability and debug issues effectively.
- **Containerization**: Learn how to use Docker for deploying web applications in a containerized environment.

## How to Use This Repository

1. Clone the repository to your local machine:
   ```bash
   git clone <repository-url>
   ```
2. Install dependencies using `pip`:
   ```bash
   pip install -r requirements/app.txt
   ```
3. Run the application locally:
   ```bash
   python srcs/flask/run.py
   ```
4. Optionally, use Docker for containerized deployment:
   ```bash
   docker-compose up
   ```

## Notes

- The project is currently **on hiatus**, and some features may be incomplete or require further refinement.


## Conclusion

**Matcha** is a creative exploration of web application development, showcasing the potential of Flask for building modular and scalable platforms. While the project is on hiatus, it serves as a valuable resource for learning and experimentation in web development.

Feel free to explore the codebase and adapt it for your own projects!