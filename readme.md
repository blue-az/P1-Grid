# Grid Meeting Simulation

## Problem Description

This simulation explores an interesting probability problem:

> You and a friend live N blocks away from each other on a square grid. You both decide to take random walks towards each other. You flip coins at the same time to decide whether to go horizontally or vertically, but always moving toward each other. What is the probability you'll meet?

## Key Insights

- **Starting Positions**: You start at the bottom-left (SW) corner, your friend at the top-right (NE) corner
- **Movement Rules**: 
  - You can only move right or up (determined by coin flip)
  - Your friend can only move left or down (determined by coin flip)
- **Meeting Points**: The only possible meeting points are along the SE-NW diagonal
- **Probability**: The probability of meeting is exactly 1/N for an N×N grid

## Running the Simulation

### Requirements
- Python 3.6+
- Streamlit
- NumPy
- Matplotlib
- Pandas

### Installation

```bash
pip install streamlit numpy matplotlib pandas
```

### Running the App

```bash
streamlit run grid_meeting_sim.py
```

### Controls

- **Grid Size**: Adjust the size of the grid (N×N) from 3×3 to 10×10
- **Number of Simulations**: Set how many simulations to run for analysis
- **Animation**: Toggle animation for a single simulation
- **Animation Speed**: Adjust how quickly the animation plays

## Features

### Simulation Tab
- Visual representation of the grid with labeled meeting points (A, B, C, etc.)
- Animation of both walkers' paths
- Status updates showing current positions and steps
- Highlights meeting point if one occurs

### Analysis Tab
- Runs thousands of simulations to calculate empirical meeting probability
- Displays distribution of meeting locations
- Compares empirical results with theoretical 1/N probability
- Shows detailed statistics for each possible meeting point

### Theory Tab
- Mathematical explanation of why the probability is 1/N
- Description of the combinatorial interpretation
- Analysis of path requirements to reach each meeting point

## Mathematical Explanation

The 1/N probability arises because:

1. Each walker must take exactly N-1 steps to reach any meeting point
2. For each meeting point (i, N-1-i):
   - You must take exactly i steps right and (N-1-i) steps up
   - Your friend must take exactly (N-1-i) steps left and i steps down
3. Since coin flips are independent and each path is equally likely:
   - The probability of meeting at any specific point is identical
   - With N possible meeting points, the probability is 1/N

## Example

In a 5×5 grid:
- 5 possible meeting points (labeled A through E)
- Each walker takes exactly 4 steps
- Meeting probability is 1/5 = 0.2 or 20%

## Notes

- The simulation terminates after exactly N-1 steps (the minimum needed to reach any meeting point)
- Meetings can only occur if both walkers independently choose paths that lead to the same point
- All meeting points have equal probability
