# Qalk - File Transfer Client/Server Project

## Overview

Qalk is a simple client-server file transfer application using Python sockets. It supports:

- Viewing server directory (`LIST`)
- Downloading single or multiple files with chunking (`GET`)
- Navigating server directories (`CD`, `PWD`)
- Viewing directory listings with folders highlighted
- Environment configuration via `.env` file

---

## Project Structure

```
qalk/
├── .env                # Server host and port settings
├── .gitignore
├── requirements.txt    # Python dependencies
├── README.md
├── server/
│   └── main.py         # Server implementation
└── client/
    └── main.py         # Client implementation
```

---

## Setup Instructions

### 1. Clone the repository and navigate to `qalk/`:
```bash
cd qalk
```

### 2. Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Configure the `.env` file:
```env
SERVER_HOST=localhost
SERVER_PORT=5001
```

---

## Usage

### Start the Server
```bash
python server/main.py
```

### Start the Client
```bash
python client/main.py
```

### Available Client Commands

- `LIST` — list files and folders on the server
- `GET file1.txt file2.zip` — download one or more files
- `CD foldername` — change server directory
- `PWD` — print current server directory
- `QUIT` — disconnect

---

## Notes

- Files are transferred in 1MB chunks.
- Folders are shown in **bold blue** in directory listings.
- Downloads are saved to client/download at default.

---

## License

MIT License


