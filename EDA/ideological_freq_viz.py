import matplotlib.pyplot as plt
import numpy as np

# Original data
ideologies = ['libleft', 'libright', 'libcenter', 'centrist', 'left', 'right', 'authright', 'authcenter', 'authleft']
frequencies = [18070, 15054, 13548, 13408, 9646, 6526, 5672, 4801, 4275]

# Reorganize data by economic position and authority level
# Economic positions: Left, Center, Right
# Authority levels: Libertarian, Center, Authoritarian

# Left economic position
left_lib = 18070  # libleft
left_center = 9646  # left
left_auth = 4275  # authleft

# Center economic position
center_lib = 13548  # libcenter
center_center = 13408  # centrist
center_auth = 4801  # authcenter

# Right economic position
right_lib = 15054  # libright
right_center = 6526  # right
right_auth = 5672  # authright

# Prepare data for stacked bar chart
economic_positions = ['Left', 'Center', 'Right']
libertarian_counts = [left_lib, center_lib, right_lib]
center_counts = [left_center, center_center, right_center]
authoritarian_counts = [left_auth, center_auth, right_auth]

# Create the stacked bar chart
fig, ax = plt.subplots(figsize=(12, 8))

# Width of bars
bar_width = 0.6

# Create stacked bars
bars1 = ax.bar(economic_positions, libertarian_counts, bar_width, 
               label='Libertarian', color='#90EE90', alpha=0.8)
bars2 = ax.bar(economic_positions, center_counts, bar_width, 
               bottom=libertarian_counts, label='Center', color='#D3D3D3', alpha=0.8)
bars3 = ax.bar(economic_positions, authoritarian_counts, bar_width, 
               bottom=np.array(libertarian_counts) + np.array(center_counts), 
               label='Authoritarian', color='#FF6B6B', alpha=0.8)

# Add value labels on each segment
for i, pos in enumerate(economic_positions):
    # Libertarian segment (bottom)
    lib_height = libertarian_counts[i]
    ax.text(i, lib_height/2, f'{lib_height:}\n({lib_height/91000:.1%})', 
            ha='center', va='center', fontweight='regular', fontsize=10)
    
    # Center segment (middle)
    center_height = center_counts[i]
    center_y = lib_height + center_height/2
    ax.text(i, center_y, f'{center_height:}\n({center_height/91000:.1%})', 
            ha='center', va='center', fontweight='regular', fontsize=10)
    
    # Authoritarian segment (top)
    auth_height = authoritarian_counts[i]
    auth_y = lib_height + center_height + auth_height/2
    ax.text(i, auth_y, f'{auth_height:}\n({auth_height/91000:.1%})', 
            ha='center', va='center', fontweight='regular', fontsize=10)

    # Total at the top
    total = lib_height + center_height + auth_height
    ax.text(i, total + 500, f'Total: {total:}\n({total/91000:.1%})', 
            ha='center', va='bottom', fontweight='bold', fontsize=11, 
            bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))

# Customize the plot
ax.set_ylabel('Number of Users', fontsize=12, fontweight='bold')
ax.set_xlabel('Economic Position', fontsize=12, fontweight='bold')
ax.set_title('Reddit Political Compass Flair Distribution\nStacked by Authority Level (n = 91,000)', 
             fontsize=14, fontweight='bold', pad=20)

# # Add legend
# ax.legend(loc='upper right', fontsize=11)

# Add grid for better readability
ax.grid(True, alpha=0.3, axis='y')
ax.set_axisbelow(True)

# Set y-axis limits with some padding
max_total = max([sum(x) for x in zip(libertarian_counts, center_counts, authoritarian_counts)])
ax.set_ylim(0, max_total * 1.15)

# Add some styling
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.show()

# Print detailed breakdown
print("Reddit Political Compass Distribution by Economic and Authority Positions:")
print("=" * 70)
print(f"{'Economic Position':<15} {'Libertarian':<12} {'Center':<12} {'Authoritarian':<12} {'Total':<12}")
print("-" * 70)

for i, pos in enumerate(economic_positions):
    lib = libertarian_counts[i]
    center = center_counts[i]
    auth = authoritarian_counts[i]
    total = lib + center + auth
    print(f"{pos:<15} {lib:>8} ({lib/91000:>5.1%}) {center:>8} ({center/91000:>5.1%}) {auth:>8} ({auth/91000:>5.1%}) {total:>8} ({total/91000:>5.1%})")

print("-" * 70)
total_lib = sum(libertarian_counts)
total_center = sum(center_counts)
total_auth = sum(authoritarian_counts)
grand_total = total_lib + total_center + total_auth

# print(f"{'TOTAL':<15} {total_lib:>8} ({total_lib/91000:>5.1%}) {total_center:>8} ({total_center/91000:>5.1%}) {total_auth:>8} ({total_auth/91000:>5.1%}) {grand_total:>8} ({grand_total/91000:>5.1%})")