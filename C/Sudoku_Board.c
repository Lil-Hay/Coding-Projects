#include <stdio.h>
#include <stdlib.h>
#include <time.h>


typedef struct {
    int* data;
    int size;
    int capacity;
} DynamicArray;

DynamicArray* createDynamicArray(int initialCapacity) {
    DynamicArray* array = malloc(sizeof(DynamicArray));
    array->data = malloc(sizeof(int) * initialCapacity);
    array->size = initialCapacity;
    array->capacity = initialCapacity;
    return array;
}

int getElement(DynamicArray* array, int index) {
    if (index < 0 || index >= array->size) {
        printf("Error: Index out of bounds\n");
        exit(1);
    }
    return array->data[index];
}

void freeDynamicArray(DynamicArray* array) {
    free(array->data);
    free(array);
}
void removeElement(DynamicArray* array, int index) {
    if (index < 0 || index >= array->size) {
        printf("Error: Index out of bounds\n");
        exit(1);
    }
    // Shift elements to the left to fill the gap
    for (int i = index; i < array->size - 1; i++) {
        array->data[i] = array->data[i + 1];
    }
    array->size--;
}

int main() {
    srand(time(NULL)); // seed the random number generator
    int board[9][9]; // 9x9 board
    for (int i = 0; i < 9; i++) { // fill the board with random numbers between 1 and 9
        DynamicArray* numbers = createDynamicArray(9); // create a dynamic array to hold the numbers

        for (int n = 0; n < numbers->size; n++) {
            numbers->data[n] = n + 1; // Assign a value to each element
            }

        for (int j = 0; j < 9; j++) {
            int random = rand() % sizeof(numbers) / sizeof(int); // get a random index
            board[i][j] = getElement(numbers, random);  // get the element at the random index and assign it to the board
            removeElement(numbers, random); // remove the element at the random index
        }

        freeDynamicArray(numbers);
    }

    for (int i = 0; i < 9; i++) { // print the board
        for (int j = 0; j < 9; j++) {
            printf("%d ", board[i][j]);
        }
        if (i != 8) { // print a new line at the end of each row except the last one
            printf("\n");
        } 
    }
    printf("\n%zu", sizeof(board) / sizeof(int)); // print the size of the board in memory
    return 0;
}