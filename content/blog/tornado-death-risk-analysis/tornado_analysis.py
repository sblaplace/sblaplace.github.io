import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from io import StringIO
import matplotlib.patheffects as path_effects

# Data Sources:
# - NOAA Storm Prediction Center Tornado Database (1950-2024): https://www.spc.noaa.gov/wcm/
# - Thomas P. Grazulis "Significant Tornadoes" (1900-1949): Historical tornado records
# - U.S. Census Bureau Historical Population Estimates: https://www.census.gov/data/tables/time-series/dec/popchange-data-text.html
# 
# Population factors represent estimated population in tornado-prone regions (millions)
# Tornado-prone regions (25 states): AL, AR, FL, GA, IA, IL, IN, KS, KY, LA, MI, MN, MO, 
#                                    MS, NC, ND, NE, OH, OK, SC, SD, TN, TX, VA, WI
# Population estimates interpolated linearly between census years

# Raw data: Year, Deaths, Population (millions in tornado-prone regions)
data = """Year,Deaths,PopFactor,Era
1900,101,45.0,Pre-Radar
1901,52,45.8,Pre-Radar
1902,157,46.6,Pre-Radar
1903,216,47.4,Pre-Radar
1904,87,48.2,Pre-Radar
1905,184,49.0,Pre-Radar
1906,70,49.8,Pre-Radar
1907,80,50.6,Pre-Radar
1908,477,51.4,Pre-Radar
1909,404,52.2,Pre-Radar
1910,12,53.0,Pre-Radar
1911,55,53.8,Pre-Radar
1912,175,54.6,Pre-Radar
1913,346,55.4,Pre-Radar
1914,41,56.2,Pre-Radar
1915,84,57.0,Pre-Radar
1916,150,57.8,Pre-Radar
1917,551,58.6,Pre-Radar
1918,136,59.4,Pre-Radar
1919,206,60.2,Pre-Radar
1920,499,61.0,Pre-Radar
1921,202,61.8,Pre-Radar
1922,135,62.6,Pre-Radar
1923,110,63.4,Pre-Radar
1924,376,64.2,Pre-Radar
1925,794,65.0,Pre-Radar
1926,144,65.8,Pre-Radar
1927,540,66.6,Pre-Radar
1928,95,67.4,Pre-Radar
1929,274,68.2,Pre-Radar
1930,179,69.0,Pre-Radar
1931,36,69.8,Pre-Radar
1932,394,70.6,Pre-Radar
1933,362,71.4,Pre-Radar
1934,47,72.2,Pre-Radar
1935,71,73.0,Pre-Radar
1936,552,73.8,Pre-Radar
1937,29,74.6,Pre-Radar
1938,183,75.4,Pre-Radar
1939,91,76.2,Pre-Radar
1940,65,77.0,Pre-Radar
1941,53,77.8,Pre-Radar
1942,384,78.6,Pre-Radar
1943,58,79.4,Pre-Radar
1944,275,80.2,Pre-Radar
1945,210,81.0,Pre-Radar
1946,78,81.8,Pre-Radar
1947,313,82.6,Pre-Radar
1948,139,83.4,Pre-Radar
1949,211,84.2,Pre-Radar
1950,70,85.0,Pre-Radar
1951,34,86.78571428571429,Warning Era
1952,230,88.57142857142857,Warning Era
1953,519,90.35714285714286,Warning Era
1954,36,92.14285714285714,Warning Era
1955,129,93.92857142857143,Warning Era
1956,83,95.71428571428572,Warning Era
1957,193,97.5,Warning Era
1958,67,99.28571428571429,Warning Era
1959,58,101.07142857142857,Warning Era
1960,46,102.85714285714286,Warning Era
1961,52,104.64285714285714,Warning Era
1962,30,106.42857142857143,Warning Era
1963,31,108.21428571428572,Warning Era
1964,73,110.0,Warning Era
1965,301,111.78571428571429,Warning Era
1966,98,113.57142857142857,Warning Era
1967,114,115.35714285714286,Warning Era
1968,131,117.14285714285714,Warning Era
1969,66,118.92857142857143,Warning Era
1970,73,120.71428571428572,Warning Era
1971,159,122.5,Warning Era
1972,27,124.28571428571428,Warning Era
1973,89,126.07142857142858,Warning Era
1974,366,127.85714285714286,Warning Era
1975,60,129.64285714285714,Warning Era
1976,44,131.42857142857144,Warning Era
1977,43,133.21428571428572,Warning Era
1978,53,135.0,Warning Era
1979,84,136.78571428571428,Warning Era
1980,28,138.57142857142858,Warning Era
1981,24,140.35714285714286,Warning Era
1982,64,142.14285714285714,Warning Era
1983,34,143.92857142857144,Warning Era
1984,122,145.71428571428572,Warning Era
1985,94,147.5,Warning Era
1986,15,149.28571428571428,Warning Era
1987,59,151.07142857142856,Warning Era
1988,32,152.85714285714286,Warning Era
1989,50,154.64285714285717,Warning Era
1990,53,156.42857142857144,Warning Era
1991,39,158.21428571428572,Modern Era
1992,39,160.0,Modern Era
1993,33,161.78571428571428,Modern Era
1994,69,163.57142857142856,Modern Era
1995,30,165.35714285714286,Modern Era
1996,25,167.14285714285717,Modern Era
1997,67,168.92857142857144,Modern Era
1998,130,170.71428571428572,Modern Era
1999,94,172.5,Modern Era
2000,41,174.28571428571428,Modern Era
2001,40,176.07142857142856,Modern Era
2002,55,177.85714285714286,Modern Era
2003,54,179.64285714285717,Modern Era
2004,35,181.42857142857144,Modern Era
2005,39,183.21428571428572,Modern Era
2006,67,185.0,Modern Era
2007,81,186.78571428571428,Modern Era
2008,126,188.57142857142858,Modern Era
2009,21,190.35714285714286,Modern Era
2010,45,192.14285714285717,Modern Era
2011,553,193.92857142857144,Modern Era
2012,70,195.71428571428572,Modern Era
2013,55,197.5,Modern Era
2014,47,199.28571428571428,Modern Era
2015,36,201.07142857142858,Modern Era
2016,18,202.85714285714286,Modern Era
2017,35,204.64285714285717,Modern Era
2018,10,206.42857142857144,Modern Era
2019,41,208.21428571428572,Modern Era
2020,76,210.0,Modern Era
2021,103,210.0,Modern Era
2022,23,210.0,Modern Era
2023,83,210.0,Modern Era
2024,52,210.0,Modern Era
"""

