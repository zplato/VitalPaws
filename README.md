# VitalPaws

**VitalPaws** is a smartphone application designed to monitor and analyze your pet's respiratory rate using your handheld device. By leveraging embedded sensors and signal processing techniques, VitalPaws offers a non-invasive solution to track your pet's breathing patterns, aiding in early detection of potential health issues.

## Features

- Mobile application with a user-friendly interface developed using Vue.js.
- Uses your smartphone's sensors and analyze your pet's breathing.
- Python-based backend processes data to extract respiratory rates.
- Provides real-time feedback on your pet's respiratory patterns.
- Maintains a history of respiratory data to monitor trends over time.

## Technologies Used

- **Frontend**: Vue.js, JavaScript, HTML, CSS
- **Backend**: Python
- **Others**: MIT License

## Installation

### Prerequisites

- Node.js and npm installed on your machine
- Python 3.x installed

### Frontend Setup

1. Navigate to the `frontend` directory:

   ```bash
   cd frontend
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Run the development server:

   ```bash
   npm run serve
   ```

### Backend Setup

1. Navigate to the `backend` directory:

   ```bash
   cd backend
   ```

2. Create and activate a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the backend server:

   ```bash
   python app.py
   ```

## Usage

1. Launch the frontend application in your browser (usually at `http://localhost:8080/`).
2. Use the interface to start a new respiratory monitoring session.
3. Follow on-screen instructions to position your pet and begin recording.
4. View real-time analysis and historical data within the app.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

