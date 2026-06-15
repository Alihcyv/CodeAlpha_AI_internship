# Generative Music Composition using LSTM

This project implements a Deep Learning model capable of composing music in the style of Frédéric Chopin. Using a Long Short-Term Memory (LSTM) network, the model learns the complex patterns of notes and chords from MIDI files to generate new, original musical sequences.

## Project Overview

The goal of this project is to bridge the gap between music theory and artificial intelligence. By treating music as a sequence of tokens (similar to Natural Language Processing), the model predicts the next note or chord based on a sliding window of previous musical events.

## Technical Architecture

The model uses a sophisticated architecture to handle the nuances of classical music:

- **Data Preprocessing**: 
  - MIDI parsing using `music21`.
  - Feature extraction: converting music into a sequence of note pitches and chord normal orders.
  - Tokenization: mapping musical events to integers.
- **Neural Network Design**:
  - **Embedding Layer**: Transforms note indices into dense vectors, capturing harmonic relationships between notes.
  - **LayerNormalization**: Stabilizes the learning process and prevents gradient explosion.
  - **Stacked LSTMs**: Captures long-term dependencies and structural patterns in the music.
  - **Dropout**: Regularization to prevent overfitting and ensure the model generalizes rather than memorizing.
  - **Softmax Output**: Predicts the probability distribution of the next musical token.

## Results & Evaluation

The model was trained on a corpus of Chopin's MIDI files. 
- **Accuracy**: Achieved a significant increase in validation accuracy by implementing Embedding layers and LayerNormalization.
- **Generalization**: Use of `EarlyStopping` and to ensure the model learns the style without overfitting (memorizing) the training set.
