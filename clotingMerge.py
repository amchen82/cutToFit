import cv2
import numpy as np

def find_edges_and_contours() : 
        # Load images of clothing parts (make sure the parts have transparent backgrounds where applicable)
    # fix the path of the images
    
    torso = cv2.imread("C:\\Users\\zhaih\\OneDrive\\\Pictures\\torso.png", cv2.IMREAD_UNCHANGED)
    sleeve = cv2.imread("C:\\Users\\zhaih\\OneDrive\\Pictures\\sleeve1.png", cv2.IMREAD_UNCHANGED)
    # Function to detect edges and find contours
    def find_edges_and_contours(image):
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply edge detection (Canny)
        edges = cv2.Canny(gray, threshold1=50, threshold2=150)

        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        return contours

    # Find contours of both the torso and sleeve
    torso_contours = find_edges_and_contours(torso)
    sleeve_contours = find_edges_and_contours(sleeve)

    # Calculate the bounding box for the contours of the torso
    x_torso, y_torso, w_torso, h_torso = cv2.boundingRect(torso_contours[0])

    # Calculate the bounding box for the sleeve contours
    x_sleeve, y_sleeve, w_sleeve, h_sleeve = cv2.boundingRect(sleeve_contours[0])

    # Determine the position where the sleeve should be placed relative to the torso (e.g., near the shoulder)
    # You can refine this based on edge analysis or predefined logic
    sleeve_position = (x_torso + int(w_torso * 0.05), y_torso + int(h_torso * 0.3))  # Adjust based on torso dimensions

    # Combine the images by pasting the sleeve onto the torso image
    combined = torso.copy()
    sleeve_resized = cv2.resize(sleeve, (w_sleeve, h_sleeve))  # Resize if necessary

    # Create a region of interest on the torso image where the sleeve will be placed
    y_offset, x_offset = sleeve_position
    y1, y2 = y_offset, y_offset + sleeve_resized.shape[0]
    x1, x2 = x_offset, x_offset + sleeve_resized.shape[1]

    # Merge the images by combining the alpha channels (for transparency)
    alpha_sleeve = sleeve_resized[:, :, 3] / 255.0  # Sleeve transparency (assuming RGBA)
    alpha_torso = 1.0 - alpha_sleeve  # Background transparency

    # Apply the alpha blend between torso and sleeve
    for c in range(0, 3):  # Loop over RGB channels
        combined[y1:y2, x1:x2, c] = (alpha_sleeve * sleeve_resized[:, :, c] + alpha_torso * combined[y1:y2, x1:x2, c])

    # Save or display the final merged image
    cv2.imwrite("merged_clothing.png", combined)

    # Optional: Display the final result
    cv2.imshow("Merged Clothing", combined)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


    # generate main function to run
if __name__ == "__main__":
    find_edges_and_contours()

# need to determine how the position of different piece
    # need to determine how the pics can be scaled to fit
    