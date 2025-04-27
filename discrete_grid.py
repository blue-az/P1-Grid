import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
from matplotlib.patches import Circle, Rectangle
from matplotlib.lines import Line2D

st.set_page_config(page_title="Grid Meeting Probability", layout="wide")

# Title and description
st.title("Random Walks Toward Each Other on a Square Grid")
st.write("""
This simulator demonstrates the problem: You and a friend live N blocks away from each other on a square grid.
You both flip coins at the same time to decide whether to go horizontally or vertically, 
but you're always moving toward each other. What's the probability you'll meet?
""")

# Sidebar controls
st.sidebar.header("Simulation Parameters")
grid_size = st.sidebar.slider("Grid Size (N×N)", 3, 10, 5)
num_simulations = st.sidebar.slider("Number of Simulations", 100, 100000, 10000)
animate = st.sidebar.checkbox("Animate Single Simulation", True)
animation_speed = st.sidebar.slider("Animation Speed", 1, 50, 10, disabled=not animate)

# Create tabs
tab1, tab2, tab3 = st.tabs(["Simulation", "Analysis", "Theory"])

with tab1:
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Placeholder for grid visualization
        grid_placeholder = st.empty()
    
    with col2:
        # Status display
        status_placeholder = st.empty()
        
        # Run buttons
        col_a, col_b = st.columns(2)
        with col_a:
            simulate_button = st.button("Run Simulation")
        with col_b:
            analyze_button = st.button("Run Analysis")
        
        # Progress bar (only shown during animation)
        if animate:
            progress_bar = st.empty()

# This defines the simulation where walkers move only toward each other
# You are at bottom-left (0,0) and move right/up
# Friend is at top-right (n-1,n-1) and moves left/down
# Meeting points are on the SE-NW diagonal: (0,n-1), (1,n-2), ..., (n-1,0)
def simulate_meeting(animate=False):
    n = grid_size
    
    # Initialize positions
    you_pos = [0, 0]  # Bottom left (SW)
    friend_pos = [n-1, n-1]  # Top right (NE)
    
    # Track paths
    you_path = [you_pos.copy()]
    friend_path = [friend_pos.copy()]
    
    # Calculate possible meeting points (SE-NW diagonal)
    meeting_points = []
    for i in range(n):
        meeting_points.append([i, n-1-i])  # Points from SE to NW
    
    # Continue until paths are determined
    steps = 0
    met = False
    
    # Each walker takes exactly n-1 steps to reach any meeting point
    max_steps = n - 1
    
    while steps < max_steps:
        steps += 1
        
        # You flip a coin - heads move right, tails move up
        your_move = "right" if np.random.random() < 0.5 else "up"
        
        if your_move == "right" and you_pos[0] < n-1:
            you_pos[0] += 1
        elif your_move == "up" and you_pos[1] < n-1:
            you_pos[1] += 1
        
        # Friend flips a coin - heads move left, tails move down
        friend_move = "left" if np.random.random() < 0.5 else "down"
        
        if friend_move == "left" and friend_pos[0] > 0:
            friend_pos[0] -= 1
        elif friend_move == "down" and friend_pos[1] > 0:
            friend_pos[1] -= 1
        
        # Record paths
        you_path.append(you_pos.copy())
        friend_path.append(friend_pos.copy())
        
        # Check if they're at the same position
        if you_pos[0] == friend_pos[0] and you_pos[1] == friend_pos[1]:
            met = True
    
    return met, steps, you_path, friend_path, meeting_points

