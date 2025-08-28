---
title:       "Wanna play an iterated prisoner's dilemma tournament between ChatGPT, Claude, Gemini, and humans?"
one_liner:   "How will we do against the LLMs in this classic game of cooperation and betrayal?"
author:      me
image:       ''
link:        https://buster.substack.com/p/wanna-play-an-iterated-prisoners
redirect:    true
---

If you're unfamiliar with Prisoner's Dilemma or feel like you need a refresher, this video from Veritasium from last year does a good job of introducing the game, as well as explaining why I think it's such an interesting little microcosm of how we behave in the world and a game that is capable of teaching us so much:

{% youtube "https://www.youtube.com/watch?v=mScpHTIi-kM" %}

I’ve hosted a few “team-based iterated prisoner’s dilemma” games on Facebook over the years. There are usually 15-25 people split up into two to four teams, and the goal is for the people to discuss ways to beat the other team in a round-robin style format where every player is matched up with every player on the other teams.

So if Team Ant has 5 people and Team Beetle has 5 people, then everyone on Team Ant plays 100 matches against everyone on Team Beetle and vice versa. If there’s also a Team Caterpillar, then everyone on each team plays everyone on each of the other teams. I like this structure because it allows for the interesting dynamics of both cooperation and competition to play out in a bunch of different ways:

- Players of course try to come up with the smartest strategy to beat players on the other teams (competition).

- Players collaborate with their own team members to not only come up with the best strategies, but the best mix of strategies that will give them the most insight into how the other team is thinking about them. There’s usually one or two people that are really good at this type of analysis and everyone else on the team benefits from it.

- Teams win as a unit (collaboration) but there’s also a scoreboard within the team to see who scored the most points (competition).

- People are allowed to talk to each other across teams (collaboration) but it’s up to them to figure out how much to trust any information shared since at the end of the day they’re still competing with one another.

Players of course try to come up with the smartest strategy to beat players on the other teams (competition).

Players collaborate with their own team members to not only come up with the best strategies, but the best mix of strategies that will give them the most insight into how the other team is thinking about them. There’s usually one or two people that are really good at this type of analysis and everyone else on the team benefits from it.

Teams win as a unit (collaboration) but there’s also a scoreboard within the team to see who scored the most points (competition).

People are allowed to talk to each other across teams (collaboration) but it’s up to them to figure out how much to trust any information shared since at the end of the day they’re still competing with one another.

As the game host I am in communication with everyone across all of the teams: collecting their strategies, helping them understand the rules, and then writing the scripts that run the rounds that generate the points for each person and team.

Even though I don’t get to play my own strategies, I think I still have the most fun because I get to see the behind-the-scenes discussions amongst players on all of the teams and to see how intricate strategies for collaboration and competition play out.

Although I give out the scores of all the matches between rounds, I don’t share the strategies that people on the other teams played, so I also get to see how people interpret (or misinterpret) results and try to guess not only what the players played last round, but what they think they’ll play next round.

My favorite part of these tournaments (that makes them different from most of the other iterated prisoner’s dilemma games that I’ve seen) is that people can change their strategies between rounds. So, maybe David starts with a very friendly strategy like “Always Cooperate” in round 1, filled with optimism and idealism about the kindness of others. When he gets trounced in the first round, and he has a chance to update his strategy, will he stick to his guns, hoping that now that he’s signaled a desire to cooperate that others might be more friendly next round? Or will he feel spurned and flip to a more guarded strategy like Grim Reaper (cooperate until you defect, and then defect for the remainder of the 100 moves) or even something like Suspicious Tit-for-Tat that starts by defecting but then always copies the other player’s previous move?

The game plays out on two levels…

- Within a single turn (where your strategy determines how much you cooperate and how much you defect) and…

- Across turns (where you get to adjust your strategies to try to be smarter than the other teams, by trying to predict how they will be adjusting their strategies to be smarter than yours).

Within a single turn (where your strategy determines how much you cooperate and how much you defect) and…

Across turns (where you get to adjust your strategies to try to be smarter than the other teams, by trying to predict how they will be adjusting their strategies to be smarter than yours).

