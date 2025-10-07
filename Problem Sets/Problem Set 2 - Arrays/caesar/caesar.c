#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

bool dec_mal(string a);

int main(int argc, string argv[])
{
    if (argc != 2 || !dec_mal(argv[1]))
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    int key = atoi(argv[1]) % 26;
    string in = get_string("plaintext:  ");

    printf("ciphertext: ");
    int len = strlen(in);

    for (int i = 0; i < len; i++)
    {
        if (isalpha(in[i]))
        {
            if (isupper(in[i]))
            {
                in[i] = ((in[i] - 'A' + key) % 26) + 'A';
            }
            else
            {
                in[i] = ((in[i] - 'a' + key) % 26) + 'a';
            }
        }
        printf("%c", in[i]);
    }
    printf("\n");
}

bool dec_mal(string a)
{
    for (int i = 0; i < strlen(a); i++)
    {
        if (!isdigit(a[i]))
        {
            return false;
        }
    }
    return true;
}
