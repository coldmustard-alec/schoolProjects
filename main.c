#include <stdio.h>
#include <stdlib.h>
#include <dirent.h>
#include <memory.h>


struct Trienode{

    struct Trienode *childNode[26];
    char subword[50];
    int isWordEnd;
    int lastNode;
};

int toIndex(char c){

    return ((int)c - (int)'a');
}


void insert(struct Trienode *n, char *word){

    long wordEnd = strlen(word) - 1;
    struct Trienode *root = n;

    for(int i = 0; i < strlen(word); i++){

        int charIndex = toIndex(word[i]);

        if(root->childNode[charIndex] == NULL){

            struct Trienode *tempNode = NULL;
            tempNode = malloc(sizeof(struct Trienode));

            if(tempNode != NULL) {

                for (int j = 0; j < 26; j++) {

                    tempNode->childNode[j] = NULL;
                }

                tempNode->lastNode = 0;

                if(i == wordEnd){
                    tempNode->isWordEnd = 1;
                    strcpy(tempNode->subword,word);
                }
            }

            root->childNode[charIndex] = tempNode;
            root = root->childNode[charIndex];

        } else {root = n->childNode[charIndex];}

    }

    root->lastNode = 1;
}


void printSubTrie(struct Trienode *n){

    if(n->isWordEnd){
        printf("%s\n", n->subword);
    }

    for(int i = 0; i < 26; i++){
        if(n->childNode[i] != NULL){
            printSubTrie(n->childNode[i]);
        }
    }

}


struct Trienode *search(struct Trienode *n, char *word){

    struct Trienode *root = n;

    for(int i = 0; i < strlen(word); i++){

        int charIndex = toIndex(word[i]);

        if(root->childNode[charIndex] == NULL) {return root;}
        else {

            root = root->childNode[charIndex];
            search(root,word);

        }

    }

    return root;

}


int main() {

    struct Trienode *trie;
    trie = malloc(sizeof(struct Trienode));

    char input[50];
    DIR* dir;
    struct dirent *d_ent;

    printf("Enter a folder name: ");
    scanf("%s",input);
    dir = opendir(input);

    if(dir == NULL) { printf("No such directory"); return 0; }
    else {

        d_ent = readdir(dir);

        while((d_ent = readdir(dir)) != NULL) {

            if(toIndex(*d_ent->d_name) != -51){
                insert(trie, d_ent->d_name);
            }
        }

        closedir(dir);
    }

    char key[50];

    while(strcmp(key,":q") != 0){
        printf("> ");
        scanf("%s", key);

        struct Trienode *subtrie = search(trie, key);
        if(subtrie != NULL){
            printSubTrie(subtrie);
        }

    }

    free(trie->childNode); free(trie);

}
