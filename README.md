# A second foray into Computer Vision

For as long as I can remember, I've been fascinated by Sudoku. I have family members who can play it for hours, uninterrupted, and claim it's the undisputed king of brain games. 

Not being much of a "numbers person", I never got particularly good at it, favouring puzzles like Chess or Cryptograms. However, the very simple constraints and virtually endless difficulty curve always made me wish I was better at it.

So, as a mostly self-taught programmer, I figured I'd leverage my lack of talent with Sudoku by turning it into a programming exercise. It would be fairly simple to create a 9x9 array and feed it into a function that backtracks each digit to eventually sum to the final answer, but a much more interesting (for me) challenge is to have the computer read the puzzle off an image, interpret it into a list-of-lists structure, and solve for x.

In this project, I used a few Python libraries, mainly OpenCV (computer vision) and Google Tesseract (character recognition). 

The algorithm that solves the Sudoku puzzle is basic recursive backtracking (read: brute force), but I plan to implement the Knuth dancing-links algorithm as I iteratively improve on this project.

### Next Steps:
- Implement a more efficient algorithm to solve the Sudoku itself. See [Knuth Algorithm X](https://en.wikipedia.org/wiki/Knuth%27s_Algorithm_X).
- Improve the capabilities of the Computer Vision function such that actual photographs can be used instead of just computer generated images.
- Use a machine learning library like Keras to read handwritten text on a partially complete puzzle.

## In Action:
<img src="assets/result.png" width="50%" height="50%" />
