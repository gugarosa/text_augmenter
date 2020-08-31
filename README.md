# Text Augmenter: A Lecture on Text-based Augmentation

Text Augmenter provides a thorough lecture on text-based augmentation techniques to be given at ICMC/USP mini-course. Apart from the lecture itself, we also implemented a wide variety of tasks to illustrate how one can use such tools in real-world applications.

---

## Guidelines

1. Every needed piece of information is elucidated in this **README**;
2. **Installation** is also straightforward and well-explained;
3. If there is a problem, please do not **hesitate** and call us.

---

## Installation

The installation process is straightforward as the dependencies are listed on the `requirements.txt` file. One can install them under the most preferred Python environment (raw, conda, virtualenv):

```bash
pip install -r requirements.txt
```

Additionally, the source files for the lecture are presented in LaTeX. Thus, one might need an additional compiler or even Overleaf to build the files into a PDF file.

---

## Getting Started

This section provides an overview of the text augmentation lecture, as well as three text augmentation applications.

### Lecture

The lecture is written in Portuguese in a slide-based format. The contents are available at the `slides` folder and can be compiled to PDF using a LaTeX compiler.

### Causal Language Generation

Causal language generation stands for the task of predicting a `t+1` timestep given `t` timesteps, e.g., predict a word given a sequence of words. Such applications are implemented and available at the `applications/causal` folder.

### Masked Language Generation

Masked language generation is the task of predicting a masked token given a sequence of tokens, e.g., predict a word given its surrounding context. This application is implemented and available at the `applications/masked` folder.

### Language Generation Bot

The bot code is available at the `applications/bot` folder and is composed of two scripts: `bot.py` and `api.py`. The `bot.py` stands for a straightforward implementation using the python-telegram-bot and provides a simple user interaction, while the `api.py` implements a one-handler API using tornado, which encodes the text generation task.

---

## Support

It is inevitable to make mistakes or create some bugs. If there is any problem or concern, we will be available at this repository or gustavo.rosa@unesp.br.

---