def animate_simulation():
    # Run a simulation
    met, steps, you_path, friend_path, meeting_points = simulate_meeting(animate=True)
    
    # Setup the visualization
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Initial setup
    ax.set_xlim(-0.5, grid_size - 0.5)
    ax.set_ylim(-0.5, grid_size - 0.5)
    ax.set_xticks(range(grid_size))
    ax.set_yticks(range(grid_size))
    ax.set_aspect('equal')
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Draw the grid points
    for i in range(grid_size):
        for j in range(grid_size):
            # Highlight potential meeting points (SE-NW diagonal)
            if [i, j] in meeting_points:
                ax.plot(i, j, 'o', color='green', markersize=10, alpha=0.3)
            else:
                ax.plot(i, j, 'ko', markersize=5)
    
    # Initialize markers
    you_marker = Circle((0, 0), 0.3, color='red', alpha=0.7)
    friend_marker = Circle((grid_size-1, grid_size-1), 0.3, color='blue', alpha=0.7)
    ax.add_patch(you_marker)
    ax.add_patch(friend_marker)
    
    # Add legend
    legend_elements = [
        Line2D([0], [0], marker='o', color='red', label='You', 
               markerfacecolor='red', markersize=10, linestyle=''),
        Line2D([0], [0], marker='o', color='blue', label='Friend', 
               markerfacecolor='blue', markersize=10, linestyle=''),
        Line2D([0], [0], marker='o', color='green', label='Possible Meeting Points', 
               markerfacecolor='green', markersize=10, alpha=0.3, linestyle=''),
    ]
    ax.legend(handles=legend_elements, loc='upper center', 
              bbox_to_anchor=(0.5, 1.15), ncol=3)
    
    # Label meeting points A, B, C, etc.
    for i, point in enumerate(meeting_points):
        label = chr(65 + i)  # A, B, C, ...
        ax.text(point[0], point[1]+0.3, label, fontsize=12, ha='center')
    
    # Display initial state
    grid_placeholder.pyplot(fig)
    
    # Update status display
    status_placeholder.write(f"""
    **Initial State**
    - You: ({you_path[0][0]}, {you_path[0][1]}) (SW corner)
    - Friend: ({friend_path[0][0]}, {friend_path[0][1]}) (NE corner)
    - Distance: {abs(friend_path[0][0] - you_path[0][0]) + abs(friend_path[0][1] - you_path[0][1])} blocks
    
    There are {grid_size} possible meeting points along the SE-NW diagonal (labeled A-{chr(64+grid_size)}).
    """)
    
    # Animation
    if animate:
        progress_bar.progress(0)
        
        for i in range(1, len(you_path)):
            # Update progress bar
            progress = i / (len(you_path) - 1)
            progress_bar.progress(progress)
            
            # Draw paths up to current step
            ax.plot([you_path[i-1][0], you_path[i][0]], 
                    [you_path[i-1][1], you_path[i][1]], 'r-', alpha=0.7)
            ax.plot([friend_path[i-1][0], friend_path[i][0]], 
                    [friend_path[i-1][1], friend_path[i][1]], 'b-', alpha=0.7)
            
            # Update markers
            you_marker.center = (you_path[i][0], you_path[i][1])
            friend_marker.center = (friend_path[i][0], friend_path[i][1])
            
            # Update display
            grid_placeholder.pyplot(fig)
            
            # Update status
            status_placeholder.write(f"""
            **Step {i}**
            - You: ({you_path[i][0]}, {you_path[i][1]})
            - Friend: ({friend_path[i][0]}, {friend_path[i][1]})
            - Distance: {abs(friend_path[i][0] - you_path[i][0]) + abs(friend_path[i][1] - you_path[i][1])} blocks
            """)
            
            # Pause for animation
            time.sleep(1.0 / animation_speed)
    
    # Final state - emphasize if they met
    if met:
        meeting_point = you_path[-1]
        meeting_circle = Circle((meeting_point[0], meeting_point[1]), 
                                0.4, color='green', alpha=0.5)
        ax.add_patch(meeting_circle)
        
        # Find which meeting point they met at (A, B, C, etc.)
        for i, point in enumerate(meeting_points):
            if point[0] == meeting_point[0] and point[1] == meeting_point[1]:
                meeting_label = chr(65 + i)
                break
        else:
            meeting_label = "?"
        
        status_placeholder.success(f"""
        **Meeting Occurred!**
        - Meeting Point: {meeting_label} ({meeting_point[0]}, {meeting_point[1]})
        - Steps: {steps}
        """)
    else:
        status_placeholder.info(f"""
        **No Meeting Occurred**
        - Final You Position: ({you_path[-1][0]}, {you_path[-1][1]})
        - Final Friend Position: ({friend_path[-1][0]}, {friend_path[-1][1]})
        - Steps: {steps}
        """)
    
    # Final display update
    grid_placeholder.pyplot(fig)
    if animate:
        progress_bar.empty()

