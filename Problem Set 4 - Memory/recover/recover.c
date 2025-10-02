#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover FILE\n");
        return 1;
    }

    FILE *card = fopen(argv[1], "r");
    if (card == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    uint8_t buffer[512];
    int counter = 0;
    char filename[8];
    FILE *img = NULL;

    while (fread(buffer, 1, 512, card) == 512)
    {
        // Detecta novo JPEG
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            // Se já havia imagem aberta → fecha
            if (img != NULL)
            {
                fclose(img);
            }

            // Cria novo arquivo
            sprintf(filename, "%03i.jpg", counter);
            counter++;
            img = fopen(filename, "w");
        }

        // Se já temos um JPEG aberto, escrevemos o bloco
        if (img != NULL)
        {
            fwrite(buffer, 1, 512, img);
        }
    }

    if (img != NULL)
    {
        fclose(img);
    }

    fclose(card);
    return 0;
}
