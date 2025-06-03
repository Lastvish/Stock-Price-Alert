# Stock Price Alert System

A real-time US stock monitoring system based on Finnhub API, supporting real-time price monitoring and custom alerts for stocks and indices.

## Features

- Real-time stock price monitoring (using WebSocket)
- Periodic index data monitoring (using REST API)
- Custom price change threshold alerts
- Custom percentage change threshold alerts
- Support for custom alert sounds
- Complete market status checking
- Error handling and automatic reconnection mechanism

## Technical Implementation

- Uses Finnhub WebSocket API for real-time stock price monitoring
- Uses Finnhub REST API for index data monitoring
- Supports custom monitoring parameters via configuration file
- Built-in market trading hours check
- Comprehensive error handling mechanism

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Lastvish/Stock-Price-Alert.git
cd Stock-Price-Alert
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configuration:
- Copy the configuration file template:
```bash
cp config/config.example.yaml config/config.yaml
```
- Edit `config/config.yaml` to set your Finnhub API key and monitoring parameters

## Configuration Guide

The configuration file (config.yaml) contains the following main parameters:

- `api_key`: Finnhub API key
- `symbols`: List of stock symbols to monitor
- `indices`: List of indices to monitor
- `thresholds`:
  - `price`: Price change threshold (USD)
  - `percentage`: Percentage change threshold
- `update_interval`: Data update interval (seconds)
- `sound`: Alert sound settings

## Usage

1. Ensure `config.yaml` is properly configured
2. Run the program:
```bash
python src/monitor.py
```

## Important Notes

- Make sure you have a valid Finnhub API key
- It's recommended to run the program during US market trading hours
- Be aware of Finnhub API usage limits
- Adjust alert thresholds according to your needs

## License

MIT License

## Author

Lastvish

## Contributing

<<<<<<< HEAD
Issues and Pull Requests are welcome! 
=======
欢迎提交 Issue 和 Pull Request！ 
>>>>>>> 2bc24489f76dac2514f6cd473a6a60879054ffdd
