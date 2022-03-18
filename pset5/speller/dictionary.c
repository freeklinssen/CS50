// Implements a dictionary's functionality
#include <ctype.h>
#include <stdio.h>
#include <cs50.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    struct node *next;
    char word[LENGTH + 1];
}
node;

// Number of buckets in hash table
const unsigned int N = 2184;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    char c;
    char word_low[LENGTH + 1];
    
    
    for (int i = 0; i <= strlen(word); i++)
    {
        c = word[i];
        
        if (isalpha(c) || c == '\0')
        {
            c = tolower(c);
            word_low[i] = c;
        }
        
        if (c == '\'' && i > 0)
        {
            word_low[i] = c;
        }
        
        //rintf(" %s\n", word_low);
        

    }
    
    int row = hash(word_low);

        
    for (node *tmp = table[row]; tmp != 0; tmp = tmp->next)
    {
        if (strcmp(word_low, tmp->word) == 0)
        {
            return true;
        }
         

    }
     
     
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO
    int number = word[0] - 97; 
    
    number = number * 28;
    
    int extra;
    
    if (word[1] == 39)
    {
        extra = 27;
        
    }
    if (word[1] == 00)
    {
        extra = 28;
    }
    else
    {
        extra = word[1] - 97;
    }
    number = number + extra;
    
    if (strlen(word) <= 4)
    {
        number = number + 728;
    }
    
    if (strlen(word) > 8)
    {
        number = number + 1469;
    }
    
    return number;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    
    for (int i = 0; i <= N; i++)
    {
        table[i] = NULL; 
    }
    
    
    FILE *file = fopen(dictionary, "r");
    
    if (file == false)
    {
        printf("could not open %s", dictionary);
        return false;
    }

    
    char word2[LENGTH + 1];
    char c;
    int count = 0;
    
    while (fread(&c, sizeof(char), 1, file))
    {
        
        if (isalpha(c) || (c == '\'' && count > 0))
        {
            word2[count] = c;
            
            count++;
            
        }
        
        else if (c == '\n')
        {
            word2[count] = '\0';
            
            
            int hashnum = hash(word2);
            
            node *tmp = malloc(sizeof(node));
            tmp->next = NULL;
            
            for (int i = 0; i < LENGTH + 1; i++)
            {
                tmp->word[i] = word2[i];  
            }
            
            tmp->next = table[hashnum];
            table[hashnum] = tmp; 
             
            
            /*
            if (strlen(word2) < 4)
            {
                tmp->next = table[hashnum];
                table[hashnum] = tmp; 
            }
            
            else
            {
                if (table[hashnum] == NULL)
                {
                    tmp->next = table[hashnum];
                    table[hashnum] = tmp; 
                }
                
                else
                {
                    node *last = table[hashnum];
                    int a = 0;
                    
                    while (last->next != NULL)
                    {
                        
                        if (a == 5)
                        {
                            tmp->next = last->next->next;
                            last->next = tmp;
                            break;
                        }
                        
                        last = last->next;
                        a++;
                    }
                    
                    last->next = tmp;

                }
            }
            */
            
    
            
            count = 0;
        }
            
        else
        {
            return false;
        }
        
    }
    
    
    fclose(file);
    
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    
    int count = 0;
    
    for (int i = 0; i <= N; i++)
    {
        for (node *tmp = table[i]; tmp != 0; tmp = tmp->next)
        {
            count++;
        }
    }
    
    
    return count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i <= N; i++)
    
    {
        
        while (table[i] != NULL)
        {
            node *tmp = table[i]->next;
            free(table[i]);
            table[i] = tmp; 
        }
       
    }
    
    
    return true;
}


