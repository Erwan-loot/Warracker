# 🛡️ Warracker

Warracker is an open-source warranty tracker application designed to help you effortlessly keep track of product warranties, expiration dates, and related documentation.

## 🌟 Overview

Warracker is a web-based application that provides a centralized system for managing all your product warranties. Key features include:

*   Tracking product warranties in one central location.
*   Adding warranty details, including purchase dates and duration.
*   Uploading and storing warranty documentation and receipts.
*   Providing visual indicators for active, expiring soon, and expired warranties.
*   Searching through your warranty collection.

## 📸 Screenshots


![image](https://github.com/user-attachments/assets/7b343fa3-0880-48e9-8809-55a72be4d5e4)

![image](https://github.com/user-attachments/assets/0a4de195-fdcb-4dcb-87c3-e518323462ba)


## ✨ Features

*   **Warranty Management**: Add, edit, and delete warranty information.
*   **Document Storage**: Upload and securely store receipts and warranty documentation.
*   **Status Tracking**: Visual indicators for warranty status (active, expiring soon, expired).
*   **Search**: Easily find warranties by product name.
*   **Responsive Design**: A seamless experience on both desktop and mobile devices.

## 🛠️ Technology Stack

*   **Frontend**: HTML, CSS, JavaScript
*   **Backend**: Python with Flask
*   **Database**: PostgreSQL
*   **Containerization**: Docker and Docker Compose
*   **Web Server**: Nginx

## 🚀 Installation

### Prerequisites

*   Docker and Docker Compose installed on your system.
*   Git (for cloning the repository).

### Setup

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/sassanix/warracker.git
    cd warracker
    ```
2.  **Start the Application:**

    ```bash
    docker-compose up -d
    ```
3.  **Access the Application:**

    Open your browser and navigate to `http://localhost:8005`.

## 📝 Usage

### Adding a Warranty

1.  Fill in the product details on the left panel.
2.  Enter the purchase date and warranty duration.
3.  Optionally upload receipt/documentation.
4.  Click the "Add Warranty" button.

### Managing Warranties

*   Use the search box to filter warranties.
*   Click the edit icon to modify warranty details.
*   Click the delete icon to remove a warranty.

## 💻 Development

### Local Development Environment

1.  Clone the repository.
2.  Make your changes.
3.  Build and run with Docker Compose:

    ```bash
    docker-compose build
    docker-compose up -d
    ```

### Project Structure

```
warracker/
├── backend/             # Python Flask backend
│   ├── app.py           # Main application logic
│   ├── requirements.txt # Python dependencies
│   └── init.sql         # Database initialization
├── frontend/            # Web frontend
│   ├── index.html
│   ├── script.js
│   └── style.css
├── docker-compose.yml   # Docker configuration
├── Dockerfile           # Container definition
└── nginx.conf           # Web server configuration
```

## 🗺️ Roadmap

*   User authentication.
*   Email reminders for expiring warranties.
*   Settings page.
*   Status page.

## 🛠️ Troubleshooting

### Common Issues

*   **Connection Refused Error**:  Ensure all containers are running (`docker-compose ps`). Verify the backend is correctly connected to the database.
*   **Database Errors**: If schema issues arise, double-check that the database initialization script (`init.sql`) matches the expected schema in `app.py`.

## 🤝 Contributing

Contributions are welcome! We encourage you to submit a Pull Request.

1.  Fork the repository.
2.  Create your feature branch (`git checkout -b feature/amazing-feature`).
3.  Commit your changes (`git commit -m 'Add some amazing feature'`).
4.  Push to the branch (`git push origin feature/amazing-feature`).
5.  Open a Pull Request.

## 📜 License

This project is licensed under the GNU Affero General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

*   Flask
*   PostgreSQL
*   Docker
