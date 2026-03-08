---
anchors:
- '[[Software Development]]'
- '[[Programmierung]]'
- '[[Prototyping]]'
- '[[C-Sharp|C#]]'
- '[[Dot NET|.NET]]'
- '[[Avalonia]]'
closed: 2026-03-05
description: A simple Kanban board demo project, built with .NET (C#) using the Avalonia
  UI framework
feature-image: /attachments/(2026) Avalonia Kanban Demo (Feature).webp
opened: 2026-02-12
project-type:
- other
publish: true
thumb-image: /attachments/(2026) Avalonia Kanban Demo (Thumb).webp
title: Avalonia Kanban Demo
year: '2026'
---

# Avalonia Demo Project: Kanban Board

A lightweight Kanban board application built as a demo/test project using [Avalonia](https://avaloniaui.net/) (11.3.11), a cross-platform .NET UI framework.

![[(2026) Avalonia Kanban Demo (Feature).webp]]

Besides getting a first-hand look at the Avalonia UI framework, I also started this side project to get more familiar with .NET – coming from game development in Unity with C#, I thought it would be a good way to expand my skillset for cross-platform desktop app development.

I also got to learn a lot about Model-View-ViewModel (MVVM) architecture in the process, due to how Avalonia is set up by default. Even though the end result was pretty simple, I had to play around with a number of Avalonia's features, from implementing light/dark theme modes to dynamically generating elements with `ItemsControl` and using data binding for various visibility/command functions.

One of the trickier things was getting the drag-and-drop functionality for the tasks to work. This is also where Avalonia's documentation left me a little confused for a while. But I stayed patient and went over everything step-by-step, and eventually got it working exactly how I wanted, which made it all the more satisfying!

The whole project & source code is available on [GitHub](https://github.com/paulinprogress/Avalonia-Demo-Kanban).