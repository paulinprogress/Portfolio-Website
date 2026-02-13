---
anchors:
- '[[Game Development]]'
- '[[Game Jams]]'
- '[[Prototyping]]'
- '[[Arcade]]'
- '[[Retro Ästhetik]]'
- '[[PS1 Ästhetik]]'
closed: 2025-11-23
description: An arcady flying game with a challenge-based gameplay loop
feature-image: /attachments/(2025) JetQuest (Feature).webp
opened: 2025-11-16
project-type:
- game
- game-jam
publish: true
thumb-image: /attachments/(2025) JetQuest (Thumb).webp
title: JetQuest
year: '2025'
---

# JetQuest

This was a collaboration with [JustinGonsalves](https://justingonsalves.itch.io/) created in one week for [Jame Gam #55](https://itch.io/jam/jame-gam-55), built around the themes “Mobility” and “Gorge”.

We opted for a fun, arcady flying game with a retro look, focused on risky, mobility-driven challenges set in a canyon environment. You complete challenges to earn points and unlock new spaceships. Along the way, you can collect pickups for bonus points or fuel, but you must land before running out of fuel in order to stash your points, select new challenges, or upgrade your ship.

![[(2025) JetQuest (Challenge Selection).webm]]

After we settled on the general idea early on, we began by adopting a simple airplane controller, scripting the challenge system and building the level. In particular, I got familiar with the Unity’s Terrain tool, as well as Scriptable Objects for neatly organizing and handling the data for different ships and challenges.

Once many of the individual elements for the game were prototyped, I got deeply involved with integrating and finalizing all of them to get the complete game loop running:

- **Challenge system:** Each challenge type checks for different conditions in order to calculate the progress of the challenge and whether it has been completed. If it is has and the player lands, the new challenge selection panel is activated. If it is uncompleted and the player crashes, the progress gets reset.
- **Points system:** Player receives points for the active challenges, points get stashed when landing (or lost when crashing), and everything is synced with the UI.
- **Ship upgrades & win condition:** When landed, an option appears for the player to upgrade their ship, if they have enough points. For this, I had to implement the logic for loading the different ships’ Scriptable Objects and applying their values to the player controller. Finally, after the player has upgraded twice and collected enough points with the third ship, the “win game” button appears instead.
- **Visuals:** After finalizing the overall level design, I added a PSX-style retro shader for the terrain and objects, a fitting skybox asset that I color-adjusted to the level, and I implemented a simple pixelation effect with Shader Graph.
- **Polish:** I spend a lot of time on polishing various elements of the experience – designing the UI and menus, finding fonts, adding music, etc. The level of polish was pointed out a lot as a positive in feedback from players.
- **Further game design:** Later in the project, I got the idea of adding fuel & points pickups that spawn randomly throughout the level, which ended up adding much needed variety to the game flow and encouraged more exploration of the level space. I was also able to fit the visuals of the pickups to the retro aesthetic (colorized and slightly transparent, easily distinguishable shapes, rotating and “pulsating” for an extra retro feel).

Our entry landed the 1st spot in theme implementation and 6th overall, making it a pretty rewarding outcome for us! Following some of the feedback we got, I also experimented with an option to lock the camera, although I find it a bit nauseating… (see below)

![[(2025) JetQuest (Mouse Lock).webm]]

You can play JetQuest on [Itch.io](https://paultoast.itch.io/jetquest).