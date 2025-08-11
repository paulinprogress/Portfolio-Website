---
anchors:
- '[[Machine Learning]]'
- '[[Deep Learning]]'
- '[[Generative Modelle]]'
- '[[Synthetische Daten]]'
- '[[Contrastive Learning]]'
image: /images/attachments/(2024, BA) Flowchart Versuchsaufbau.png
project-type:
- other
publish: true
title: Bachelor's thesis
year: '2024'
---

# Bachelor’s thesis

The title for my bachelor’s thesis has quite an intimidating title:

>“[[Contrastive Learning]] with [[Stable Diffusion]]-based [[Datenaugmentation|Data Augmentation]] – Improvement of [[Bildklassifikation|Image Classification]] with [[Synthetische Daten|Synthetic Data]]”

I’ll have to explain a little bit…

During my Media Technology studies, I discovered an interest in Machine Learning after taking an introductory course. I found it surprisingly intuitive and hands-on – in one project, two classmates and I built a web app that connected to Spotify and let you control it with hand gestures via your webcam.

When the time came to do my student internship, I landed a spot at Berlin’s [Fraunhofer Institute for Production Systems and Design Technology](https://www.ipk.fraunhofer.de/en.html), working on a computer vision research project for the recycling industry. The goal was to improve a classier for identifying used parts. Specifically, my job was to explore different methods for synthetic data generation using generative AI – i.e. generating new images to be used for training the classifier, in order to increase data variety, especially for different object conditions, wear & tear, etc.

I made some decent progress, but took away a key learning: It’s *really* hard to generate realistic images – let alone with meaningful variations – of such detailed objects, with such fine-grained classes, and with such limited examples per class.

Using the [[Text-to-Image-Personalisierung|text-to-image customization]] framework *[[Perfusion]]*, this was the best I could get:

![[(2024, @IPK) Perfusion - Bestes Ergebnis (Testing, rostig).png]]

Afterwards, it only made sense to write my bachelor’s thesis there too, about the same project. After lots of further research, two topics stood out to me as particularly promising for the given use case:

1. [[DA-Fusion]]: A Stable Diffusion-based method for data augmentation, which takes images of your new object classes and automatically generates semantically meaningful variations of it – all without having to fine-tune the actual diffusion model with tons of new data.
2. [[Contrastive Learning]]: A method for learning representations of input data, which can then be used for classification. This was interesting, because it learns by comparing “positive” and “negative” examples, which gave me an idea: *Can I use sub-optimal synthetic data as negative examples and thereby increase model performance after all?*

This led to an experiment in which I would train a Supervised Contrastive Learning classifier and compare it’s accuracy as well as Out-of-Distribution Detection across three different training setups:

1) With only real data,
2) With “normal” augmentations from DA-Fusion as synthetic data, and
3) With additional “bad” augmentations from DA-Fusion, only ever used as negative examples.

In short: the _good_ augmentations improved performance, but the _bad_ ones didn’t. Likely, the out-of-distribution samples were too far from the real ones to challenge the model in a meaningful way.

Here are some of the *in-distribution* augmentations:

![[(2024, BA) Vergrößerte Ausschnitte von einigen der In-Distribution-Augmentationen (2).png]]

![[(2024, BA) Beispiele der In-Distribution-Augmentationen.png]]

Here some of the *out-of-distribution* ones:

![[(2024, BA) Beispiele der Near Out-of-Distribution-Augmentationen (2).png]]

And here some of the bad out-of-distribution ones:

![[(2024, BA) Beispiele für mangelhafte Out-of-Distribution-Augmentationen (2).png]]

For implementation details, the code is available on [GitHub](https://github.com/paulinprogress/BA-Synthetic-Data).