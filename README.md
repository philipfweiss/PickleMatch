## Computes Optimal Pickleball Pairings
Given a list of players and their ratings, runs thousands of simulations to find the teams/pairings that are the most fair.

Used for the Portland "Dinkies for Drinkies" mini pickleball tournaments. 

## How does it work?

The algorithm works in two phases: generating teams and then generating pairings. 

### Team Generation:
- Each team consists of 4 players, and the "strength" of the team is the cumulative rating of that team.
- Each team will have 1 player from the bottom 25%, 1 player from the 25-50% percentile, and 2 players from the top 50%.
- We randomly generate teams `num_attempts` times and pick the one with the lowest variance in team strength.

### Pairing Generation 
Dinkies for Drinkies has six rounds of gameplay. Each player keeps the same partner for 2 rounds, and they play with all three partners. No partners can play anyone on their team, and no partners will play the same exact opponents twice. 

We run a graph algorithm to find a pairing schedule respecting the above constraints. We do this `num_attempts` times and choose the pairing with the lowest average rating difference between matches. 
