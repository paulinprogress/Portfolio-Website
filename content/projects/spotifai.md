---
anchors:
- '[[Web Development]]'
- '[[Machine Learning]]'
- '[[Spotify]]'
closed: 2022-01-01
description: AI-powered web app for controlling Spotify with hand gestures
feature-image: /attachments/(2021~2022) SpotifAI - Showcase.webp
opened: 2021-01-01
project-type:
- other
- web
- ai
publish: true
thumb-image: /attachments/(2021~2022) SpotifAI - Showcase.webp
title: SpotifAI
year: '2022'
---

# SpotifAI

During the fall semester 2021/22 of my Media Technology bachelor, I took an introductory course on machine learning. It turned out to be surprisingly intuitive, providing me with tangible, first-hand experience as we implemented our own neural networks from the ground up.

“SpotifAI” was our group’s final project of the course; a web app for controlling Spotify with AI-detected hand gestures (play/pause, skip, like, and more). We went through all stages of implementation, from dataset creation and curation to model setup and training, and finally integration and deployment.

My main responsibility was setting up and training the AI model, while we all contributed to a custom dataset with lots of webcam images of different gestures. I started by implementing the image pre-processing and augmentation pipeline and creating a train/test split. Afterwards, I prepared the training script, using PyTorch to import various pre-trained convolutional neural networks (CNNs) in order to compare their performance. Ultimately, the chosen model was SqueezeNet, as it was optimised for small model size and the performance of all the models was quite similar.

Once loaded into the web app, the trained model makes inferences on the webcam stream every 0.5 seconds and executes the appropriate API call if the confidence level of a prediction is above 99.3%. This worked really well, giving us a stable and reliable working prototype.

The final web interface looked like this:

![[(2021~2022) SpotifAI - Showcase.webp]]

The experience taught me a lot and laid the groundwork for my internship and [[(2024) Bachelorarbeit (BA)|bachelor’s thesis]] in the field of AI later on.