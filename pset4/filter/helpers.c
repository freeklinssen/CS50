#include "helpers.h"
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float average = (image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue)/3.00;
            int average2 = round(average);
            
            image[i][j].rgbtRed = average2;
            image[i][j].rgbtGreen = average2;
            image[i][j].rgbtBlue = average2;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float sr = (image[i][j].rgbtRed * 0.393 + image[i][j].rgbtGreen * 0.769 + image[i][j].rgbtBlue * 0.189);
            if (sr > 255)
            {
                sr = 255;
            }
            int sr2 = round(sr);
            
            float sg = (image[i][j].rgbtRed * 0.349 + image[i][j].rgbtGreen * 0.686 + image[i][j].rgbtBlue * 0.168);
            if (sg > 255)
            {
                sg = 255;
            }
            int sg2 = round(sg);
            
            float sb = (image[i][j].rgbtRed * 0.272 + image[i][j].rgbtGreen * 0.534 + image[i][j].rgbtBlue * 0.131);
            if (sb > 255)
            {
                sb = 255;
            }
            int sb2 = round(sb);
            
            
            image[i][j].rgbtRed = sr2;
            image[i][j].rgbtGreen = sg2;
            image[i][j].rgbtBlue = sb2; 
          
        }
    }
    return;
}
    
    

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    
    
    RGBTRIPLE temp[height][width];
    
    // Iterate over infile's scanlines
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            temp[i][j] = image[i][j];
        }
    }
    
        
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = temp[i][width - j - 1];
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
            temp[i][j] = image[i][j];
        }
    }
    
    
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int red = 0;
            int green = 0;
            int blue = 0;
            float count = 0;
            
            for (int h = -1; h <= 1; h++)
            {
                for (int v = -1; v <= 1; v++)
                {
                    if (i + h < 0 || i + h > height - 1 || j + v < 0 || j + v > width - 1)
                    {
                        continue;
                    } 
                    else 
                    {
                        red += temp[i + h][j + v].rgbtRed;
                        green += temp[i + h][j + v].rgbtGreen;
                        blue += temp[i + h][j + v].rgbtBlue;
                        count += 1;
                    }  
                }
            }  
            red = round(red / count);
            green = round(green / count);
            blue = round(blue / count); 
                
            image[i][j].rgbtRed = red;
            image[i][j].rgbtGreen = green;
            image[i][j].rgbtBlue = blue;
                
        }
            
            
        
    }
    
    
    return;
}
