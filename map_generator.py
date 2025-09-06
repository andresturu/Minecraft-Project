import numpy as np
from noise import pnoise2


def generate_biome_map(width, height, seed, scale, octaves=4, persistence=0.5, lacunarity=2.0):
    """
    Generates a 2D biome map using Perlin noise.
    
    Returns:
        biome_map: numpy.ndarray of shape (height, width), integers representing biomes
    """
    # Define biome thresholds based on noise elevation, elevation doesn't get higher than 0.6 about?
    def get_biome(elevation):
        if elevation < -0.20:  
            return 0  # Deep water
        elif elevation < -0.11:
            return 1  # Desert
        elif elevation < 0.10:
            return 2  # Grassland
        elif elevation < 0.20:
            return 3  # Forest
        elif elevation < 0.33:
            return 4  # Mountain
        else:
            return 5  # Snow
        
        
    
    np.random.seed(seed)
    x_offset = np.random.uniform(0, 10000)
    y_offset = np.random.uniform(0, 10000)
    
    biome_map = np.zeros((height, width), dtype=np.uint8) #creates 2D NumPy array, filled with zeros, height # of rows and width # of columns, each element in the array is an 8-bit unsigned integer (0-255)
    for y in range(height):
        for x in range(width):
           
        
           
            nx = (x + x_offset) / scale
            ny = (y + y_offset + 500) / scale
            
            elevation = pnoise2(ny, nx, octaves=octaves, persistence=persistence,
                                lacunarity=lacunarity) # removed base = seed and that fixed the issue. Too high of a base causes weird vertical line patterns
            
            biome_map[y, x] = get_biome(elevation)
    
    return biome_map 