#include <stdio.h>
#include <stdlib.h>
#include <time.h>


void shuffle(int *array, size_t n);
int check_columns(int (*board)[9]);
int check_squares(int (*board)[9]);
void create_board(int board[9][9]);
void print_board(int board[9][9]);

int main() {
    clock_t start_time = clock();
    srand(time(NULL)); // seed the random number generator
    int board[9][9];
    create_board(board);
    print_board(board);
    clock_t end_time = clock();
    double time_used = (double)(end_time - start_time) / CLOCKS_PER_SEC;
    printf("\nTime used to create board %f seconds", time_used);
    printf("\npress enter to exit: ");
    getchar();
    return 0;
}


void shuffle(int *array, size_t n)
{
    if (n > 1) 
    {
        size_t i;
        for (i = 0; i < n - 1; i++) 
        {
          size_t j = i + rand() / (RAND_MAX / (n - i) + 1);
          int t = array[j];
          array[j] = array[i];
          array[i] = t;
        }
    }
}


// first index is column and second is row
int check_columns(int (*board)[9]){
    for (int row = 0; row < 9; row++){

        int numbers[] = {0, 0, 0, 0, 0, 0, 0, 0, 0};

        for (int column = 0; column < 9; column++){

            int number = board[column][row];
            
            if (number != 0){
                numbers[number - 1] += 1;
            }
        }
        for (int i = 0; i < 9; i++){
            if (numbers[i] > 1){
                return 0;
            }
        }
     
    }
    return 1;   
}

int check_squares(int (*board)[9]){
    int square_x = 0, square_y = 0;
    while (1)
    {
    int numbers[] = {0,0,0,0,0,0,0,0,0};
    for (int column = 0; column < 3; column++)
    {
        for (int row = 0; row < 3; row++)
        {
            int number = board[column + square_x][row + square_y]; // find number in cell
            if (number != 0){
                numbers[number - 1] += 1; // add 1 count to number of times it's used
            }
        }
        
        }
    
    for (int i = 0; i < 9; i++){
    if (numbers[i] > 1){
        return 0; // return false if a number appeared more than once in a 3x3 grid
        }
    }

    if (square_y == 6){
        return 1; // every 3x3 checked so return true
    }

    if (square_x == 6){
        square_y += 3;
        square_x = 0;
    }

    else{
        square_x += 3;
    }

    }// end of while true    
}

void create_board(int board[9][9]){
    for (int column = 0; column < 9; column++) {
        for (int row = 0; row < 9; row++) {
            board[column][row] = 0; // initialize the board with zeros
        }
    }  



    for (int column = 0; column < 9; column++) {// fill the board with random numbers between 1 and 9
        int column_valid = 0, squares_valid = 0, attempts = 0;

        while (column_valid == 0 || squares_valid == 0)
        {

            int numbers[] = {1, 2, 3, 4, 5, 6, 7, 8, 9}; // create an array of numbers to shuffle
            shuffle(numbers, sizeof(numbers) / sizeof(int)); // shuffle the array of numbers to put into each cell

            for (int row = 0; row < 9; row++) {
                board[column][row] = numbers[row]; // put the shuffled numbers into the board
            }
        

            column_valid = check_columns(board); // check if columns valid like this
            squares_valid = check_squares(board); // check if 3x3 grids valid
            attempts++;
            if (attempts > 100000){
                column_valid = 1, squares_valid = 1;
                for (int column = 0; column < 9; column++) {
                    for (int row = 0; row < 9; row++) {
                        board[column][row] = 0; // initialize the board with zeros
                    }
                }
                column = -1;  
            }
        }
        
    }
}

void print_board(int board[9][9]){
    for (int i = 0; i < 9; i++) { // print the board
        for (int j = 0; j < 9; j++) {
            printf("%d ", board[i][j]);
        }
        if (i != 8) { // print a new line at the end of each row except the last one
            printf("\n");
        } 
    }
}