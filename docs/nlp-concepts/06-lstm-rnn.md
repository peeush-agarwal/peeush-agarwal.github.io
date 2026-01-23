# Long Short-Term Memory (LSTM) RNNs

Long Short-Term Memory (LSTM) networks are a specialized type of Recurrent Neural Network (RNN) designed to effectively capture long-term dependencies in sequential data. They were introduced by Hochreiter and Schmidhuber in 1997 to address the limitations of traditional RNNs, particularly the vanishing gradient problem that hampers learning over long sequences.

## Key Components of LSTMs

LSTMs consist of memory cells and three primary gates that regulate the flow of information:
1. **Forget Gate**: Decides what information from the previous cell state should be discarded. It takes the previous hidden state and the current input, applies a sigmoid activation function, and outputs a value between 0 and 1 for each number in the cell state.
2. **Input Gate**: Determines which new information should be added to the cell state. It consists of a sigmoid layer that decides which values to update and a tanh layer that creates new candidate values to be added to the cell state.
3. **Output Gate**: Controls what information from the cell state should be output as the hidden state. It uses a sigmoid function to decide which parts of the cell state to output and applies a tanh function to scale the cell state values.

## How LSTMs Work?

At each time step, the LSTM processes the input data along with the previous hidden state and cell state. The gates work together to update the cell state and produce the new hidden state. The process can be summarized as follows:
- **Forget Gate**: $f_t = \sigma(W_f \cdot [h_{t-1}, x_t] + b_f)$
- **Input Gate**: $i_t = \sigma(W_i \cdot [h_{t-1}, x_t] + b_i)$
- **Candidate Values**: $\tilde{C}_t = \tanh(W_C \cdot [h_{t-1}, x_t] + b_C)$
- **Cell State Update**: $C_t = f_t * C_{t-1} + i_t * \tilde{C}_t$
- **Output Gate**: $o_t = \sigma(W_o \cdot [h_{t-1}, x_t] + b_o)$
- **Hidden State Update**: $h_t = o_t * \tanh(C_t)$

Where:
- $x_t$ is the input at time step t.
- $h_{t-1}$ is the previous hidden state.
- $C_{t-1}$ is the previous cell state.
- $W_f$, $W_i$, $W_C$, and $W_o$ are weight matrices.
- $b_f$, $b_i$, $b_C$, and $b_o$ are bias vectors.

## Applications of LSTMs in NLP

LSTMs have been widely used in various NLP tasks due to their ability to capture long-term dependencies. Some common applications include:
- **Language Modeling**: Predicting the next word in a sequence based on the context of previous words.
- **Text Generation**: Generating coherent and contextually relevant text by sampling from the learned language model.
- **Machine Translation**: Translating text from one language to another by encoding the source language and decoding it into the target language.
- **Speech Recognition**: Converting spoken language into text by modeling the temporal dependencies in audio signals.
- **Sentiment Analysis**: Classifying the sentiment of a piece of text (e.g., positive, negative, neutral) by understanding the context over long sequences.

## Advantages of LSTMs

- **Long-Term Dependency Capture**: LSTMs are effective at learning long-term dependencies in sequential data, making them suitable for tasks where context is crucial.
- **Mitigation of Vanishing Gradient Problem**: The gating mechanisms in LSTMs help mitigate the vanishing gradient problem, allowing for more stable training over long sequences.
- **Flexibility**: LSTMs can be adapted for various sequence lengths and types of data, making them versatile for different NLP applications.

## Good to read

- [Understanding LSTMs](https://colah.github.io/posts/2015-08-Understanding-LSTMs/)

---

[<< Recurrent Neural Networks (RNNs)](05-recurrent-neural-networks.md)

[Back to NLP Concepts](index.md) | [Back to Home](../index.md)