df = pd.read_csv(StringIO(data))

# Calculate population-adjusted death rate (deaths per million population)
df['DeathRate'] = (df['Deaths'] / df['PopFactor'])

# Population milestones by era
print("\n" + "="*70)
print("POPULATION IN TORNADO-PRONE REGIONS BY ERA")
print("="*70)
print("Pre-Radar Era (1900-1950):  45.0M → 85.0M")
print("Warning Era (1951-1990):    86.8M → 156.4M")
print("Modern Era (1991-2024):     158.2M → 210.0M")
print("="*70)

# Define era colors and order
era_colors = {
    'Pre-Radar': '#d62728',      # Red
    'Warning Era': '#ff7f0e',    # Orange  
    'Modern Era': '#2ca02c'      # Green
}
era_order = ['Pre-Radar', 'Warning Era', 'Modern Era']

# Calculate 10-year rolling average
df['RollingAvg'] = df['DeathRate'].rolling(window=10, center=True).mean()

# Create figure with two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), height_ratios=[3, 1])
fig.suptitle('Tornado Death Risk in the United States (1900-2024)\nPopulation-Adjusted Mortality Rate', 
             fontsize=16, fontweight='bold', y=0.98)

# === TOP PLOT: Main time series ===
for era in era_order:
    era_data = df[df['Era'] == era]
    ax1.scatter(era_data['Year'], era_data['DeathRate'], 
                c=era_colors[era], label=era, alpha=0.6, s=40, edgecolors='white', linewidth=0.5)

# Add rolling average line
ax1.plot(df['Year'], df['RollingAvg'], color='navy', linewidth=2.5, 
         label='10-Year Rolling Average', zorder=5)

# Add era mean lines
for era in era_order:
    era_data = df[df['Era'] == era]
    mean_rate = era_data['DeathRate'].mean()
    ax1.hlines(mean_rate, era_data['Year'].min(), era_data['Year'].max(),
               colors=era_colors[era], linestyles='--', linewidth=2, alpha=0.8)
    
    # Annotate the mean with path effect for outline
    mid_year = (era_data['Year'].min() + era_data['Year'].max()) / 2
    text = ax1.annotate(f'{era}\nMean: {mean_rate:.2f}', 
                        xy=(mid_year, mean_rate), xytext=(0, 15),
                        textcoords='offset points', ha='center', fontsize=9,
                        bbox=dict(boxstyle='round,pad=0.3', facecolor=era_colors[era], alpha=0.3))
    text.set_path_effects([path_effects.Stroke(linewidth=3, foreground='white'),
                           path_effects.Normal()])

