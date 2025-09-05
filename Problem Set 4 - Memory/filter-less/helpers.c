#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    int average = 0;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            average = (int) round(
                (image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0);
            image[i][j].rgbtBlue = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtRed = average;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    int sepiared = 0;
    int sepiagreen = 0;
    int sepiablue = 0;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            sepiared = (int) round(image[i][j].rgbtRed * (0.393) + image[i][j].rgbtGreen * (0.769) +
                                   image[i][j].rgbtBlue * (0.189));
            sepiagreen =
                (int) round(image[i][j].rgbtRed * (0.349) + image[i][j].rgbtGreen * (0.686) +
                            image[i][j].rgbtBlue * (0.168));
            sepiablue =
                (int) round(image[i][j].rgbtRed * (0.272) + image[i][j].rgbtGreen * (0.534) +
                            image[i][j].rgbtBlue * (0.131));

            if (sepiared > 255)
            {
                sepiared = 255;
            }

            if (sepiagreen > 255)
            {
                sepiagreen = 255;
            }

            if (sepiablue > 255)
            {
                sepiablue = 255;
            }

            image[i][j].rgbtBlue = sepiablue;
            image[i][j].rgbtGreen = sepiagreen;
            image[i][j].rgbtRed = sepiared;
        }
    }
    return;
}
// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];
    int ourwidth = 0;

    if (width % 2 == 0)
    {
        ourwidth = width / 2;
    }
    else
    {
        ourwidth = width / 2 + 1;
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < ourwidth; j++)
        {
            temp[i][j] = image[i][j];
            image[i][j] = image[i][width - 1 - j];
            image[i][width - 1 - j] = temp[i][j];
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int totalred = 0;
            int totalgreen = 0;
            int totalblue = 0;
            int counter = 0;

            for (int local_i = i - 1; local_i <= i + 1; local_i++)
            {
                for (int local_j = j - 1; local_j <= j + 1; local_j++)
                {
                    if (local_i >= 0 && local_i < height && local_j >= 0 && local_j < width)
                    {
                        totalred += image[local_i][local_j].rgbtRed;
                        totalgreen += image[local_i][local_j].rgbtGreen;
                        totalblue += image[local_i][local_j].rgbtBlue;
                        counter++;
                    }
                }
            }
            temp[i][j].rgbtRed = (int) round((float) totalred / counter);
            temp[i][j].rgbtGreen = (int) round((float) totalgreen / counter);
            temp[i][j].rgbtBlue = (int) round((float) totalblue / counter);
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = temp[i][j];
        }
    }
    return;
}
