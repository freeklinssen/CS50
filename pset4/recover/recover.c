#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
//memcmp

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    char *infile = argv[1];

    FILE *input = fopen(infile, "r");
    FILE *output = NULL;

    if (input == NULL)
    {
        printf("Could not open %s\n", infile);
        return 1;
    }


    uint8_t block[512];


    int i = 0;
    int a = 0;
    int b = 0;

    while (fread(&block, sizeof(uint8_t), 512, input))
    {


        if (block[0] == 0xff && block[1] == 0xd8 && block[2] == 0xff && (block[3] >= 0xe0 && block[3] <= 0xef))
        {

            if (output != NULL)
            {
                fclose(output);
            }

            char *name = malloc(8);

            sprintf(name, "%i%i%i.jpg", b, a, i);

            output = fopen(name, "w");


            fwrite(&block, sizeof(block), 1, output);


            i++;

            if (i == 10)
            {
                i = 0;
                a++;
            }

            if (a == 10)
            {
                a = 0;
                b ++;
            }

            free(name);

        }

        else
        {
            if (output != NULL)
            {
                fwrite(&block, sizeof(block), 1, output);
            }

        }
    }


    fclose(input);

    if (output != NULL)
    {
        fclose(output);
    }



}