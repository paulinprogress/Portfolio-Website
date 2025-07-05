---
anchors:
- '[[Game Jams]]'
- '[[Game Development]]'
- '[[Game Design]]'
- '[[Game Programmierung]]'
- '[[Prototyping]]'
- '[[Unity]]'
closed: '[[2025-03-20]]'
date: '2025-07-04T11:51:04.193541'
opened: '[[2025-03-13]]'
publish: true
spaces:
- '[[@G&G]]'
title: (2025) Last Block Standing (PULS GAME JAM)
year: '2025'
---

%%Key features:

- Random projectile spawner with increasing difficulty
- Grid-snapping wall placement
- 8-directional player movement & sprite animation handling%%
# [PULS GAME JAM](https://itch.io/jam/puls-game-jam)

Start: [[2025-03-14]], 19:00 Uhr
Ende: [[2025-03-16]], 19:00 Uhr

Theme: *Kaputt*

## Idee

- Super simples Top-Down 2D game in [[Pixel Art]]
- Man spawnt auf einer kleinen Platform, umzingelt von Mauern
- Außerhalb der Platform (Void) kommen aus zufälligen Richtungen kleine Projectiles, die bei Kontakt mit den Mauer-Blöcken Schaden anrichten & diese schließlich ganz zerstören – wodurch sie zum Spieler gelangen und ihn eliminieren können
- Während des Spiels spawnen kleine Pick-ups, mit denen man neue Mauern platzieren kann
- Die Menge an Projectiles steigt stetig, wodurch es immer mehr ums ausweichen geht, und um gute Platzierungen der Mauern
- Im Prinzip: Endless-Spielmodus mit Highscore

## Umsetzung

- [x] Erste [[Game Art|Art Assets]] zusammensuchen
	- [x] Plattform
	- [x] Player (von 4 Seiten)
		- [x] Idle
		- [x] Walking
		- [x] Dying
	- [x] Walls
		- [x] Normal
		- [x] Geschädigt
	- [-] Projectiles
	- [-] UI
- [x] [[Game Programmierung]]
	- [x] Gameplay basics
		- [x] Platform tilegrid
		- [x] Player movement & animation
		- [x] Wall prefab with damage
		- [x] Projectile prefab
		- [x] Game manager with continuous projectile spawning, increasing speed
		- [x] Player hit & game over
		- [x] Wall placing mechanic with highlighting
		- [x] Wall pickup with timed respawn after picking up
		- [x] Limit movement to platform
	- [x] Score
		- [x] Timer display
		- [-] Highscore display
	- [x] Intro animation
		- [x] Camera zoom-in
		- [-] Audio cue
		- [-] Show controls
	- [x] Game Over animation
		- [x] Death animation
		- [-] Audio cue
		- [-] Text
	- [x] Small fixes & improvements
		- [x] Make sure wall pickups don’t respawn until wall has been placed
		- [x] Make sure wall pickups don’t spawn into walls
		- [x] Make sure you can’t place walls inside other walls
		- [x] Fade in timer text
- [x] Polishing
	- [-] Flat shapes with pixelate shader?
	- [x] Better art for projectiles
	- [x] Pixel font for timer
	- [-] Audio

## Submission

==[Last Block Standing](https://ghostsnglitter.itch.io/protect-the-walls)== ([GitHub-Repo](https://github.com/PaulToast/Last-Block-Standing))

![[Last Block Standing.png]]

Assets:

- **Tileset:** _Pattern Pack Pixel 16x16_ from [Kenney](https://kenney.nl/assets/1-bit-input-prompts-pixel-16) _(CC0)_
- **Character Sprite:** _Top-Down Prototype Character_ by [Snoblin](https://snoblin.itch.io/pixel-rpg-free-npc) (Used under creator's license)
- **Font:** _Pixelify Sans_ from [Google Fonts](https://fonts.google.com/specimen/Pixelify+Sans) _(SIL Open Font License 1.1)_

## Retro

- Allgemein:
	- War erstmal etwas deprimierend: trotzdem ich nach ein wenig Brainstorming eine gute, überschaubare, *sehr* simple Idee gefunden habe, habe ich *echt* sehr damit gekämpft, sie umzusetzen – sowohl aus programmiertechnischen als auch aus zeitlichen Gründen. Dabei kamen immer weitere kleine To-dos hinzu, die ich vorher überhaupt nicht im Kopf hatte (inkl. der Erstellung einer halbwegs anschaulichen Projektseite auf Itch.io). Es war also gewissermaßen eine ziemlich demütigende Erfahrung.
	- Aber: Ich habe mich durchgekämpft, weitergemacht, und hatte am Ende dann *doch* noch Zeit ein paar Kleinigkeiten zu fixen und zu verbessern – auch wenn vieles wie Audio gestrichen werden musste
	- Sofort nach Einreichung wurde mir das Ganze dann als totales Erfolgserlebnis klar; Ja, es war stressig und etwas demütigend, aber auch eine sehr intensive Lernerfahrung. Ich war gezwungen, *wirklich* einmal alles von vorne bis hinten durchzugehen. Genau diese Art von Herausforderung stellt meinen [[Perfektionismus]] richtig auf die Probe und bringt mich tatsächlich vorran, wenn es darum geht, meine [[Effektivität]] als Spieleentwickler zu trainieren und die kreative [[Closing the gap|“gap”]] zu schließen.
- Im Detail:
	- [[GitHub Copilot]] ([[Künstliche Intelligenz|KI]]-Unterstützung beim [[Game Programmierung|Coden]]) hat mir wirklich enorm geholfen… Ich will dem Vormarsch von KI-Tools nicht unkritisch gegenüberstehen, aber muss eingestehen, dass ich den massiven Widerstand im Bereich Code nicht ganz verstehen kann. Die [[Datenschutz]]-Problematik erschließt sich mir noch nicht zu 100%, möchte ich mir aber nochmal genauer anschauen…
	- UI/Menus, [[Tutorialization]], etc. in diesem Fall komplett ignoriert, ist aber ein *ziemlich* umfangreicheres Aufgabenpaket, das man einfach vergessen kann – ist aber für Polishing usw. natürlich nicht trivial
	- Auch für Sound Design blieb hier gar keine Zeit; Könnte einiges einfacher machen, wenn man dafür Leute in einem Team hat
	- ==Obsidian-Template erstellen:== [[(+) projects (Game Jam)]]
	- Ich möchte auch unbedingt anfangen, eine ==[[Game Art|Asset]]-Library zu erstellen==, vor allem für einfache, free-to-use Assets, um schneller loslegen zu können

## Post-Submission

(Small update, just to round things off)

- [x] Update repository name to “Last Block Standing”
- [x] Make block respawns more frequent, especially as time goes on
- [x] Place blocks on grid?
- [-] Add some basic sounds?