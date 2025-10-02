#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int main(void)
{
    int sum1 = 0, sum2 = 0;
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    for (int i = 0; i < strlen(word1); i++)
    {
        char c = tolower(word1[i]);
        if (c == 'a' || c == 'e' || c == 'i' || c == 'l' || c == 'n' || c == 'o' || c == 'r' ||
            c == 's' || c == 't' || c == 'u')
            sum1 += 1;
        else if (c == 'b' || c == 'c' || c == 'm' || c == 'p')
            sum1 += 3;
        else if (c == 'd' || c == 'g')
            sum1 += 2;
        else if (c == 'f' || c == 'h' || c == 'v' || c == 'w' || c == 'y')
            sum1 += 4;
        else if (c == 'j')
            sum1 += 8;
        else if (c == 'k')
            sum1 += 5;
        else if (c == 'q' || c == 'z')
            sum1 += 10;
    }

    for (int i = 0; i < strlen(word2); i++)
    {
        char c = tolower(word2[i]);
        if (c == 'a' || c == 'e' || c == 'i' || c == 'l' || c == 'n' || c == 'o' || c == 'r' ||
            c == 's' || c == 't' || c == 'u')
            sum2 += 1;
        else if (c == 'b' || c == 'c' || c == 'm' || c == 'p')
            sum2 += 3;
        else if (c == 'd' || c == 'g')
            sum2 += 2;
        else if (c == 'f' || c == 'h' || c == 'v' || c == 'w' || c == 'y')
            sum2 += 4;
        else if (c == 'j')
            sum2 += 8;
        else if (c == 'k')
            sum2 += 5;
        else if (c == 'q' || c == 'z')
            sum2 += 10;
    }

    // Mostrar resultado
    if (sum1 > sum2)
        printf("Player 1 wins!\n");
    else if (sum1 < sum2)
        printf("Player 2 wins!\n");
    else
        printf("Tie!\n");
}
