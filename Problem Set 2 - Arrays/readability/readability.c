#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int main(void)
{
    float letters = 0;
    float words = 1;
    float sentences = 0;
    string text = get_string("Text: ");

    /*loop*/
    for (int i = 0; i < strlen(text); i++)
    {
        if (isalpha(text[i]))
        {
            letters++;
        }
        else if (text[i] == ' ')
        {
            words++;
        }
        else if (text[i] == '.' || text[i] == '?' || text[i] == '!')
        {
            sentences++;
        }
    }

    /*variable*/
    float L = ((letters / words) * 100);
    float S = ((sentences / words) * 100);

    /*index*/
    float index = ((0.0588 * L) - (0.296 * S) - 15.8);

    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (16 >= index >= 1)
    {
        printf("Grade %.0f\n", index);
    }
    else
    {
        printf("Grade 16+\n");
    }
}
