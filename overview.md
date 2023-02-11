### Step 1
- Run the main file.
- The main file should instantiate a loop that opens the webcam and scrutinizes each frame to find a Sudoku board.

### Step 2
- Once an image is found, the image should be resized, reshaped and processed into the best possible format/colors for OCR.
- [For debugging, hang the program and observe the image once it passes this stage, and ensure that all types of images will work reliably]

### Step 3
- Once the image has been analyzed and processed, send the resulting cv2 object to the OCR program. This has to be fast, and accurate!
- The output should be a numpy array representing the board, with zeros representing blank spaces.

### Step 4
- Once a numpy array representing the board has been created, use an algorithm to solve the Sudoku puzzle. Find something better than recursive backtracking...

### Step 5
- Once the puzzle has been solved (and verified), open the frame that was created in step 1, and draw the correct numbers directly onto it.

### Step 6
- Display the finished image, wait for key 0, then terminate.