As we played this tournament a few times I learned that it helps to have more than 2 teams (that’s where it shifts from zero sum to non-zero sum) and that strategies can get even more interesting when you let them hinge on logic that considers metadata about teams and players on teams (you might want to be more forgiving of one team over another, or more defensive about specific people).

I’ve learned so much about cooperation and competition from these tournaments but I felt like part of it was because I had a privileged perspective into the games that the individual players weren’t able to see.

So THIS TIME, I want to do it differently!

This time, there are 4 teams, but all humans are on one team. The other three teams will be run by ChatGPT, Claude, and Gemini, respectively, and I will still be mediating a few things between the teams (like the exact logic of strategies picked by each team), but I will be sharing everything else that happens publicly (like the prompts I’m using to get them to generate strategies, whatever information each team wants to make public about their strategies, and detailed results from each round that will help us try to outsmart them in future rounds. To make it fair to the LLMs I’ll also make sure to share whatever we end up looking at back to them as well.

## The Setup

When prompting it to come up with strategies before each round, I’m gonna always use the latest model with deep research mode turned on. For this first introduction and setup for Round 1 (of 3, most likely) here are the models I will be using:

- ChatGPT 4.5 - Deep Research mode

- Claude Opus 4 - Research mode

- Gemini 2.5 Pro - Deep Research mode


Here’s the prompt I will give them:

{% responsive_image path:'assets/images/pieces/2025-08-28-wanna-play-an-iterated-prisoners-dilemma-tournament-between-chatgpt-claude-gemini-and-humans-01.png' %}

It includes:

- The basic rules of Prisoner’s Dilemma and the modified rules for this team-based iterated tournament.

- Instructions on how to write strategies using something that I’ve come up with and have been able to so far implement any strategy that someone has been able to come up with (it became a lot easier with AI assistance).

- Example strategies from the most simple to some more complicated ones.

- Considerations for how the team-based aspect of this tournament might influence strategic decisions.

- Instructions for how to format their submissions doc, with details around which parts will be public and which parts will be kept private until the game is over.

The basic rules of Prisoner’s Dilemma and the modified rules for this team-based iterated tournament.

Instructions on how to write strategies using something that I’ve come up with and have been able to so far implement any strategy that someone has been able to come up with (it became a lot easier with AI assistance).

Example strategies from the most simple to some more complicated ones.

Considerations for how the team-based aspect of this tournament might influence strategic decisions.

Instructions for how to format their submissions doc, with details around which parts will be public and which parts will be kept private until the game is over.

## Example strategies

The way we will describe strategies is using a new domain-specific language that looks like this (and is described in full in the prompt document linked above):

Each team will come up with 5 of these strategies (picking from well-known ones or inventing new ones) and every player will match up against every player on the other teams and play 100 times during the first turn. Then results will be shared and teams will be able to adjust their strategies for the next round. There will be 3 rounds.

## Next up: getting team submissions

I wanted to share the prompt above before I ran it with all of the LLMs, to give time for feedback and to potentially incorporate suggestions for improvement. Then, in the next couple days I’ll feed the prompt to each of the LLMs and add their players to the game engine. At that time I’ll also share the parts of the submissions that have been deemed public.

## What strategies should we humans play?

We humans also need to come up with a team name, 5 players, and 5 strategies to use to compete with the LLMs. I will come up with some default thoughts to start with, before I get the submissions back from the LLMs, but I would love to have input from others who find this to be interesting as well! Especially if you’re interested in getting deep in the details and really trying to beat the LLMs. If you’re interested in being a part of the human team, leave a comment and I’ll invite you to whichever messaging platform ends up being the most convenient for discussing these things.

Starting things scrappy and will add structure and figure things out as we go!

{% responsive_image path:'assets/images/pieces/2025-08-28-wanna-play-an-iterated-prisoners-dilemma-tournament-between-chatgpt-claude-gemini-and-humans-02.png' alt:'Illustration showing how always cooperate performs against other strategies. And also how grim trigger performs.' %}

