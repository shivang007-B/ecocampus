#include <stdio.h>
int main() {
    int marks[4];
    int sum = 0;
    float percentage;

    printf("Enter marks in 4 subjects (out of 100):\n");
    for(int i = 0; i < 4; i++) {
        if(scanf("%d", &marks[i]) != 1) {
            printf("Invalid input! Please enter an integer.\n");
            return 1;
        }
        if(marks[i] < 0 || marks[i] > 100) {
            printf("Marks must be between 0 and 100.\n");
            return 1;
        }
        sum += marks[i];
    }

    percentage = (sum / 400.0) * 100;
    printf("Percentage = %.2f%%\n", percentage);

    return 0;
}