# Add vertical lines for era boundaries
ax1.axvline(x=1950.5, color='gray', linestyle=':', linewidth=1.5, alpha=0.7)
ax1.axvline(x=1990.5, color='gray', linestyle=':', linewidth=1.5, alpha=0.7)

# Annotate major outliers with path effect for outline
outliers = [(1925, 'Tri-State\nTornado'), (1953, 'Waco/Flint\nOutbreaks'), 
            (2011, 'Super\nOutbreak')]
for year, label in outliers:
    row = df[df['Year'] == year].iloc[0]
    text = ax1.annotate(label, xy=(year, row['DeathRate']), 
                        xytext=(0, 20), textcoords='offset points',
                        ha='center', fontsize=8, fontstyle='italic',
                        arrowprops=dict(arrowstyle='->', color='gray', lw=0.8))
    text.set_path_effects([path_effects.Stroke(linewidth=2, foreground='white'),
                           path_effects.Normal()])

ax1.set_ylabel('Deaths per Million Population\n(Tornado-Prone Regions)', fontsize=11)
ax1.set_xlim(1898, 2026)
ax1.set_ylim(0, 13)
ax1.legend(loc='upper right', framealpha=0.9)
ax1.grid(True, alpha=0.3)
ax1.set_axisbelow(True)

# === BOTTOM PLOT: Era comparison bar chart with error bars ===
era_stats = df.groupby('Era')['DeathRate'].agg(['mean', 'median', 'std', 'count']).reindex(era_order)

bars = ax2.bar(era_order, era_stats['mean'], color=[era_colors[e] for e in era_order], 
               edgecolor='black', linewidth=1.2, alpha=0.8)

# Add error bars (standard deviation)
ax2.errorbar(era_order, era_stats['mean'], yerr=era_stats['std'], 
             fmt='none', color='black', capsize=5, capthick=2, linewidth=2)

# Add value labels with smaller font size, not bold, and path effect
for bar, era in zip(bars, era_order):
    height = bar.get_height()
    text = ax2.text(bar.get_x() + bar.get_width()/2., height + era_stats.loc[era, 'std'] + 0.15,
                    f'{height:.2f}', ha='center', va='bottom', fontsize=9, fontweight='normal')
    text.set_path_effects([path_effects.Stroke(linewidth=2, foreground='white'),
                           path_effects.Normal()])

ax2.set_ylabel('Mean Death Rate', fontsize=11)
ax2.set_xlabel('Era', fontsize=11)
ax2.set_title('Average Death Rate by Era (± Std Dev)', fontsize=12, pad=10)
ax2.set_ylim(0, 6.5)  # Increased to accommodate error bars
ax2.grid(True, axis='y', alpha=0.3)
ax2.set_axisbelow(True)

plt.tight_layout()
plt.savefig('tornado_death_risk.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.show()

# Print summary statistics
print("\n" + "="*70)
print("SUMMARY STATISTICS BY ERA")
print("="*70)
for era in era_order:
    era_data = df[df['Era'] == era]
    print(f"\n{era} ({era_data['Year'].min()}-{era_data['Year'].max()}):")
    print(f"  Mean death rate:   {era_data['DeathRate'].mean():.3f} per million")
    print(f"  Median death rate: {era_data['DeathRate'].median():.3f} per million")
    print(f"  Std deviation:     {era_data['DeathRate'].std():.3f}")
    print(f"  Total deaths:      {era_data['Deaths'].sum():,}")
    print(f"  Population range:  {era_data['PopFactor'].min():.1f}M → {era_data['PopFactor'].max():.1f}M")

# Calculate improvement
pre_radar_mean = df[df['Era'] == 'Pre-Radar']['DeathRate'].mean()
modern_mean = df[df['Era'] == 'Modern Era']['DeathRate'].mean()
improvement = ((pre_radar_mean - modern_mean) / pre_radar_mean * 100)

print(f"\n{'='*70}")
print(f"OVERALL IMPROVEMENT: {improvement:.1f}% reduction")
print(f"in population-adjusted death rate from Pre-Radar to Modern Era")
print(f"({pre_radar_mean:.3f} → {modern_mean:.3f} deaths per million)")
print("="*70)
