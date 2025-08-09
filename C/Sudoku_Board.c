#include <stdio.h>
#include <stdlib.h>
#include <time.h>


void shuffle(int *array, size_t n);
int check_columns(int (*board)[9]);

int main() {
    srand(time(NULL)); // seed the random number generator
    int board[9][9]; // 9x9 board
    for (int column = 0; column < 9; column++) {
        for (int row = 0; row < 9; row++) {
            board[column][row] = 0; // initialize the board with zeros
        }
    }  

    for (int column = 0; column < 9; column++) {// fill the board with random numbers between 1 and 9
        int column_valid = 0;
        while (column_valid == 0)
        {

            int numbers[] = {1, 2, 3, 4, 5, 6, 7, 8, 9}; // create an array of numbers to shuffle
            shuffle(numbers, sizeof(numbers) / sizeof(int)); // shuffle the array of numbers to put into each cell

            for (int row = 0; row < 9; row++) {
                board[column][row] = numbers[row]; // put the shuffled numbers into the board
            }

            column_valid = check_columns(board); // check if columns valid like this
        }
    }
    



    for (int i = 0; i < 9; i++) { // print the board
        for (int j = 0; j < 9; j++) {
            printf("%d ", board[i][j]);
        }
        if (i != 8) { // print a new line at the end of each row except the last one
            printf("\n");
        } 
    }
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