// ECE 385 IS THE WORST CLASS EVER

#include <stdio.h>
#include "aes.c"

void printSquare(char* const data, int width, int height) {
    int i, j;
    char higher, lower;
	for(i = 0; i < height; i++) {
		for(j = 0; j < width; j++) {
			higher = (data[width*i + j] & 0xF0) >> 4;
			lower = (data[width*i + j] & 0x0F);

            if (higher >= 0 && higher <= 9)
				higher += '0';
			else if (higher >= 10 && higher <= 15)
			{
				higher += 'a';
				higher -= 10;
			}

		    if (lower >= 0 && lower <= 9)
				lower += '0';
			else if (lower >= 10 && lower <= 15)
			{
				lower += 'a';
				lower -= 10;
			}

  			printf("%c%c ", higher, lower);
		}
		printf("\n");
	}
	printf("\n");
}

char charToHex(char c)
{
	char hex = c;

	if (hex >= '0' && hex <= '9')
		hex -= '0';
	else if (hex >= 'A' && hex <='F')
	{
		hex -= 'A';
		hex += 10;
	}
	else if (hex >= 'a' && hex <='f')
	{
		hex -= 'a';
		hex += 10;
	}
	return hex;
}

char charsToHex(char c1, char c2)
{
	char hex1 = charToHex(c1);
	char hex2 = charToHex(c2);
	return (hex1 << 4) + hex2;
}

char SubByte(char word1){
	/* Get the coordinates for S-Box */
	unsigned int coord1 = word1 & 0xF0;
	coord1 = coord1 >> 4;
	unsigned int coord2 = word1 & 0x0F;

	return aes_sbox[coord1][coord2];
}

void SubBytes(char* wordSquare){
	int i,j;
	for(i = 0; i < 4; i++){
		for(j = 0; j < 4; j++){
			wordSquare[4*j + i]=SubByte(wordSquare[4*j + i]);
		}
	}
}

void ShiftRows(char* wordSquare){
	int i,j;
	for(j = 1; j < 4; j++){
		for(i = 0; i < j; i++){
			char temp = wordSquare[4*j + 0];
			wordSquare[4*j + 0]=wordSquare[4*j + 1];
			wordSquare[4*j + 1]=wordSquare[4*j + 2];
			wordSquare[4*j + 2]=wordSquare[4*j + 3];
			wordSquare[4*j + 3]=temp;
		}
	}
}

char Xor(char word, int val){
	if(val==1)
		return word;
	else if(val==2){
		if(word&0x80){
			word=word<<1;
			return word^0x1b;
		}
		return word<<1;
	}
	else{
		char ogWord=word;
		if(word&0x80){
			word=word<<1;
			word^=0x1b;
		}
		else
			word=word<<1;

		return ogWord^word;
	}
}

void MixColumns(char* wordSquare){
	int i;
    char temp0, temp1, temp2, temp3;

	for(i = 0; i < 4; i++){
		temp0= Xor(wordSquare[4*0 + i],2);
		temp0^=Xor(wordSquare[4*1 + i],3);
		temp0^=Xor(wordSquare[4*2 + i],1);
		temp0^=Xor(wordSquare[4*3 + i],1);

		temp1= Xor(wordSquare[4*0 + i],1);
		temp1^=Xor(wordSquare[4*1 + i],2);
		temp1^=Xor(wordSquare[4*2 + i],3);
		temp1^=Xor(wordSquare[4*3 + i],1);

		temp2= Xor(wordSquare[4*0 + i],1);
		temp2^=Xor(wordSquare[4*1 + i],1);
		temp2^=Xor(wordSquare[4*2 + i],2);
		temp2^=Xor(wordSquare[4*3 + i],3);

		temp3= Xor(wordSquare[4*0 + i],3);
		temp3^=Xor(wordSquare[4*1 + i],1);
		temp3^=Xor(wordSquare[4*2 + i],1);
		temp3^=Xor(wordSquare[4*3 + i],2);

		wordSquare[4*0 + i]=temp0;
		wordSquare[4*1 + i]=temp1;
		wordSquare[4*2 + i]=temp2;
		wordSquare[4*3 + i]=temp3;
	}
}

void AddRoundKey(char* wordSquare, char* roundKey){
	int i,j;
	for(i=0; i<4; i++){
		for(j=0; j<4; j++){
			wordSquare[4*j + i]^=roundKey[4*j + i];
		}
	}
}

void string2array(char* wordSq, char* plaintext)
{
	char a,b;
	int i,j;
	for(i = 0; i < 4; i++){
		for(j = 0; j < 4; j++)
		{
			a = plaintext[2*(4*i + j)];
			b = plaintext[2*(4*i + j) + 1];

			wordSq[4*j + i] = charsToHex(a,b);
		}
	}
}

