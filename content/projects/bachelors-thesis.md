---
anchors:
- '[[Machine Learning]]'
- '[[Deep Learning]]'
- '[[Generative Modelle]]'
- '[[Synthetische Daten]]'
- '[[Contrastive Learning]]'
closed: 2024-12-02
description: Using generative AI for synthetic data generation in an industrial context
feature-image: /attachments/(2024, BA) EIBA Setup.webp
opened: 2024-03-09
project-type:
- other
- ai
publish: true
thumb-image: /attachments/(2024, BA) EIBA Setup.webp
title: Bachelor's thesis
year: '2024'
---

# Bachelor’s thesis

Looking back, my 2024 bachelor’s thesis has quite an intimidating title:

>*“Contrastive Learning with Stable Diffusion-based Data Augmentation – Improvement of Image Classification with Synthetic Data”*

I’ll have to explain a little bit…

During my Media Technology studies, I discovered an interest in machine learning after taking an introductory course. I enjoyed how quickly we could get hands-on experience; in one project, two classmates and I built a web app that connected to Spotify and let you control it with hand gestures via your webcam (see: [[(2021~2022) SpotifAI|SpotifAI]]).

So when the time came to do my student internship, I landed a spot at Berlin’s [Fraunhofer Institute for Production Systems and Design Technology](https://www.ipk.fraunhofer.de/en.html), working on a computer vision research project for the recycling industry. The goal was to improve a classier for identifying used parts. Specifically, my job was to explore different methods for *synthetic data generation using generative AI* – i.e. generating new images to be used for training the classifier, in order to increase data variety, especially for different object conditions, wear & tear, etc.

The internship was super fun and I made some decent progress, but took away a key learning: It’s *really* hard to generate realistic images – let alone with meaningful variations – of such detailed objects, with such fine-grained classes, and with such limited examples per class.

Using the text-to-image personalization framework [Perfusion](https://research.nvidia.com/labs/par/Perfusion/), this was the best I could do:

![[(2024, @IPK) Perfusion - Bestes Ergebnis (Testing, rostig).webp]]

Despite the challenges – or maybe because of them – it only made sense to write my bachelor’s thesis on the same project. After lots of further research, two topics stood out to me as particularly promising for the given use case:

1. DA-Fusion: A Stable Diffusion-based method for data augmentation, which takes images of your new object classes and automatically generates semantically meaningful variations of it – all without having to fine-tune the actual diffusion model with tons of new examples per class (instead, it fine-tunes a *token* that describes your new class, leveraging all the existing knowledge of the pre-trained model).
2. Contrastive Learning: A method for learning representations of input data, so that similar samples are close together in the representation space and dissimilar examples further apart. This was interesting, because it learns by comparing “positive” and “negative” examples, which gave me an idea: Can I use *sub-optimal* synthetic data *only* as negative examples and thereby increase model performance after all?

This led to an experiment in which I trained a Supervised Contrastive Learning classifier and compared it’s accuracy as well as out-of-distribution detection across three different training setups:

1. Using only real data,
2. Using “normal” augmentations from DA-Fusion as synthetic data, and
3. Using additional “bad” augmentations from DA-Fusion, but only as negative examples.

In short: The _good_ augmentations improved performance, but the _bad_ ones didn’t.

The bad samples (which were supposed to be “near out-of-distribution”) were most likely *too* far from the real ones to challenge the model in a meaningful way. The good ones (which acted as “in-distribution” samples) did improve performance, but were notably *very* subtle in their variations.

Here are some of the *in-distribution* augmentations:

![[(2024, BA) Vergrößerte Ausschnitte von einigen der In-Distribution-Augmentationen (2).webp]]

![[(2024, BA) Beispiele der In-Distribution-Augmentationen.webp]]

Here some of the *near out-of-distribution* augmentations:

![[(2024, BA) Beispiele der Near Out-of-Distribution-Augmentationen (2).webp]]

And here some of the *far out-of-distribution* augmentations, which clearly turned out to be way too dissimilar to the in-distribution classes:

![[(2024, BA) Beispiele für mangelhafte Out-of-Distribution-Augmentationen (2).webp]]

Either way, the project taught me a *ton* about practical ML implementation (especially since I had to re-engineer the contrastive loss function), as well as research methodology and data analysis.

For implementation details, the code is available on [GitHub](https://github.com/paulinprogress/BA-Synthetic-Data).