import os
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use('Agg')  # Guard for headless execution on DGX
import matplotlib.pyplot as plt

try:
    from gplearn.genetic import SymbolicRegressor
except ModuleNotFoundError:
    print("Error: 'gplearn' is not installed in this environment.")
    print("Please run: ./.venv/bin/pip install gplearn")
    exit(1)

def discover_image_equation(image_name, image_path):
    print(f"\n--- Processing: {image_name} ---")
    
    if not os.path.exists(image_path):
        print(f"Error: Could not find image at {image_path}")
        return

    # 1. Load the image and convert to grayscale
    img = Image.open(image_path).convert('L')
    
    # 2. Downsample to keep processing fast (30x30 pixels)
    img = img.resize((30, 30), Image.Resampling.LANCZOS)
    
    # 3. Invert AND Binarize to boost the signal
    raw_array = 1.0 - (np.array(img) / 255.0)
    # THRESHOLD STEP: Any pixel with a faint trace (> 0.15) becomes a solid 1.0
    img_array = np.where(raw_array > 0.15, 1.0, 0.0)
    
    # 4. Construct the (X, Y) coordinate grids matching the pixel array
    h, w = img_array.shape
    x_coords = np.linspace(-1, 1, w)
    y_coords = np.linspace(-1, 1, h)
    X, Y = np.meshgrid(x_coords, y_coords)
    
    # Flatten grids into 2D input variables (X, Y pairs) and target outputs
    coordinates = np.vstack([X.ravel(), Y.ravel()]).T
    intensities = img_array.ravel()
    
    # 5. Initialize and train the Symbolic Regressor
    print("Running evolutionary algorithm to discover mathematical representation...")
    est = SymbolicRegressor(
        population_size=6000,          # Expanded for complex feature discovery
        generations=50,               # More generations to align coordinates
        function_set=('add', 'sub', 'mul', 'div', 'sin', 'cos', 'abs'), 
        metric='mean absolute error',
        parsimony_coefficient=0.0002,  # Loosened to prevent premature pruning of formulas
        random_state=42,
        n_jobs=-1                      # Utilizes all CPU cores on the DGX
    )
    est.fit(coordinates, intensities)
    
    print(f"✨ Found Equation for {image_name}:")
    print(est._program)

    # 6. Generate and save visual validation to verify accuracy
    predicted_intensities = est.predict(coordinates)
    predicted_image = predicted_intensities.reshape(h, w)
    
    fig, axes = plt.subplots(1, 2, figsize=(6, 3))
    # Add indices [0] and [1] to the axes calls:
    axes[0].imshow(img_array, cmap='gray', extent=[-1,1,-1,1])
    axes[0].set_title("Target (Binarized)")
    axes[0].axis('off')
    
    axes[1].imshow(predicted_image, cmap='gray', extent=[-1,1,-1,1])
    axes[1].set_title("SR Reconstructed")
    axes[1].axis('off')

    output_preview = f"sr_match_{image_name}.png"
    plt.savefig(output_preview, bbox_inches='tight')
    plt.close()
    print(f"Saved visual verification graph to: {output_preview}")

# Execute the pipeline on your target images
image_directory = "geometric_analogy_dataset/images"
discover_image_equation("1_square", f"{image_directory}/1_square.png")
discover_image_equation("2_rectangle", f"{image_directory}/2_rectangle.png")