void makeKeySched(char* keySq, char* keySchedule){
	int i, j;
	char temp[4];
	for(i=0; i<4; i++){
		for(j=0; j<4; j++){
			keySchedule[44*j + i] = keySq[4*j + i];
		}
	}


	for(i=4; i<44; i++){
		if(i%4==0){
			temp[0] = keySchedule[(i-1) + 1*44];
			temp[1] = keySchedule[(i-1) + 2*44];
			temp[2] = keySchedule[(i-1) + 3*44];
			temp[3] = keySchedule[(i-1) + 0*44]; //RotWord
			for(j=0; j<4; j++){
				temp[j] = SubByte(temp[j]); //SubBytes
			}
			temp[0]^=Rcon[i/4-1] >> 6*4;
			for(j=0; j<4; j++){
				keySchedule[44*j + i]=keySchedule[44*j + (i-4)]^temp[j];
			}
		}
		else{
			for(j=0; j<4; j++){
				keySchedule[44*j + i]=keySchedule[44*j + (i-1)]^keySchedule[44*j + (i-4)];
			}
		}
	}
}


// Function hex2char:
void hex2char(char hexVal, char* buffer, int index) {
	char higher, lower;
    higher = (hexVal & 0xF0) >> 4;
    lower = (hexVal & 0x0F);

    if (higher >= 0 && higher <= 9)
		higher += '0';
	else if (higher >= 10 && higher <= 15)
	{
		higher += 'a';
		higher -= 10;
	}

    // Set the higher char as the first character:
	buffer[index] = higher;

    if (lower >= 0 && lower <= 9)
		lower += '0';
	else if (lower >= 10 && lower <= 15)
	{
		lower += 'a';
		lower -= 10;
	}

	// Set the lower char as the second character:
	buffer[index + 1] = lower;
}

// Function square to string:
void square2string(char* array, char* buffer) {
    int i, j;
	for(i = 0; i < 4; i++){
		for(j = 0; j < 4; j++){
			// Call uppon macro function that converts hex to chars:
			// Read down columns:
			hex2char(array[4*j + i], buffer, 2*(4*i + j));
		}
	}
	buffer[32] = '\0';
}


int main()
{
	char plaintext[33] = {"ece298dcece298dcece298dcece298dc"}; //should be 1 more character to account for string terminator
	char key[33] = {"000102030405060708090a0b0c0d0e0f"};

	char wordSq[16];
	char keySq[16];
	char keySchedTemp[16];
    char keySchedule[176];

    char cypher[33];

    int i,j,k;

//	while (1)
//	{
		printf("\n");

		printf("Enter plain text:\n");
		scanf ("%s", plaintext);
		printf ("\n");
		printf("Enter key:\n");
		scanf ("%s", key);
		printf ("\n");


		// Convert the plaintext and key into 4x4 arrays:
		string2array(keySq, key);
		printf("keySq: \n");
		printSquare(keySq, 4, 4);
		string2array(wordSq, plaintext);
		printf("keySq: \n");
		printSquare(wordSq, 4, 4);


		// Make key schedule:
		makeKeySched(keySq, keySchedule);
		printf("keySchedule: \n");
		printSquare(keySchedule, 44, 4);

		//Key Expansion and AES encryption using week 1's AES algorithm.
	    // 1: Add round key:
		printf("Add Roundkey 1: \n");
		AddRoundKey(wordSq, keySq);
		printSquare(wordSq, 4, 4);

		// 2: Looping construct:
		for(i = 0; i < 9; i++){
			// 2.1: SubBytes
			SubBytes(wordSq);
			printf("Add SubBytes %d: \n", i);
			printSquare(wordSq, 4, 4);
			// 2.2: ShiftRows
			ShiftRows(wordSq);
			printf("Add ShiftRows %d: \n", i);
			printSquare(wordSq, 4, 4);
			// 2.3: Mix Columns
			MixColumns(wordSq);
			printf("Add MixColumns %d: \n", i);
			printSquare(wordSq, 4, 4);
			// 2.4: Add ROundkey with keySchedule
			for(j=0; j<4; j++){
				for(k=0; k<4; k++){
					keySchedTemp[4*j + k]=keySchedule[44*j + k + 4*(i + 1)];
				}
			}
			printf("Add AddRoundKey %d: \n", i);
			AddRoundKey(wordSq, keySchedTemp);
			printSquare(wordSq, 4, 4);
		}

		// 3.1: SubBytes
		SubBytes(wordSq);
		printf("Add SubBytes 10: \n");
		printSquare(wordSq, 4, 4);
		// 3.2: ShiftRows
		ShiftRows(wordSq);
		printf("Add ShiftRows 10: \n");
		printSquare(wordSq, 4, 4);
		// 3.3: Add KeySchedule
		for(j=0; j<4; j++){
			for(k=0; k<4; k++){
				keySchedTemp[4*j + k]=keySchedule[44*j + k + 40];
			}
		}
		AddRoundKey(wordSq,keySchedTemp);
		printf("Add AddRoundKey 10: \n");
		printSquare(wordSq, 4, 4);

		// Convert back to a plaintext:
		square2string(wordSq, cypher);

		printf("\n%s\n", cypher);
//	}

	return 0;
}
