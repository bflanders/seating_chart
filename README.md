# seating_chart
Making a seating chart so that everyone's happy!

This repo comes from a [Reddit post](https://www.reddit.com/r/programming/comments/ekc4be/story_making_a_bruteforce_algorithm_viable_with_a/) I saw about how some one (named Mikko) was making a seating chart based on constraints in a random way. [Here is the blog post](https://tech.mikkohaapanen.com/making-brute-force-algorithm-viable-with-a-nudge/) about it.

Mikko first tried to get random permutations and then check constraints. The blog says that "small nudges" where used, but it wasn't clear to me what the small nudges were. It sounded like they were applying some heuristics? Not totally sure...

But random draws? Heuristics? How about a SAT solver? The idea is that you take the state of seating chart (even if all the seats are empty) and you take all your students that have special considerations and start filling them in one at a time. If you find that you can't follow the constraints, then you back up and try something else. Depth first search of your space! Cool!

