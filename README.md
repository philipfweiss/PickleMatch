Algorithm:
- Let {p_1, p_2.... p_n} be the list of players, each with a rating r_i. 
- Our goal is to find 
    * Teams of four
    * 6 rounds of play, switching partner every 2 rounds

- We wish to minimize
    * Let A(p_i) be the average opponent rating of player i.
    * We want to minimize the variance of {A(p_1) .... A(p_n)}


Two phases: assigning teams, and finding pairings.
1. We assign teams of four where the skill level is as close to average as possible.
2. We generate pairings according to rules above, then calculate the variance.

We do this as many times as possible and pick the teams/pairings with minimal variance.
