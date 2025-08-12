#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
// x = column, y = row. column is first index, row is second index

void shuffle(int *array, size_t n);
int check_columns(int (*board)[9]);
int check_squares(int (*board)[9]);
int check_rows(int board[9][9]);
int check_board(int board[9][9]);
void create_board(int board[9][9]);
void print_board(int board[9][9]);
void remove_cell(int board[9][9], int *x_ptr, int *y_ptr);
void find_empty_cell(int board[9][9], int *x, int *y);
int turn_cords_to_cell(int *x, int *y);
void turn_cell_to_cords (int cell, int *x, int *y);
int solver(int board[9][9], int *solutions_ptr);
void create_difficulty(int original_board[9][9], int difficulty);
void write_board(int filled_board[9][9], int difficult_board[9][9]);
__declspec(dllexport) int* create_board_python();
__declspec(dllexport) int* create_difficulty_python(int* arr, int difficulty);

__declspec(dllexport) int* create_difficulty_python(int* arr, int difficulty){
    srand(time(NULL)); // seed the random number generator
    int difficultboard[9][9];
    for (int i = 0; i < 81; i++){
        difficultboard[i / 9][i % 9] = arr[i];
    }
    create_difficulty(difficultboard, difficulty);
    int new_arr[81];
    for (int x = 0; x < 9; x++){
        for (int y = 0; y < 9; y++){
            new_arr[x * 9 + y] = difficultboard[x][y];
        }
    }
    int* arr_ptr = malloc(sizeof(new_arr));
    memcpy(arr_ptr, new_arr, sizeof(new_arr));
    return arr_ptr;
}

__declspec(dllexport) int* create_board_python(){
    srand(time(NULL)); // seed the random number generator
    int filled_board[9][9];
    create_board(filled_board);
    int arr[81];
    for (int x = 0; x < 9; x++){
        for (int y = 0; y < 9; y++){
            arr[x * 9 + y] = filled_board[x][y];
        }
    }
    int* arr_ptr = malloc(sizeof(arr));
    memcpy(arr_ptr, arr, sizeof(arr));
    return arr_ptr;
}

int main() {
    srand(time(NULL)); // seed the random number generator
    int filled_board[9][9];
    create_board(filled_board);
    int difficult_board[9][9];
    memcpy(difficult_board, filled_board, sizeof(difficult_board));
    create_difficulty(difficult_board, 3);
    write_board(filled_board, difficult_board);
    return 0;
}

void write_board(int filled_board[9][9], int difficult_board[9][9]){
    FILE *fpter;
    fpter = fopen("Board.txt", "w");
    for (int x = 0; x < 9; x++){
        for (int y = 0; y < 9; y++)
        {
            int number = filled_board[x][y];
            char test[1];
            itoa(number, test, 10);
            fprintf(fpter, test);
        }
    }
    fprintf(fpter, "\n");    
    for (int x = 0; x < 9; x++){
        for (int y = 0; y < 9; y++)
        {
            int number = difficult_board[x][y];
            char test[1];
            itoa(number, test, 10);
            fprintf(fpter, test);
        }
    
        
    }
    
    fclose(fpter);
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
int check_rows(int board[9][9]){
    for (int column = 0; column < 9; column++){
        int numbers[] = {0,0,0,0,0,0,0,0,0};
        for (int row = 0; row < 9; row++){
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

int check_board(int board[9][9]){
    if (check_columns(board) == 0){
        return 0;
    }
    if (check_rows(board) == 0){
        return 0;
    }
    if (check_squares(board) == 0){
        return 0;
    }
    return 1;
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
    printf("\n___________________\n");
    for (int i = 0; i < 9; i++) { // print the board
        for (int j = 0; j < 9; j++) {
            printf("%d ", board[i][j]);
        }
        if (i != 8) { // print a new line at the end of each row except the last one
            printf("\n");
        } 
    }
}

void find_empty_cell(int board[9][9], int *x, int *y){
    for (int column = 0; column < 9; column++){
        for (int row = 0; row < 9; row++){
            if (board[column][row] == 0){
                *x = column;
                *y = row;
                return;
            }
        }
    }
    *x = -1, *y = -1;
}

void remove_cell(int board[9][9], int *x_ptr, int *y_ptr){
    while (1){
    int x = rand() % 9, y = rand() % 9;
    if (board[x][y] != 0){
        board[x][y] = 0; 
        *x_ptr = x;
        *y_ptr = y;
        return;
        }
    }
}
int solver(int board[9][9], int *solutions_ptr){
    if (*solutions_ptr > 1){
        return 0;
    }
    int x, y;
    find_empty_cell(board, &x, &y);
    if (x && y == -1){
        return 1; 
    }
    for (int i = 1; i < 10; i++){
        board[x][y] = i;

        if (check_board(board) == 1){
            int board_copy[9][9];
            memcpy(board_copy, board, sizeof(board_copy));
            if (solver(board_copy, solutions_ptr) == 1){
                *solutions_ptr += 1;
            }
        }

    }
    return 0;
}

void turn_cell_to_cords (int cell, int *x, int *y){
    if (cell == -1){
        printf("Cell equals zero... exiting after you press enter: ");
        getchar();
        exit(EXIT_FAILURE);
    }
    *y = cell / 9; //  take cell number divided by 9 gives us y cord
    *x = cell % 9; // take remainder of division by 9 to find x cord
}
int turn_cords_to_cell(int *x, int *y){
    int cell;
    cell = (*y) * 9;
    cell += (*x);
    return cell;
}
// x = column, y = row. column is first index, row is second index
void create_difficulty(int original_board[9][9], int difficulty){

    int board[9][9];
    memcpy(board, original_board, sizeof(board));// create copy of the original board
    int cells, removed_cells = 0, x, y, solutions, attempts = 0;
    int used_cords[81];

    switch (difficulty)
        {
        case 1:
            cells = 45;
            break;
        case 2:
            cells = 54;
            break;
        case 3:
            cells = 62;
            break;
        default:
        printf("You need to specify difficulty... not creating difficult board");
            return;
        }


    while (removed_cells < cells){
        solutions = 0;
        remove_cell(board, &x, &y); // remove random cell
        used_cords[removed_cells] = turn_cords_to_cell(&x, &y);
        removed_cells++;
        int solver_board[9][9];
        memcpy(solver_board, board, sizeof(solver_board));
        solver(solver_board, &solutions);

        if (solutions != 1){
            attempts++;
            removed_cells--;
            board[x][y] = original_board[x][y];
            used_cords[removed_cells] = -1;

            if (attempts > 5){

                if (cells == 62){

                    if (removed_cells >= 55){

                        for (int x = 0; x < 9; x++){

                            for (int y = 0; y < 9; y++){
                                original_board[x][y] = board[x][y];
                            }    
                        }
                        return;
                    }
                }        
                attempts = 0;
                removed_cells--;
                turn_cell_to_cords(used_cords[removed_cells], &x, &y);
                board[x][y] = original_board[x][y];
                used_cords[removed_cells] = -1;
                }// end of attempts if statement
            }// end of solutions if statement
        else{
            attempts = 0;
        }// end of else
    }// end of while loop            
    for (int x = 0; x < 9; x++){

        for (int y = 0; y < 9; y++){
            original_board[x][y] = board[x][y];
        }
    }
}// end of function    