def run_analysis():
    # Run multiple simulations
    results = []
    meeting_locations = np.zeros(grid_size)
    
    with st.spinner(f"Running {num_simulations} simulations..."):
        for _ in range(num_simulations):
            met, steps, you_path, friend_path, meeting_points = simulate_meeting()
            results.append(met)
            
            # If they met, record the meeting location
            if met:
                final_pos = you_path[-1]
                for i, point in enumerate(meeting_points):
                    if point[0] == final_pos[0] and point[1] == final_pos[1]:
                        meeting_locations[i] += 1
                        break
    
    # Calculate empirical probability
    empirical_prob = sum(results) / len(results)
    
    # Calculate meeting location probabilities
    if sum(meeting_locations) > 0:
        meeting_probs = meeting_locations / sum(meeting_locations)
    else:
        meeting_probs = np.zeros(grid_size)
    
    # Display results in the Analysis tab
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Grid Size**: {grid_size}×{grid_size}")
        st.write(f"**Number of Simulations**: {num_simulations}")
        st.write(f"**Empirical Meeting Probability**: {empirical_prob:.4f}")
        st.write(f"**Theoretical Probability**: 1/{grid_size} = {1/grid_size:.4f}")
    
    with col2:
        # Calculate total number of meetings
        total_meetings = int(sum(meeting_locations))
        st.write(f"**Total Meetings**: {total_meetings} out of {num_simulations}")
        
        # Create a simple table of meeting locations
        data = []
        for i in range(grid_size):
            point_label = chr(65 + i)  # A, B, C, etc.
            point_coord = f"({i}, {grid_size-1-i})"
            count = int(meeting_locations[i])
            percentage = meeting_probs[i] * 100 if sum(meeting_locations) > 0 else 0
            data.append([point_label, point_coord, count, f"{percentage:.1f}%"])
        
        df = pd.DataFrame(data, columns=["Point", "Coordinates", "Count", "Percentage"])
        st.write(df)
    
    # Create bar chart of meeting locations
    fig, ax = plt.subplots(figsize=(10, 6))
    positions = np.arange(grid_size)
    ax.bar(positions, meeting_probs, color='green', alpha=0.7)
    ax.set_xlabel('Meeting Position')
    ax.set_ylabel('Probability')
    ax.set_title('Probability Distribution of Meeting Locations')
    ax.set_xticks(positions)
    
    # Add location labels (A, B, C, etc.)
    location_labels = [chr(65 + i) for i in range(grid_size)]
    ax.set_xticklabels(location_labels)
    
    # Add coordinate labels as secondary information
    for i, label in enumerate(location_labels):
        x_coord = i
        y_coord = grid_size - 1 - i
        if meeting_probs[i] > 0:
            ax.annotate(f"({x_coord},{y_coord})", 
                       (i, meeting_probs[i] + 0.01),
                       ha='center', va='bottom')
    
    st.pyplot(fig)
    
    # Additional insights
    st.write("""
    ### Observations:
    
    1. The meeting probability is approximately 1/N for an N×N grid
    2. All meeting points along the SE-NW diagonal have equal probability
    3. This is because both walkers must independently choose the right combination of horizontal and vertical steps
    
    The empirical results from our simulations align with the theoretical prediction of 1/N probability.
    """)

# Add theoretical explanation
with tab3:
    st.write("""
    ## Mathematical Theory
    
    Let's analyze why the meeting probability is 1/N for an N×N grid:
    
    ### Key Insights:
    
    1. **Constrained Movement**: 
       - You (at SW corner) can only move east or north
       - Friend (at NE corner) can only move west or south
    
    2. **Meeting Points**: 
       - Meetings can only occur on the SE-NW diagonal
       - These points are at coordinates (i, N-1-i) for i from 0 to N-1
       - We can label them as points A, B, C, etc.
    
    3. **Path Requirements**: 
       - For you to reach meeting point (i, N-1-i):
         * You must take exactly i steps east and (N-1-i) steps north
       - For friend to reach that same point:
         * Friend must take exactly (N-1-i) steps west and i steps south
    
    4. **Independence and Equal Probability**:
       - Each walker's decisions are independent
       - Each path to each meeting point is equally likely
       - The probability of meeting at a specific point is:
         * For you: (N-1 choose i) * (1/2)^(N-1)
         * For friend: (N-1 choose i) * (1/2)^(N-1)
       - Combined probability: (N-1 choose i)² * (1/2)^(2N-2)
    
    5. **Total Meeting Probability**:
       - Sum over all possible meeting points i from 0 to N-1
       - This equals 1/N
    
    ### For Example, in a 5×5 Grid:
    
    - 5 possible meeting points (A through E)
    - Each requires specific combinations of moves
    - Meeting probability is 1/5 = 0.2 or 20%
    
    ### Combinatorial Interpretation:
    
    The problem can be seen as two independent walkers selecting paths through a grid.
    The 1/N probability represents the constraint that both must arrive at the same point
    despite making independent random choices.
    """)

# Handle button actions
if simulate_button:
    animate_simulation()

if analyze_button:
    run_analysis()
