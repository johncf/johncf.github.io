Title: Practical Advice on Attentional Mechanism

If you're new to the concept of attention, then I highly recommend reading the "Attentional Interfaces" section of [this article][distill] first.

[distill]: https://distill.pub/2016/augmented-rnns/

Here's a diagramatic representation of an attention layer:

![Attention Layer]({attach}diags/attn.svg)

This is usually part of an encoder-decoder model such as:

\[diagram]

With that in mind, this is my advice:

> Do _not_ use RNNs in the encoder part. Use CNNs or nothing at all.

Disclaimer: What I discuss below is simply a hypothesis that could explain some of my experimental results. Therefore, my "assertions" below should only be considered "guesses." If you have a better explanation, then please discuss it in comments.

RNN: Good for maintaining long-distant relationships. Here, the "rememberence" of past information is dependent on the state and inputs.
CNN: Good for "uniform" dissemination of information. Here, since there's no "state," the degree of information dissemination is dependent only on the inputs and will therefore have a more "predictable" pattern.

To effectively train an attention mechanism, the memory units need to have more-or-less uniform distribution of information.
