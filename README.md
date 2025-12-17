# English Accent Classifier

[![CI](https://github.com/yourusername/english-accent-classifier/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/english-accent-classifier/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A professional tool for identifying English accents from YouTube videos using machine learning. Built with SpeechBrain and modern Python practices.

## 📽️ Demo

[![Watch the video](assets/mq3.png)](https://youtu.be/ONuoW3pODB8)

## ✨ Features

- **YouTube Integration**: Download and analyze audio from YouTube videos
- **Advanced ML Model**: Uses SpeechBrain's state-of-the-art accent classification
- **Comprehensive Results**: Detailed probability scores for all supported accents
- **Modern GUI**: Clean, responsive tkinter interface
- **Configurable**: YAML-based configuration system
- **Professional Code**: Type hints, comprehensive testing, and CI/CD

## 🎯 Supported Accents

The model supports classification of the following English accents:

- American
- Australian
- British
- Indian
- Irish
- African
- Malaysian
- New Zealand (Kiwi)
- South Atlantic
- Bermudan
- Filipino
- Chinese
- Welsh
- Singaporean

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- FFmpeg (for audio processing)

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/english-accent-classifier.git
   cd english-accent-classifier
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the package:**
   ```bash
   pip install -e .
   ```

4. **Run the application:**
   ```bash
   english-accent-classifier
   ```
   Or directly:
   ```bash
   python gui.py
   ```

### Development Installation

For development with all optional dependencies:

```bash
pip install -e .[dev]
```

## 📖 Usage

### GUI Application

Simply run the application and enter a YouTube URL. The app will:

1. Download the audio from the video
2. Convert it to WAV format
3. Analyze the accent using the ML model
4. Display detailed probability scores

### Programmatic Usage

```python
from english_accent_classifier import AccentClassifier, AudioProcessor

# Initialize components
audio_processor = AudioProcessor()
classifier = AccentClassifier()

# Process a YouTube video
wav_path = audio_processor.download_and_convert_to_wav("https://youtube.com/watch?v=example")
result_text, best_accent = classifier.classify_accent(wav_path)

print(f"Most probable accent: {best_accent}")
print(result_text)

# Clean up
audio_processor.cleanup_temp_file(wav_path)
```

## ⚙️ Configuration

The application uses a YAML configuration file located at `config/default.yaml`. You can customize:

- Audio processing settings (sample rate, temp directory)
- Model parameters (cache directory, model path)
- YouTube download options (format, quality)
- GUI appearance (fonts, colors, window size)
- Logging configuration

Example custom configuration:

```yaml
audio:
  temp_dir: "/path/to/temp"
  sample_rate: 22050

model:
  cache_dir: "/path/to/model_cache"

gui:
  width: 800
  height: 600
  font_family: "Arial"
```

## 🏗️ Architecture

### Core Components

- **`AudioProcessor`**: Handles YouTube video downloading and audio conversion
- **`AccentClassifier`**: Manages the SpeechBrain ML model for accent classification
- **`AccentClassifierGUI`**: Provides the graphical user interface
- **`Config`**: Centralized configuration management

### Project Structure

```
english-accent-classifier/
├── src/english_accent_classifier/
│   ├── __init__.py
│   ├── audio_processor.py      # Audio downloading and processing
│   ├── accent_classifier.py    # ML model wrapper
│   ├── gui.py                  # GUI application
│   ├── config.py               # Configuration management
│   └── exceptions.py           # Custom exceptions
├── config/
│   └── default.yaml           # Default configuration
├── tests/                     # Unit tests
├── scripts/                   # Utility scripts
├── assets/                    # Static assets (images, etc.)
├── docs/                      # Documentation
├── pyproject.toml            # Modern Python packaging
└── requirements.txt          # Dependencies
```

## 🧪 Testing

Run the test suite:

```bash
python -m pytest tests/ -v
```

Run with coverage:

```bash
python -m pytest tests/ --cov=english_accent_classifier --cov-report=html
```

## 🔧 Development

### Code Quality

The project uses several tools to maintain code quality:

- **Black**: Code formatting
- **isort**: Import sorting
- **mypy**: Type checking
- **pylint**: Code linting

Run all quality checks:

```bash
black src/ tests/
isort src/ tests/
mypy src/
pylint src/
```

### Model Details

**Current Implementation**: SpeechBrain's `Jzuluaga/accent-id-commonaccent_ecapa` model
- Fast inference on CPU
- Pre-trained on diverse English accent data
- Reasonable accuracy for most use cases

**Performance Characteristics**:
- Model size: ~50MB
- Inference time: ~2-5 seconds per audio sample
- Memory usage: ~1GB RAM during inference

### Limitations & Future Improvements

#### Current Limitations

1. **YouTube Only**: Currently only supports YouTube URLs
2. **Model Accuracy**: Confidence scores can vary based on audio quality and speaker clarity
3. **Resource Usage**: Requires decent CPU/GPU for model inference

#### Potential Improvements

1. **Enhanced Model**: Fine-tune on larger datasets (Wav2Vec + Mozilla Common Voice)
   - Pros: Higher accuracy, more robust
   - Cons: Requires significant compute resources (80GB+ dataset)

2. **Streaming Approach**: Use distilled models with streaming data loading
   - Good balance of performance vs. resource usage

3. **Additional Platforms**: Support for Vimeo, TikTok, local files

4. **Real-time Processing**: Live audio stream analysis

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

If you encounter issues or have questions:

1. Check the [Issues](https://github.com/yourusername/english-accent-classifier/issues) page
2. Create a new issue with detailed information
3. Include error messages, Python version, and steps to reproduce

## 🙏 Acknowledgments

- [SpeechBrain](https://speechbrain.github.io/) for the accent classification model
- [Jzuluaga](https://github.com/Jzuluaga) for the pre-trained model
- [PyTorch](https://pytorch.org/) for the deep learning framework
- YouTube community for providing diverse accent samples
